import logging
import os
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime, timedelta

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Настраиваем логгер
logger = logging.getLogger(__name__)

# Словарь для хранения времени последнего сообщения пользователей
last_active = {}
chat_id = None


# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    global chat_id
    chat_id = update.message.chat_id
    update.message.reply_text(f'Бот запущен! Chat ID: {chat_id}')


# Обработка всех текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    last_active[user.id] = datetime.now()


# Функция для проверки неактивных пользователей
def check_inactive_users(context: CallbackContext) -> None:
    if chat_id is None:
        return  # Если chat_id еще не установлен, ничего не делаем

    now = datetime.now()
    for user_id, last_time in last_active.items():
        if now - last_time > timedelta(hours=24):
            try:
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"<a href='tg://user?id={user_id}'>@{user_id}</a> пидарас",
                    parse_mode=ParseMode.HTML
                )
                last_active[user_id] = now  # Обновляем время последней активности
            except Exception as e:
                logger.error(f"Error: {e}")


def main() -> None:
    # Получаем токен из переменной среды
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не установлен в переменных среды")
        return

    updater = Updater(token)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Периодическая проверка неактивных пользователей (каждый час)
    job_queue = updater.job_queue
    job_queue.run_repeating(check_inactive_users, interval=3600, first=0)

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
