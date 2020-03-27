from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

import sqlite3

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
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field is required!"
    )

    @jwt_required()
    def get(self, name):
        # Search in items if new_item already exists
        for item in items:
            if item['name'].lower() == name.lower():
                return item, 200
        return {'item': None}, 404

    def post(self, name):
        
        # Search in items if the new item already exists
        for item in items:
            if item['name'].lower() == name.lower():
                return {'message': f"An item named {item['name']} already in items!"}, 400

        data = Item.parser.parse_args()

        new_item = {
            "name": name,
            "price": data['price']
        }

        items.append(new_item)

        return new_item, 201

    def put(self, name):
        data = Item.parser.parse_args()

        new_item = {
            "name": name,
            "price": data['price']
        }

        # Search in items if new_item already exists
        for item in items:
            if item['name'].lower() == name.lower():
                item.update(data)
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
