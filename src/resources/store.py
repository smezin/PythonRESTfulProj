from flask_restful import Resource, reqparse
from models.store import StoreModel

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)   
        if store:
            return store.json()
        return {'message': 'Store not found.'}, 404
         
    def post(self, name: str):
        store = StoreModel.find_by_name(name)   
        if store:
            return {'message': 'Store named: {} already exists.'.format(name)}, 400
        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 201

    def delete(self, name: str):
        store = StoreModel.find_by_name(name)   
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

