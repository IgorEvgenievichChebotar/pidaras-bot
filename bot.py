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

# Словарь для хранения времени последнего сообщения и имен пользователей
last_active = {}

# Словарь для хранения ID чатов по имени пользователя
usernames_to_chat_ids = {}


# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    usernames_to_chat_ids[user.username] = update.message.chat_id
    update.message.reply_text(f'Игра началась')


# Обработка всех текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if user.username:
        usernames_to_chat_ids[user.username] = update.message.chat_id
    last_active[user.username] = datetime.now()


# Функция для проверки неактивных пользователей
def check_inactive_users(context: CallbackContext) -> None:
    now = datetime.now()
    for username, last_time in last_active.items():
        if now - last_time > timedelta(hours=24):
            chat_id = usernames_to_chat_ids.get(username)
            if chat_id:
                try:
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=f"<a href='tg://user?id={username}'>@{username}</a> пидарас",
                        parse_mode=ParseMode.HTML
                    )
                    last_active[username] = now  # Обновляем время последней активности
                except Exception as e:
                    logger.error(f"Error: {e}")


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не установлен в переменных среды")
        return

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    job_queue = updater.job_queue
    job_queue.run_repeating(check_inactive_users, interval=60, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
