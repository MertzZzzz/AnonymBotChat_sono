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