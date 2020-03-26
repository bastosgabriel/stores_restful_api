from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'bobiki'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = [
    {
        "name": "liquidificador",
        "price": 10.99
    }
]

class Items(Resource):

    def get(self):
        return {'Items': items}

class Item(Resource):

    @jwt_required()
    def get(self, name):
        # Search in items if new_item already exists
        for item in items:
            if item['name'].lower() == name.lower():
                return item, 200
        return {'item': None}, 404

    def post(self, name):
        data = request.get_json()

        new_item = {
            "name": name,
            "price": data['price']
        }

        # Search in items if new_item already exists
        for item in items:
            if item['name'].lower() == new_item['name'].lower():
                return {'message': f"An item named {item['name']} already in items!"}, 400

        items.append(new_item)

        return new_item, 201

    def put(self, name):
        data = request.get_json()

        new_item = {
            "name": name,
            "price": data['price']
        }

        # Search in items if new_item already exists
        for item in items:
            if item['name'].lower() == new_item['name'].lower():
                item['price'] = new_item['price']
                return new_item, 200

        items.append(new_item)

        return new_item, 201

    def delete(self, name):
        for index, item in enumerate(items):
            if item['name'].lower() == name.lower():
                return items.pop(index), 200

        return {'message': f"Item '{name}' does not exist!"}, 400


api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(debug = True)