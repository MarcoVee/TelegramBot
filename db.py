import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO  `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        self.cursor.execute("INSERT INTO  'records' ('users_id', 'operation', 'value') VALUES (?, ?, ? ",
                            (self.get_user_id(user_id),
                             operation == '+',
                             value))
        return self.conn.commit()

    def get_records(self, user_id, within="all"):
        if within == "day":
            ressult = self.cursor.execute(
                "SELECT * FROM 'records' WHERE 'users_id' = ? AND 'date' BETWEEN datetime('now', 'start day' AND "
                "datetime('now', 'localtime') ORDER BY 'date'",
                (self.get_user_id(user_id),))
        elif within == "week":
            ressult = self.cursor.execute(
                "SELECT * FROM 'records' WHERE 'users_id' = ? AND 'date' BETWEEN datetime('now', '-6 days' AND "
                "datetime('now', 'localtime') ORDER BY 'date'",
                (self.get_user_id(user_id),))
        elif within == "month":
            ressult = self.cursor.execute(
                "SELECT * FROM 'records' WHERE 'users_id' = ? AND 'date' BETWEEN datetime('now', 'start of month' AND "
                "datetime('now', 'localtime') ORDER BY 'date'",
                (self.get_user_id(user_id),))
        else:
            ressult = self.cursor.execute(
                "SELECT * FROM 'records' WHERE 'users_id' = ?  ORDER BY 'date'",
                (self.get_user_id(user_id),))

        return ressult.fetchall()

    def close(self):
        self.conn.close()
