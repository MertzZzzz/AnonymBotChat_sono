from config import BotSettings
import telebot
import logging
from telebot import types
from database import Database
from handlers.message_handler import MessageHandler
from handlers.command_handler import CommandHandler
from utils.user_manager import UserManager

Settings = BotSettings
token = Settings.token

db = Database
db.init_db()

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class AnonymousChatBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.user_manager = UserManager()
        self.message_handler = MessageHandler(self.bot, self.user_manager)
        self.command_handler = CommandHandler(self.bot, self.user_manager)

        # Регистрация обработчиков команд
        self.bot.message_handler(commands=['start'])(self.command_handler.start)
        self.bot.message_handler(commands=['search'])(self.command_handler.search)
        self.bot.message_handler(commands=['stop'])(self.command_handler.stop)
        self.bot.message_handler(commands=['next'])(self.command_handler.search)
        self.bot.message_handler(commands=['cancel'])(self.command_handler.cancel)
        self.bot.message_handler(commands=['link'])(self.command_handler.link)  # Добавлен обработчик команды /link
        self.bot.message_handler(func=lambda message: True)(self.message_handler.handle_message)

    def run(self):
        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    bot = AnonymousChatBot(token)
    bot.run()