# Используем официальный образ Python
FROM python:3.12.2-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущей директории в рабочую директорию контейнера
COPY . .

# Устанавливаем переменную среды для токена бота
ENV TELEGRAM_BOT_TOKEN="<token>"

# Определяем команду для запуска бота
CMD ["python", "bot.py"]
