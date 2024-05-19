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

# Словарь для хранения информации о пользователях (chat_id, username, имя)
user_info = {}


# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    username = user.username
    name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name

    user_info[chat_id] = {
        "username": username,
        "name": name
    }
    
    update.message.reply_text(f'игра началась')


# Обработка всех текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    username = user.username
    name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name

    user_info[chat_id] = {
        "username": username,
        "name": name
    }
    
    last_active[chat_id] = datetime.now()


# Функция для проверки неактивных пользователей
def check_inactive_users(context: CallbackContext) -> None:
    now = datetime.now()
    for chat_id, last_time in last_active.items():
        timeout_sec = os.getenv("TIMEOUT_SEC") if os.getenv("TIMEOUT_SEC") is not None else 86400
        if now - last_time > timedelta(seconds=timeout_sec):
            user_data = user_info.get(chat_id)
            if user_data:
                username = user_data.get("username")
                name = user_data.get("name")
                try:
                    if username:
                        text = f"<a href='tg://user?id={chat_id}'>@{username}</a> пидарас"
                    else:
                        text = f"{name} пидарас!"
                    
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=text,
                        parse_mode=ParseMode.HTML
                    )
                    last_active[chat_id] = now  # Обновляем время последней активности
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
    job_queue.run_repeating(check_inactive_users, interval=1, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
