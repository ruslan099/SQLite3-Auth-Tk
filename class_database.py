import sqlite3

class Db:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def check_valid(self, log, pwd):
        with self.con:
            res = self.cur.execute("SELECT * FROM Users WHERE Login=? AND Password=?;",(log, pwd)).fetchall()
            return res
    
    def close_connection(self):
        self.con.close()