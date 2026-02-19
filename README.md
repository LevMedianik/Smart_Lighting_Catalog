# EN: 💡 Smart AI Lighting Catalog
Intelligent Lighting Recommendation System

---

### 📘 Project Overview

Smart AI Lighting Catalog is a web-based application that combines a structured lighting product catalog with an intelligent recommendation engine.  
The system analyzes user input (e.g., “office 45 m², ceiling height 3.2 m, budget 20000”) and, based on a trained ML model, suggests suitable lighting fixtures along with an explanation of the selection.  
The project also includes an AI advisor module powered by NLP (SpaCy), capable of understanding natural language input and providing recommendations through an interactive chat interface.  

---

### ⚙️ Core Features

**💡 AI-powered lighting recommendation** – calculates optimal lighting parameters based on room size, height, and budget.
**💬 AI advisor (chat interface)** – natural language processing and interactive advisory responses.
**🧩 Recommendation engine** – CatBoost model with a serialized preprocessing pipeline.
**🌐 Interactive frontend** – responsive UI with dynamic product cards.
**🐳 Containerized deployment** – Docker-based setup with deployment on Render.

---

### 🧰 Tech Stack

**Backend:** Python, FastAPI, Uvicorn  
**Frontend:** HTML5, TailwindCSS, JavaScript  
**NLP: SpaCy** (ru_core_news_sm)  
**ML / Data:** CatBoost, scikit-learn, pandas, numpy  
**Validation & Schemas:** Pydantic  
**Containerization:** Docker, docker-compose  
**Deployment:** Render.com  
**Other:** Jinja2, logging, dotenv  

---

### 🧩 Project Architecture
```
Smart_Lighting_Catalog/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── recommend.py         # ML inference & fixture recommendation
│   ├── advisor.py           # Advisory text generation
│   ├── advisor_chat.py      # Chat-based AI advisor
│   ├── spacy_parser.py      # NLP parameter extraction
│   ├── schemas.py           # Pydantic schemas
│   └── config.py            # Configuration
│
├── frontend/
│   ├── index.html
│   ├── assets/
│   │   ├── style.css
│   │   ├── script.js
│   │   ├── adviser_bg.png
│   │   ├── advisor-icon.png
│   │   └── other assets
│
├── ml/
│   ├── best_model.pkl
│   ├── preprocessor.pkl
│   ├── generate_data.py
│   └── train_models.py
│
├── data/
│   ├── fixtures.csv
│   ├── rooms.csv
│   ├── train_test_ready.npz
│   └── training_dataset.csv
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
---

### 🚀 Running the Project

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the FastAPI backend:
```
uvicorn app.main:app --reload
```

3. Frontend is available at:
```
http://127.0.0.1:5500/frontend/index.html
```

### For containerized deployment:
```
docker-compose up --build
```

The application will be accessible at:
```
http://localhost:8000
```
---

### 🔹 Environment Variables (.env.example)
```
MODEL_PATH=ml/best_model.pkl
PREPROCESSOR_PATH=ml/preprocessor.pkl
FIXTURES_PATH=data/fixtures.csv
TOP_N=3

