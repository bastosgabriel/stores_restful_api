from flask_jwt import jwt_required

from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
        def get(self,name):
            store = StoreModel.find_by_name(name)

            if store:
                return store.json(),200
            else:
                return {'message': f"Store '{name}' not found!"},404
        @jwt_required()
        def post(self,name):
            if (StoreModel.find_by_name(name)):
                return {'message': f"Store '{name}' already exists!"},400
            
            store = StoreModel(name)
            try:
                store.save_to_db()
            except Exception as e:
                return {'message': f"An error ocurred while trying to create store {name}: {e}"},500
            
            return store.json(),201

        @jwt_required()
        def delete(self,name):
            store = StoreModel.find_by_name(name)
            if store:
                store.delete()

            return {'message': f"Store '{name}' was deleted."},200


class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 200

        
