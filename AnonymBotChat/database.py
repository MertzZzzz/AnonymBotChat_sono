import sqlite3

class Database():
    @staticmethod
    def init_db():
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY,
                USERNAME TEXT
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()

class ProfileDB(Database):
    @staticmethod
    def init_db():
        Database.init_db()
    def Create_user(user_id,username):
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (ID, USERNAME) VALUES (?, ?)', (user_id, username))
        conn.commit()
        conn.close()

class AdminPanel():
    def users_list():
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()
        cur.execute('SELECT ID, USERNAME FROM users')
        userlist = cur.fetchall()
        cur.close()
        conn.close()
        return userlist
