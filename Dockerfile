# ==============================================================
# Dockerfile — Smart AI Lighting Catalog
# Backend (FastAPI) + Frontend (StaticFiles)
# ==============================================================

# Базовый образ
FROM python:3.12-slim

# Установка рабочей директории
WORKDIR /app

# Зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Проект
COPY . .
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
