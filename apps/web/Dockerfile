FROM python:3.11-slim

WORKDIR /app

# Копируем все файлы фронтенда
COPY . .

# Открываем порт 8000 (внутри контейнера)
EXPOSE 8000

# Запускаем простой HTTP-сервер
CMD ["python", "-m", "http.server", "8000"]