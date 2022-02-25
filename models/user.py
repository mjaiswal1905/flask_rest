import sqlite3


class UserModel:
    db = 'data/data.db'
    table = 'users'

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect(cls.db)
        cursor = connection.cursor()

        query_select = f"SELECT * FROM {cls.table} where username=?"
        cursor.execute(query_select, (username,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect(cls.db)
        cursor = connection.cursor()

        query_select = f"SELECT * FROM {cls.table} where id=?"
        cursor.execute(query_select, (_id,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()

        return user