HOST=0.0.0.0
PORT=8000
DEBUG=True

ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,https://smart-lighting-catalog.onrender.com
```
---

### 🌍 Deployment

The application is deployed on Render.com:
```
https://smart-lighting-catalog.onrender.com
```

---

### 🧠 Implementation Highlights

Modular architecture separating ML, backend, and frontend layers  
NLP-based parameter extraction using SpaCy  
Combined FastAPI + frontend setup within a single container  
Flexible recommendation logic with explainability  
Scalable design allowing new room types and fixture categories  
Russian-language AI advisor with flexible natural input handling  

---

### 💬 Example Interaction

User:
Lighting for a kitchen, 25 square meters, 2.8 m ceiling, budget 15000  

AI Advisor:  
For a “kitchen” with recommended illumination of 400 lux, the following fixtures are suggested:  
• IEK IEK-LN37082 — ceiling linear, ≈433 lux, 7902 ₽  
• Gauss NK82085 — wall-mounted, ≈459 lux, 6486 ₽  
• Uniel NK99803 — wall-mounted, ≈441 lux, 16472 ₽  

All options provide comfortable lighting levels and fit within the specified budget constraints.  

---

### 🏁 Conclusion

Smart AI Lighting Catalog demonstrates the integrated use of:  
Machine learning  
Natural language processing  
Backend API architecture  
Web-based user interfaces  
The project is production-ready and extensible, supporting future enhancements such as advanced neural models, expanded room categories, and additional decision-support workflows.  

---

© 2025 — Smart Lighting Solutions Catalog  

## Note  

The AI advisor currently supports a generalized set of room types including: office, kitchen, living room, bedroom, retail space, workshop, restaurant, café, warehouse, classroom, corridor, lobby, restroom, bathroom, hallway, laboratory, and store.  

---

# RU: 💡 Smart AI Lighting Catalog 
Интеллектуальная система подбора осветительных решений

---

## 📘 Описание проекта

Smart AI Lighting Catalog — это веб-приложение, объединяющее каталог светильников с интеллектуальной системой подбора освещения.  
Сервис анализирует ввод пользователя (например: «офис 45 м², высота 3.2 м, бюджет 20000») и на основе обученной ML-модели предлагает подходящие светильники с объяснением выбора.  

Проект также включает AI-советника, который с помощью NLP (SpaCy) понимает естественный язык и выдает рекомендации в интерактивном чат-интерфейсе.  

---

## ⚙️ Основной функционал

💡 AI-подбор освещения — расчёт оптимальных параметров по площади, высоте и бюджету.  
💬 AI-советник (чат) — обработка естественного языка и генерация советов.  
🧩 Модуль рекомендаций — CatBoost-модель с сохранённым препроцессором.  
🌐 Интерактивный фронтенд — адаптивный интерфейс с динамическими карточками.  
🐳 Контейнеризация и деплой — запуск через Docker и публикация на Render.  

---

## 🧰 Используемый стек

**Backend:** Python, FastAPI, Uvicorn  
**Frontend:** HTML5, TailwindCSS, JavaScript  
**NLP:** SpaCy (ru_core_news_sm)  
**ML / Data:** CatBoost, scikit-learn, pandas, numpy  
**Схемы и валидация:** Pydantic  
**Контейнеризация:** Docker, docker-compose  
**Деплой:** Render.com  
**Прочее:** Jinja2, Logging, dotenv  

---

## 🧩 Архитектура проекта
```
Smart_Lighting_Catalog/  
├── app/  
│  ├── main.py — основное FastAPI-приложение  
│  ├── recommend.py — ML-инференс и подбор светильников  
│  ├── advisor.py — генерация текстовых советов  
│  ├── advisor_chat.py — AI-советник (чат)  
│  ├── spacy_parser.py — NLP-парсер (извлечение параметров)  
│  ├── schemas.py — Pydantic-схемы  
│  └── config.py — настройки  
│  
├── frontend/  
│  ├── index.html  
│  ├── assets/  
│  │  ├── style.css  
│  │  ├── script.js  
│  │  ├── adviser_bg.png  
│  │  ├── advisor-icon.png  
│  │  └── прочие ресурсы  
│  
├── ml/  
│  ├── best_model.pkl  
│  ├── preprocessor.pkl  
│  ├── generate_data.py  
│  └── train_models.py  
│  
├── data/  
│  ├── fixtures.csv
│  ├── rooms.csv 
│  ├── train_test_ready.npz
│  └── training_dataset.csv (Данные для обучения модели)
│  
├── Dockerfile  
├── docker-compose.yml  
├── requirements.txt  
└── README.md  
```
---
### 🧠 Логика модели и системы рекомендаций
Система рекомендаций построена на модели машинного обучения (CatBoost), обученной на структурированном датасете параметров помещений и конфигураций освещения.  

Входные признаки включают:

- **Тип помещения** (категориальный признак)
- **Площадь** (м²)
- **Высоту потолка** (м)
- **Бюджетные ограничения**
- **Требуемый уровень освещённости** (lux)

Пайплайн предобработки (совместимый со scikit-learn) выполняет кодирование категорий, масштабирование и детерминированные преобразования признаков.  

Модель прогнозирует:  

Оптимальную категорию светильника  
Ожидаемый уровень освещённости  
Соответствие бюджетным ограничениям  
Стратегия рекомендаций  

Система объединяет:

**Модельное ранжирование** – прогноз оптимальных параметров освещения.  
**Фильтрацию каталога** – подбор светильников по типу и цене.  
**Top-N выборку** – вывод наиболее подходящих вариантов (TOP_N настраивается).  
**Вывод** – формирование объяснения на основе lux и ограничений.  

Гибридный подход обеспечивает:

Практическую применимость  
Интерпретируемость  
Предсказуемость поведения  
Масштабируемость при обновлении модели  

Модель и пайплайн сериализуются и загружаются при запуске сервиса для обеспечения низкой задержки инференса.

---

## 🚀 Развёртывание проекта

Установка зависимостей выполняется через файл requirements.txt.  
Сервер FastAPI запускается командой uvicorn app.main:app --reload.  

Frontend доступен по адресу  
http://127.0.0.1:5500/frontend/index.html  

Для контейнерного запуска используется docker-compose up --build.  
Приложение открывается по адресу http://localhost:8000  

---

## 🔹 Переменные окружения (.env.example)
```
MODEL_PATH=ml/best_model.pkl  
PREPROCESSOR_PATH=ml/preprocessor.pkl  
FIXTURES_PATH=data/fixtures.csv  
TOP_N=3  

