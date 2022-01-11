import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Items(Resource):
    @jwt_required()
    def get(self):
        return {'items':items}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Get real dude!"
        )
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'item': item}, 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "item '{}' already exists".format(name)}, 400
            
        item_data = Item.parser.parse_args()
        item = ItemModel(name, item_data['price'])
        try:
            item.insert()
        except:
            return {'message': 'Error inserting item'}
        return item, 201

    def put (self, name):
        if ItemModel.find_by_name(name):
            return {'message': "item '{}' does not exist".format(name)}, 400
        try:
            item_data = Item.parser.parse_args()
            updated_item = ItemModel(name, item_data['price'])
            updated_item.update()
        except:
            return {'message': 'Error updating item'}

        return item, 200

    def delete (self, name):
        pass
