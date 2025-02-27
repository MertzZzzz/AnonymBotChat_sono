import telebot
import logging
from telebot import types

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class AnonymousChatBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.queue = []  # Очередь пользователей, ищущих собеседника
        self.pairs = {}  # Словарь для хранения пар пользователей

        # Регистрация обработчиков команд
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['search'])(self.search)
        self.bot.message_handler(commands=['stop'])(self.stop)
        self.bot.message_handler(commands=['next'])(self.search)
        self.bot.message_handler(commands=['cancel'])(self.cancel)
        self.bot.message_handler(func=lambda message: True)(self.handle_message)

    def start(self, message):
        user_id = message.from_user.id
        self.bot.send_message(user_id, 'Добро пожаловать в анонимный чат! Нажми /search чтобы начать поиск собеседника.')

    def search(self, message):
        user_id = message.from_user.id

        if user_id in self.pairs:
            self.bot.send_message(user_id, 'Вы уже в чате. Нажми /stop чтобы закончить диалог.')
            return

        if user_id in self.queue:
            self.bot.send_message(user_id, 'Вы уже в очереди. Пожалуйста, подождите.')
            return

        self.queue.append(user_id)
        self.bot.send_message(user_id, 'Ищем собеседника...')

        if len(self.queue) >= 2:
            user1 = self.queue.pop(0)
            user2 = self.queue.pop(0)
            self.pairs[user1] = user2
            self.pairs[user2] = user1

            self.bot.send_message(user1, 'Собеседник найден! Начинайте общение.')
            self.bot.send_message(user2, 'Собеседник найден! Начинайте общение.')

    def cancel(self, message):
        user_id = message.from_user.id

        if user_id in self.queue:
            self.queue.remove(user_id)
            self.bot.send_message(user_id, 'Поиск отменен. Вы больше не в очереди.')
        elif user_id in self.pairs:
            self.bot.send_message(user_id, 'Вы уже в чате. Нажми /stop чтобы выйти.')
        else:
            self.bot.send_message(user_id, 'Вы не в очереди поиска.')

    def handle_message(self, message):
        user_id = message.from_user.id

        if user_id in self.pairs:
            partner_id = self.pairs[user_id]
            self.bot.send_message(partner_id, message.text)
        else:
            self.bot.send_message(user_id, 'Вы не в чате. Нажмите /search чтобы найти собеседника.')

    def stop(self, message):
        user_id = message.from_user.id

        if user_id in self.pairs:
            partner_id = self.pairs[user_id]
            del self.pairs[user_id]
            del self.pairs[partner_id]

            self.bot.send_message(user_id, 'Вы вышли из чата.')
            self.bot.send_message(partner_id, 'Собеседник покинул чат.')
        else:
            self.bot.send_message(user_id, 'Вы не в чате.')

    def run(self):
        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    # Вставь сюда токен своего бота
    bot = AnonymousChatBot("7574326854:AAEMgD5qlf8Tg1ziTeXbYM0tRZvM5teFhV8")
    bot.run()