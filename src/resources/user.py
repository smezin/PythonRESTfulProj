import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='must provide username')
    parser.add_argument('password',
        type=str,
        required=True,
        help='must provide password')   

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_name(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201