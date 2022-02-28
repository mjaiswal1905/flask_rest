from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This can not be blank!")
    parser.add_argument('password', type=str, required=True, help="This can not be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': f'User with username: {data["username"]} already exists'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'User created!'}, 201
