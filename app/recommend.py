import os
import logging
import pandas as pd
import numpy as np
import joblib

from app.schemas import RoomInput

# -------------------------
# Настройка логирования
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# Пути из окружения (.env)
# -------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "ml/best_model.pkl")
PREPROCESSOR_PATH = os.getenv("PREPROCESSOR_PATH", "ml/preprocessor.pkl")
FIXTURES_PATH = os.getenv("FIXTURES_PATH", "data/fixtures.csv")
TOP_N = int(os.getenv("TOP_N", 3))

# -------------------------
# Загрузка артефактов
# -------------------------
try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    fixtures_df = pd.read_csv(FIXTURES_PATH)
    logger.info("✅ Модель, препроцессор и каталог успешно загружены.")
except Exception as e:
    logger.exception(f"Ошибка загрузки артефактов: {e}")
    raise RuntimeError("Ошибка при инициализации модели.")


# -------------------------
# Основная функция рекомендаций
# -------------------------
def recommend_luminaires(input_data):
    try:
        # Универсальная обработка входа (Pydantic v1/v2/dict)
        if hasattr(input_data, "model_dump"):
            data = input_data.model_dump(by_alias=True)
        elif hasattr(input_data, "dict"):
            data = input_data.dict(by_alias=True)
        else:
            data = input_data

        df_input = pd.DataFrame([data])

        # Переименование при необходимости
        if "budget_rub" in df_input.columns:
            df_input["бюджет_₽"] = df_input.pop("budget_rub")

        # Извлечение базовых параметров
        E = df_input["целевой_люкс"].iloc[0]
        S = df_input["площадь_м2"].iloc[0]
        η = 0.6  # коэффициент использования света
        бюджет = df_input["бюджет_₽"].iloc[0]

        # ----------------------------------------
        # Расчёт количества светильников индивидуально по потоку
        # ----------------------------------------
        fixtures_expanded = fixtures_df.copy()
        for col in df_input.columns:
            fixtures_expanded[col] = df_input.iloc[0][col]

        # Количество приборов
        fixtures_expanded["количество_светильников"] = np.ceil(
            (E * S) / (fixtures_expanded["световой_поток_лм"] * η)
        ).clip(lower=1).astype(int)

        # ----------------------------------------
        # Инференс модели
        # ----------------------------------------
        X_processed = preprocessor.transform(fixtures_expanded)
        y_pred = model.predict(X_processed)
        fixtures_expanded["предсказанная_оценка"] = y_pred

        # ----------------------------------------
        # Инженерные расчёты
        # ----------------------------------------
        fixtures_expanded["итоговая_мощность_вт"] = (
            fixtures_expanded["мощность_вт"] * fixtures_expanded["количество_светильников"]
        ).round(1)
        fixtures_expanded["итоговая_стоимость_₽"] = (
            fixtures_expanded["цена_₽"] * fixtures_expanded["количество_светильников"]
        ).round(2)

        # Фактическая освещённость (лк)
        fixtures_expanded["освещенность_лк"] = (
            (fixtures_expanded["световой_поток_лм"] *
             fixtures_expanded["количество_светильников"] *
             η) / S
        ).round(1)

        # Доля от бюджета
        fixtures_expanded["доля_бюджета_%"] = (
            fixtures_expanded["итоговая_стоимость_₽"] / бюджет * 100
        ).round(1)

        # Оценка пересвета/недосвета
        fixtures_expanded["уровень_освещения"] = np.where(
            fixtures_expanded["освещенность_лк"] > E * 1.2, "пересвет",
            np.where(fixtures_expanded["освещенность_лк"] < E * 0.8, "недосвет", "норма")
        )

        # ----------------------------------------
        # Выбор top-N
        # ----------------------------------------
        top_recs = fixtures_expanded.sort_values(by="предсказанная_оценка", ascending=False).head(TOP_N)

        # Поля для вывода
        results = top_recs[[
            "тип_светильника", "бренд", "серия",
            "мощность_вт", "световой_поток_лм", "цена_₽",
            "количество_светильников", "итоговая_мощность_вт",
            "итоговая_стоимость_₽", "освещенность_лк", "уровень_освещения",
            "доля_бюджета_%", "предсказанная_оценка"
        ]].to_dict(orient="records")

        # ----------------------------------------
        # Текстовый summary
        # ----------------------------------------
        summary_lines = []
        for r in results:
            line = (
                f"💡 {r['бренд']} {r['тип_светильника']} ({r['серия']}) — "
                f"{r['количество_светильников']} шт., "
                f"≈{r['освещенность_лк']} лк ({r['уровень_освещения']}), "
                f"стоимость {r['итоговая_стоимость_₽']} ₽ "
                f"({r['доля_бюджета_%']}% бюджета)."
            )
            summary_lines.append(line)

        summary = "\n".join(summary_lines)

        logger.info(f"✅ Успешно сформировано {len(results)} рекомендаций.")
        return {"recommendations": results, "summary": summary}

    except Exception as e:
        logger.exception(f"Ошибка во время инференса: {e}")
        return {"error": str(e)}
