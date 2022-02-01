import sqlite3

class Db:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                First_name TEXT,
                Last_name TEXT,
                Email TEXT,
                Login TEXT UNIQUE,
                Password TEXT NOT NULL);
                """)

    def check_valid(self, log, pwd):
        """Проверка на валидность"""
        with self.con:
            res = self.cur.execute("SELECT * FROM users WHERE Login=? AND Password=?;",(log, pwd)).fetchall()
            return res

    def add_to_db(self, fname, sname, email, login, pwd):
        """Добавление в БД при регистрации"""
        with self.con:
            self.cur.execute("""INSERT INTO users (First_name, Last_name, Email, Login, Password)
                    VALUES (?, ?, ?, ?, ?);
                    """,(fname, sname, email, login, pwd))

    def delete_account(self, id):
        """Удаление аккаунта"""
        with self.con:
            self.cur.execute("DELETE FROM users WHERE id=?;", (id,))
    
    def close_connection(self):
        self.con.close()