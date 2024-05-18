# Используем минималистичный базовый образ
FROM python:3.12.2-alpine

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
# Обновляем и устанавливаем необходимые пакеты для сборки и установки зависимостей
RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    # Удаляем временные файлы и кеши после установки пакетов
    apk del .build-deps

# Копируем все файлы из текущей директории в рабочую директорию контейнера
COPY . .

# Устанавливаем переменную среды для токена бота
# Замените YOUR_TELEGRAM_BOT_TOKEN на ваш реальный токен
ENV TELEGRAM_BOT_TOKEN="<token>"

# Определяем команду для запуска бота
CMD ["python", "bot.py"]
