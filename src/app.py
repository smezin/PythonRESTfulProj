from flask import Flask, jsonify
from flask_restful import Api, reqparse
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, Items
from resources.store import Store, StoreList
from blacklist import BLACKLIST
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'mySecretKey'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@app.errorhandler(Exception)
def global_error_handler(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is admin': True}
    return {'is admin': False}

@jwt.token_in_blocklist_loader
def token_in_blocklist_loader(jwt_headers, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    return jsonify({
        'message': 'token expired, please sign in again',
        'error': 'token expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Invalid token',
        'error': error
    }), 401

@jwt.unauthorized_loader
def unathorized_loader(error):
    return jsonify({
        'message': 'Missing token',
        'error': error
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_loader(jwt_headers, jwt_payload):
    return jsonify({
        'message': 'Your token is stale',
    }), 401

@jwt.revoked_token_loader
def revoked_token_loader(jwt_headers, jwt_payload):
    return jsonify({
        'message': 'Token revoked',
    }), 401

api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
