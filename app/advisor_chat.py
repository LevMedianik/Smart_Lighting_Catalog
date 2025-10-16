# ==============================================================
# AI-советник (чат-интерфейс)
# Обрабатывает пользовательские запросы с использованием SpaCy
# для извлечения параметров помещения и вызова рекомендаций
# ==============================================================

from fastapi import APIRouter, HTTPException
from app.spacy_parser import parse_room_params_spacy
from app.recommend import recommend_luminaires as recommend
from app.advisor import generate_advice
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


# --------------------------------------------------------------
# Основная функция чат-интерфейса
# --------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str

@router.post("/chat/")
async def chat(request: ChatRequest):
    message = request.message  # ← достаём текст из тела JSON
    """
    Принимает текстовое сообщение пользователя,
    извлекает параметры помещения через SpaCy,
    вызывает recommend() и формирует совет через generate_advice().
    """
    try:
        logger.info("────────────────────────────────────────────")
        logger.info(f"📩 Получено сообщение от пользователя: {message}")

        # 🔹 1. Извлечение параметров помещения (SpaCy)
        parsed = parse_room_params_spacy(message)
        logger.info(f"🧩 Извлечённые параметры: {parsed}")

        # Проверка на корректность данных
        if not parsed or not isinstance(parsed, dict):
            raise ValueError("Парсер не вернул корректных данных.")

        # 🔹 2. Получение рекомендаций от ML-модуля
        rec_result = recommend(parsed)
        if not rec_result:
            logger.warning("⚠️ Рекомендации не найдены.")
            return {
                "user_query": message,
                "parsed_params": parsed,
                "summary": "Рекомендации не найдены. Попробуйте уточнить запрос.",
                "advice": "Проверьте, указаны ли площадь, высота и бюджет."
            }

        recommendations = rec_result.get("recommendations", [])
        summary = rec_result.get("summary", "")

        logger.info(f"✅ Успешно получены {len(recommendations)} рекомендаций.")

        # 🔹 3. Генерация текстового совета
        advice_text = generate_advice(recommendations, parsed)
        logger.info("💬 Советник успешно сгенерировал объяснение.")

        # 🔹 4. Формирование ответа
        result = {
            "user_query": message,
            "parsed_params": parsed,
            "summary": summary,
            "advice": advice_text
        }

        logger.info("🎯 Ответ успешно сформирован и возвращён пользователю.")
        logger.info("────────────────────────────────────────────")
        return result

    except Exception as e:
        logger.exception("❌ Ошибка в обработке чата:")
        raise HTTPException(status_code=500, detail=f"Ошибка советника: {e}")
