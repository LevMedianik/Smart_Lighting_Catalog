# ==============================================================
# ЭТАП 2. ПРЕДОБРАБОТКА ДАННЫХ
# ==============================================================
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# -------------------------
# 1) Загрузка данных
# -------------------------
def load_data(path: str = "data/training_dataset.csv") -> pd.DataFrame:
    """Загрузка основной выборки"""
    df = pd.read_csv(path)
    print(f"Загружено {len(df)} строк из {path}")
    return df


# -------------------------
# 2) Очистка и базовая проверка
# -------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет пропуски, проверяет дубликаты, выбросы"""
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.fillna(0)
    # Выбросы по цене и мощности (срез 1%)
    for col in ["цена_₽", "мощность_вт", "световой_поток_лм"]:
        low, high = df[col].quantile([0.01, 0.99])
        df[col] = np.clip(df[col], low, high)
    return df


# -------------------------
# 3) Разделение признаков и таргета
# -------------------------
def split_features_target(df: pd.DataFrame):
    """Отделение целевой переменной"""
    y = df["оценка_пригодности"]
    X = df.drop(columns=["оценка_пригодности", "id_сценария", "id_продукта"])
    return X, y


# -------------------------
# 4) Формирование категориальных и числовых признаков
# -------------------------
def create_preprocessor(X: pd.DataFrame):
    """Создаёт пайплайн предобработки"""
    categorical_cols = [
        "тип_помещения", "тип_светильника", "бренд"
    ]
    numeric_cols = [
        "площадь_м2", "высота_м", "целевой_люкс", "бюджет_₽",
        "cri_min", "cct_предпочтение_k", "ip_min", "угол_раскрытия_град",
        "cri", "cct_k", "ip", "срок_службы_ч", "мощность_вт",
        "световой_поток_лм", "эффективность_лм_вт", "цена_₽", "количество_светильников"
    ]

    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    numeric_transformer = StandardScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, categorical_cols),
            ("num", numeric_transformer, numeric_cols)
        ]
    )
    return preprocessor


# -------------------------
# 5) Разделение на train/test
# -------------------------
def split_train_test(X, y, test_size: float = 0.2, random_state: int = 42):
    """Разделение на обучающую и тестовую выборки"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"Train: {X_train.shape}, Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test


# -------------------------
# 6) Основная функция
# -------------------------
def run_preprocessing():
    df = load_data()
    df = clean_data(df)
    X, y = split_features_target(df)

    preprocessor = create_preprocessor(X)
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    # Fit + Transform
    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)

    # Сохранение препроцессора
    joblib.dump(preprocessor, "ml/preprocessor.pkl")
    print("Препроцессор сохранён в ml/preprocessor.pkl")

    # Сохранение матриц
    np.savez_compressed("data/train_test_ready.npz",
                        X_train=X_train_prep,
                        X_test=X_test_prep,
                        y_train=y_train,
                        y_test=y_test)
    print("Предобработка завершена. Данные сохранены в /data.")

    return X_train_prep, X_test_prep, y_train, y_test


if __name__ == "__main__":
    run_preprocessing()