class UserManager:
    def __init__(self):
        self.queue = []  # Очередь пользователей, ищущих собеседника
        self.pairs = {}  # Словарь для хранения пар пользователей
        self.message_texts = {}  # Словарь для хранения текстов сообщений

    def add_user_to_queue(self, user_id, preferred_gender=None):
        """
        Добавляет пользователя в очередь поиска.
        :param user_id: ID пользователя
        :param preferred_gender: Предпочтительный пол собеседника (опционально)
        :return: True, если пользователь успешно добавлен в очередь, иначе False
        """
        if user_id in self.pairs:
            return False
        if user_id in [user['user_id'] for user in self.queue]:
            return False
        self.queue.append({'user_id': user_id, 'preferred_gender': preferred_gender})
        return True

    def remove_user_from_queue(self, user_id):
        """
        Удаляет пользователя из очереди поиска.
        :param user_id: ID пользователя
        :return: True, если пользователь был в очереди и удален, иначе False
        """
        self.queue = [user for user in self.queue if user['user_id'] != user_id]
        return True

    def create_pair(self, user1, user2):
        """
        Создает пару между двумя пользователями.
        :param user1: Данные первого пользователя (словарь с user_id и preferred_gender)
        :param user2: Данные второго пользователя (словарь с user_id и preferred_gender)
        """
        self.pairs[user1['user_id']] = user2['user_id']
        self.pairs[user2['user_id']] = user1['user_id']

    def remove_pair(self, user_id):
        """
        Удаляет пару пользователей.
        :param user_id: ID пользователя
        :return: ID партнера, если пара была удалена, иначе None
        """
        if user_id in self.pairs:
            partner_id = self.pairs[user_id]
            del self.pairs[user_id]
            del self.pairs[partner_id]
            return partner_id
        return None

    def get_partner(self, user_id):
        """
        Возвращает ID партнера пользователя.
        :param user_id: ID пользователя
        :return: ID партнера, если он есть, иначе None
        """
        return self.pairs.get(user_id)

    def save_message_text(self, user_id, message_id, text):
        """
        Сохраняет текст сообщения для корректного реплая.
        :param user_id: ID пользователя
        :param message_id: ID сообщения
        :param text: Текст сообщения
        """
        if user_id not in self.message_texts:
            self.message_texts[user_id] = {}
        self.message_texts[user_id][message_id] = text

    def get_message_text(self, user_id, message_id):
        """
        Возвращает текст сообщения для реплая.
        :param user_id: ID пользователя
        :param message_id: ID сообщения
        :return: Текст сообщения, если оно найдено, иначе None
        """
        if user_id in self.message_texts and message_id in self.message_texts[user_id]:
            return self.message_texts[user_id][message_id]
        return None