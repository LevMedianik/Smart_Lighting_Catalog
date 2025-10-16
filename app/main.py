# ==============================================================
# Главный модуль FastAPI-приложения
# AI Lighting Recommender + AI-Советник + Frontend
# ==============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

from app.schemas import RoomInput
from app.recommend import recommend_luminaires as recommend
from app.advisor import generate_advice
from app.advisor_chat import router as chat_router

# --------------------------------------------------------------
# Настройка логгера
# --------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# --------------------------------------------------------------
# Инициализация приложения
# --------------------------------------------------------------
app = FastAPI(
    title="AI Lighting Recommender",
    version="1.0",
    description="Интеллектуальная система подбора светильников с объяснением выбора и веб-интерфейсом."
)

# --------------------------------------------------------------
# CORS (разрешаем запросы с фронтенда)
# --------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://smart-lighting.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------
# Подключаем роутер AI-советника (чат)
# --------------------------------------------------------------
app.include_router(
    chat_router,
    prefix="",
    tags=["AI-советник"],
)

# --------------------------------------------------------------
# Подключаем FRONTEND
# --------------------------------------------------------------
# Определяем путь до каталога frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

# Проверяем наличие каталога
if not os.path.exists(FRONTEND_DIR):
    logger.warning("⚠️ Каталог frontend не найден. Проверь путь перед деплоем.")
else:
    # Подключаем все статические файлы (CSS, JS, изображения)
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

    # Главная страница index.html
    @app.get("/", response_class=FileResponse)
    async def serve_index():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index_path)

# --------------------------------------------------------------
# Проверка состояния сервиса
# --------------------------------------------------------------
@app.get("/health")
def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}

# --------------------------------------------------------------
# Основной эндпоинт рекомендаций
# --------------------------------------------------------------
@app.post("/recommend")
def get_recommendations(room: RoomInput):
    """
    Принимает параметры помещения (RoomInput),
    вызывает модель рекомендаций и AI-советник для объяснения выбора.
    """
    try:
        # 🔹 Преобразуем входные данные
        room_dict = room.model_dump()
        logger.info(f"📥 Получен запрос: {room_dict}")

        # 🔹 Получаем рекомендации
        results = recommend(room_dict)
        if not results:
            raise ValueError("Рекомендации не получены.")

        # 🔹 Обработка структуры
        if isinstance(results, dict):
            recommendations, summary = [], ""
            if "recommendations" in results:
                if isinstance(results["recommendations"], list):
                    recommendations = results["recommendations"]
                    summary = results.get("summary", "")
                elif isinstance(results["recommendations"], dict):
                    recommendations = results["recommendations"].get("recommendations", [])
                    summary = results["recommendations"].get("summary", "")
        else:
            recommendations, summary = [], ""

        # 🔹 Генерация объяснения
        advice = generate_advice(recommendations, room_dict)

        logger.info("✅ Рекомендации и совет успешно сформированы.")
        return {
            "recommendations": recommendations,
            "summary": summary,
            "advice": advice
        }

    except Exception as e:
        logger.exception("❌ Ошибка во время инференса:")
        raise HTTPException(status_code=500, detail=f"Ошибка во время инференса: {e}")


# --------------------------------------------------------------
# Точка входа для локального запуска
# --------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
