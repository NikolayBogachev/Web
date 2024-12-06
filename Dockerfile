# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY ./app /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Открываем порт для приложения
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
