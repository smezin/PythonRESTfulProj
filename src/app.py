from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT
from security import auth, identity
from resources.user import UserRegister
from resources.item import Item, Items
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mySecretKey'
api = Api(app)

jwt = JWT(app, auth, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
