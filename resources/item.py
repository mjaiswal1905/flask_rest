import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    db = 'data/data.db'
    table = 'items'
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This cannot be blank!')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400

        data = Item.parser.parse_args()
        new_item = ItemModel(name, data['price'])
        try:
            new_item.insert()
        except:
            return {'message': 'Error during insert operation'}, 500

        return new_item.json(), 201

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

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'Error during insert operation'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'Error during update operation'}, 500

        return updated_item.json()


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
