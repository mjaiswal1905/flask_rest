import sqlite3
from flask_restful import Resource, reqparse


class User:
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


class UserRegister(Resource):
    db = 'data/data.db'
    table = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This can not be blank!")
    parser.add_argument('password', type=str, required=True, help="This can not be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message': f'User with username: {data["username"]} already exists'}, 400

        connection = sqlite3.connect(UserRegister.db)
        cursor = connection.cursor()

        query_select = f"INSERT INTO {UserRegister.table} VALUES(NULL, ?, ?)"
        cursor.execute(query_select, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created!'}, 201
