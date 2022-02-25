import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    db = 'data/data.db'
    table = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This can not be blank!")
    parser.add_argument('password', type=str, required=True, help="This can not be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': f'User with username: {data["username"]} already exists'}, 400

        connection = sqlite3.connect(UserRegister.db)
        cursor = connection.cursor()

        query_select = f"INSERT INTO {UserRegister.table} VALUES(NULL, ?, ?)"
        cursor.execute(query_select, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created!'}, 201
