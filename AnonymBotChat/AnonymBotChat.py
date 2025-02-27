from config import BotSettings
import telebot
import logging
from telebot import types
from database import ProfileDB
from handlers.Message_handler import MessageHandler

Settings = BotSettings
token = Settings.token

db = ProfileDB
db.init_db()

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self):
        self.queue = []  # Очередь пользователей, ищущих собеседника
        self.pairs = {}  # Словарь для хранения пар пользователей

    def add_user_to_queue(self, user_id):
        if user_id in self.pairs:
            return False
        if user_id in self.queue:
            return False
        self.queue.append(user_id)
        return True

    def remove_user_from_queue(self, user_id):
        if user_id in self.queue:
            self.queue.remove(user_id)
            return True
        return False

    def create_pair(self, user1, user2):
        self.pairs[user1] = user2
        self.pairs[user2] = user1

    def remove_pair(self, user_id):
        if user_id in self.pairs:
            partner_id = self.pairs[user_id]
            del self.pairs[user_id]
            del self.pairs[partner_id]
            return partner_id
        return None

    def get_partner(self, user_id):
        return self.pairs.get(user_id)



class CommandHandler:
    def __init__(self, bot, user_manager):
        self.bot = bot
        self.user_manager = user_manager

    def start(self, message):
        user_id = message.from_user.id
        self.bot.send_message(user_id, 'Добро пожаловать в анонимный чат! Нажми /search чтобы начать поиск собеседника.')
        db.Create_user(user_id, message.from_user.username)

    def search(self, message):
        user_id = message.from_user.id

        if not self.user_manager.add_user_to_queue(user_id):
            self.bot.send_message(user_id, 'Вы уже в чате или в очереди.')
            return

        self.bot.send_message(user_id, 'Ищем собеседника...')

        if len(self.user_manager.queue) >= 2:
            user1 = self.user_manager.queue.pop(0)
            user2 = self.user_manager.queue.pop(0)
            self.user_manager.create_pair(user1, user2)
            self.bot.send_message(user1, 'Собеседник найден! Начинайте общение.')
            self.bot.send_message(user2, 'Собеседник найден! Начинайте общение.')

    def cancel(self, message):
        user_id = message.from_user.id

        if self.user_manager.remove_user_from_queue(user_id):
            self.bot.send_message(user_id, 'Поиск отменен. Вы больше не в очереди.')
        elif user_id in self.user_manager.pairs:
            self.bot.send_message(user_id, 'Вы уже в чате. Нажми /stop чтобы выйти.')
        else:
            self.bot.send_message(user_id, 'Вы не в очереди поиска.')

    def stop(self, message):
        user_id = message.from_user.id
        partner_id = self.user_manager.remove_pair(user_id)
        if partner_id:
            self.bot.send_message(user_id, 'Вы вышли из чата.')
            self.bot.send_message(partner_id, 'Собеседник покинул чат.')
        else:
            self.bot.send_message(user_id, 'Вы не в чате.')

    def link(self, message):
        user_id = message.from_user.id
        partner_id = self.user_manager.get_partner(user_id)

        if not partner_id:
            self.bot.send_message(user_id, 'Вы не в чате. Нажмите /search чтобы найти собеседника.')
            return

        username = message.from_user.username
        if username:
            profile_link = f"https://t.me/{username}"
            self.bot.send_message(user_id, f"Ссылка на ваш профиль отправлена собеседнику")
            self.bot.send_message(partner_id, f"Ссылка на профиль вашего собеседника: {profile_link}")
        else:
            self.bot.send_message(user_id, "У вас не установлен username. Пожалуйста, установите username в настройках Telegram, чтобы использовать эту команду.")

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