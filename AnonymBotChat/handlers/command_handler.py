from database import ProfileDB

db = ProfileDB
class CommandHandler:
    def __init__(self, bot, user_manager):
        self.bot = bot
        self.user_manager = user_manager

    def start(self, message):
        user_id = message.from_user.id
        self.bot.send_message(user_id, 'Добро пожаловать в анонимный чат СОНО!\n/search чтобы начать поиск собеседника\n/help чтобы ознакомиться с командами бота')
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
            self.bot.send_message(user_id, 'Вы вышли из чата.\nВведите /search чтобы найти нового собеседника')
            self.bot.send_message(partner_id, 'Собеседник закончил чат.\nВведите /search чтобы найти нового собеседника')
        else:
            self.bot.send_message(user_id, 'Вы не в чате. Нажмите /search чтобы найти собеседника.')

    def link(self, message):
        user_id = message.from_user.id
        partner_id = self.user_manager.get_partner(user_id)

        if not partner_id:
            self.bot.send_message(user_id, 'Вы не в чате. Нажмите /search чтобы найти собеседника.')
            return

        username = message.from_user.username
        if username:
            profile_link = f"[Ссылка](https://t.me/{username})"
            self.bot.send_message(user_id, f"{profile_link} на ваш профиль отправлена собеседнику",parse_mode='MarkdownV2')
            self.bot.send_message(partner_id, f"{profile_link} на профиль вашего собеседника",parse_mode='MarkdownV2')
        else:
            self.bot.send_message(user_id, "У вас не установлен username. Пожалуйста, установите username в настройках Telegram, чтобы использовать эту команду.")
    def help(self,message):
        user_id = message.from_user.id
        help_str='/search - найти собеседника\n/cancel - отменить поиск собеседника\n/stop - остановить диалог с собеседником\n/link - отправить ссылку на ваш профиль собеседнику'
        self.bot.send_message(user_id,help_str)