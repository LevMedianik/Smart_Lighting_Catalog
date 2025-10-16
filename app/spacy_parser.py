# ==============================================================
# spacy_parser.py
# Универсальный парсер на SpaCy для извлечения параметров помещения.
# Работает с запросами вроде:
# "Подбери освещение для офиса 45 м², высота 3.2, бюджет 20000"
# ==============================================================

import re
import spacy

# -------------------------
# Инициализация SpaCy
# -------------------------
try:
    nlp = spacy.load("ru_core_news_sm")
except Exception as e:
    nlp = None
    print("⚠️ SpaCy model not loaded:", e)


# -------------------------
# Словарь помещений (согласованный с датасетом)
# -------------------------
ROOM_TYPES = {
    "офис": "офисное помещение",
    "кухня": "кухня",
    "гостиная": "гостиная",
    "спальня": "спальня",
    "зал": "торговый зал",
    "цех": "цех",
    "ресторан": "ресторан",
    "кафе": "кафе",
    "склад": "склад",
    "аудитория": "аудитория",
    "коридор": "коридор",
    "вестибюль": "вестибюль",
    "санузел": "санузел",
    "ванная": "ванная",
    "прихожая": "прихожая",
    "лаборатория": "лаборатория",
    "магазин": "магазин"
}


# -------------------------
# Основная функция парсера
# -------------------------
def parse_room_params_spacy(text: str):
    text_clean = text.lower().replace(",", ".")
    room_type = None

    # --- 1. Определение типа помещения через SpaCy ---
    if nlp:
        doc = nlp(text_clean)
        for token in doc:
            lemma = token.lemma_
            if lemma in ROOM_TYPES:
                room_type = ROOM_TYPES[lemma]
                break

    if not room_type:
        room_type = "офисное помещение"

    # --- 2. Площадь ---
    area = None
    area_patterns = [
        r"(\d+(?:\.\d+)?)\s*(?:м2|м²|кв\.|квадратн|метров|метра)",
        r"(?:площад[ьяи]|квадратура)\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*квадрат"
    ]
    for pattern in area_patterns:
        match = re.search(pattern, text_clean)
        if match:
            area = float(match.group(1))
            break

    # --- 3. Высота ---
    height = None
    height_patterns = [
        r"высот[аы]\s*(?:потолка|потолков|)\s*(\d+(?:[.,]\d+)?)",  # высота 2.8, высота потолка 3.1
        r"потол(?:ок|ка|ки)?[^\d]*(\d+(?:[.,]\d+)?)",             # потолки 3, потолок 2.7
        r"(\d+(?:[.,]\d+)?)\s*(?:м|метр[аов]*)\s*(?:высот[аы]|потолк[аи]*)"  # 2.8 м высота
    ]

    for pattern in height_patterns:
        match = re.search(pattern, text_clean)
        if match:
            try:
                # Заменяем запятую на точку и конвертируем в float
                height = float(match.group(1).replace(",", "."))
                break
            except (ValueError, IndexError):
                continue

    # Если не найдено — стандартная высота
    height = height if height else 3.0


    # --- 4. Бюджет ---
    budget = None
    budget_patterns = [
        r"бюджет[а-я ]*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*(?:руб|₽|тыс)"
    ]
    for pattern in budget_patterns:
        match = re.search(pattern, text_clean)
        if match:
            try:
                budget = int(float(match.group(1)))
                break
            except ValueError:
                continue

    # --- 5. Числовые значения ---
    def to_float(value, default):
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    area = to_float(area, 20.0)
    height = to_float(height, 3.0)
    budget = int(budget) if budget else 100000

    # --- 6. Возврат параметров ---
    return {
        "тип_помещения": room_type,
        "площадь_м2": area,
        "высота_м": height,
        "целевой_люкс": 400,
        "cri_min": 80,
        "cct_предпочтение_k": 4000,
        "ip_min": 40,
        "бюджет_₽": budget
    }


# -------------------------
# Тест при прямом запуске
# -------------------------
if __name__ == "__main__":
    samples = [
        "Подбери светильники для офиса площадью 45 м2, высота потолка 3.2 м, бюджет 20000 рублей",
        "Хочу осветить кухню 25 квадратных метров с потолком 2.8 метра и бюджетом 15000",
        "Нужно освещение для торгового зала, площадь 100 м², высота 4 метра, бюджет 50000",
        "Классная гостиная, квадратура 30, потолки 3 метра"
    ]
    for text in samples:
        print(f"\n🗣️ {text}")
        print(parse_room_params_spacy(text))
