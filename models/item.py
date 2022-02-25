import sqlite3


class ItemModel:
    db = 'data/data.db'
    table = 'items'

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    def insert(self):
        connection = sqlite3.connect(ItemModel.db)
        cursor = connection.cursor()

        query_select = f"INSERT INTO {ItemModel.table} VALUES (?, ?)"
        cursor.execute(query_select, (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect(ItemModel.db)
        cursor = connection.cursor()

        query_select = f"UPDATE {ItemModel.table} SET price=? WHERE name=?"
        cursor.execute(query_select, (self.price, self.name))
        connection.commit()
        connection.close()

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(ItemModel.db)
        cursor = connection.cursor()

        query_select = f"SELECT * FROM {ItemModel.table} where name=?"
        cursor.execute(query_select, (name,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return cls(*row)
        else:
            return None