HOST=0.0.0.0  
PORT=8000  
DEBUG=True  

ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,https://smart-lighting-catalog.onrender.com  
```
---

## 🌍 Деплой

Проект развёрнут на Render.com  
https://smart-lighting-catalog.onrender.com  

---

## 🧩 Особенности реализации

• Модульная структура (app, ml, frontend)  
• Обработка естественного языка через SpaCy  
• Совместная работа FastAPI и фронтенда в одном контейнере  
• Гибкая система рекомендаций и объяснений  
• Возможность расширения модели и добавления новых типов помещений  
• AI-советник на русском языке с поддержкой вариативного ввода  

---

## 💬 Пример взаимодействия

Пользователь:  
Освещение для кухни 25 квадратных метров, потолки 2.8 м, бюджет 15000  

AI-советник:  
Для помещения «кухня» с нормой освещённости 400 лк рекомендованы:  
• IEK IEK-LN37082 — потолочный линейный, ≈433 лк, 7902 ₽  
• Gauss NK82085 — настенный накладной, ≈459 лк, 6486 ₽  
• Uniel NK99803 — настенный накладной, ≈441 лк, 16472 ₽  
Все варианты обеспечивают комфортное восприятие света и укладываются в заданный бюджет.  

---

## 🏁 Итоги

Smart AI Lighting Catalog демонстрирует комплексную интеграцию  
машинного обучения, обработки естественного языка и веб-технологий  
в рамках единого инженерного решения.  

Проект полностью готов к использованию и дальнейшему развитию. Вы можете расширить базы помещений до внедрения нейросетевых моделей и новых сценариев взаимодействия.  

---

© 2025 — Умный каталог световых решений

## Примечание

AI-советник работает пока с ограниченным и обобщенным набором помещений: офис, кухня, гостиная, спальня, торговый зал, цех, ресторан, кафе, склад, аудитория, коридор, вестибюль, санузел, ванная, прихожая, лаборатория, магазин и с чисто синтетическим набором данных.
