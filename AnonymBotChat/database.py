import sqlite3

class Database:
    @staticmethod
    def init_db():
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY,
                USERNAME TEXT,
                GENDER TEXT
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()

class ProfileDB(Database):
    @staticmethod
    def init_db():
        Database.init_db()

    @staticmethod
    def create_user(user_id, username):
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO users (ID, USERNAME) VALUES (?, ?)', (user_id, username))
        conn.commit()
        conn.close()

    @staticmethod
    def set_gender(user_id, gender):
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('UPDATE users SET GENDER = ? WHERE ID = ?', (gender, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_gender(user_id):
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT GENDER FROM users WHERE ID = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

class AdminPanel:
    @staticmethod
    def users_list():
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()
        cur.execute('SELECT ID, USERNAME, GENDER FROM users')
        userlist = cur.fetchall()
        cur.close()
        conn.close()
        return userlist