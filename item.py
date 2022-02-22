import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    db = 'data/data.db'
    table = 'items'
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This cannot be blank!')

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return {'Item': item}, 200
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400

        data = Item.parser.parse_args()
        new_item = {
            'name': name,
            'price': data['price']
        }
        try:
            Item.insert(new_item)
        except:
            return {'message': 'Error during insert operation'}, 500

        return new_item, 201

    def delete(self, name):
        connection = sqlite3.connect(Item.db)
        cursor = connection.cursor()

        query_select = f"DELETE FROM {Item.table} where name=?"
        cursor.execute(query_select, (name,))
        connection.commit()
        connection.close()
        return {'message': f'Item {name} is deleted'}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message': 'Error during insert operation'}, 500
        else:
            try:
                Item.update(data)
            except:
                return {'message': 'Error during update operation'}, 500

        return item

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(Item.db)
        cursor = connection.cursor()

        query_select = f"SELECT * FROM {Item.table} where name=?"
        cursor.execute(query_select, (name,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return {'name': row[0], 'price': row[1]}
        else:
            return None

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect(Item.db)
        cursor = connection.cursor()

        query_select = f"INSERT INTO {Item.table} VALUES (?, ?)"
        cursor.execute(query_select, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect(Item.db)
        cursor = connection.cursor()

        query_select = f"UPDATE {Item.table} SET price=? WHERE name=?"
        cursor.execute(query_select, (item['price'], item['name']))
        connection.commit()
        connection.close()


class ItemList(Resource):
    db = 'data/data.db'
    table = 'items'

    def get(self):
        connection = sqlite3.connect(ItemList.db)
        cursor = connection.cursor()

        query_select = f"SELECT * FROM {ItemList.table}"
        cursor.execute(query_select)
        result = cursor.fetchall()
        connection.close()

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        return {'Items': items}
