import bcrypt
from config import lang
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from messages import user_messages
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help=user_messages[lang]["must_provide_username"],
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help=user_messages[lang]["must_provide_password"],
)


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_name(data["username"]):
            return {"message": user_messages[lang]["user_already_exists"]}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": user_messages[lang]["user_created_successfully"]}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {"message": user_messages[lang]["user_not_found"]}, 404

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"message": "user id:{} deleted".format(user_id)}
        return {"message": user_messages[lang][user_not_found]}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if user and bcrypt.checkpw(data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": user_messages[lang]["invalid_credentials"]}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": user_messages[lang]["successfully_logged_out"]}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
