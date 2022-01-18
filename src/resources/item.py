from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.item import ItemModel
from middleware.decorator import middleware_decorator


class Items(Resource):
    @middleware_decorator()
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items for {}'.format(user_id): items}, 200
        return {'items for anonymous': items}, 200
        #return {'items': list(map(lambda i: i.json(), ItemModel.query.all()))} #lambda version to list comprehention

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Get real dude!"
        )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Gimme store!"
        )
    #@jwt_required()
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'item': item}, 404
        
    @jwt_required(fresh=True)
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201
    
    @jwt_required()
    def put (self, name: str):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json(), 200
    
    @jwt_required()
    def delete (self, name: str):
        claims = get_jwt()
        if not claims['is admin']:
            return {'message': 'Admin privilage required'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404
