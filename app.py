from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'mjaiswal'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'Item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'An item with name {name} already exists'}, 400

        request_data = request.get_json()
        new_item = {
            'name': name,
            'price': request_data['price']
        }
        items.append(new_item)
        return new_item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] == name, items))
        return {'message': f'Item {name} is deleted'}

    def put(self, name):
        pass


class ItemList(Resource):

    def get(self):
        return {'Items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
