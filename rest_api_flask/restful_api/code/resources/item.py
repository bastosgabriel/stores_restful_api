import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Items(Resource):
    
    def get(self):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM items"
        result = cursor.execute(select_query)
        rows = result.fetchall()

        items = []
        for row in rows:
            items.append({'name': row[1], 'price': float(row[2])})

        connection.commit()
        connection.close()

        return {"items": items}, 200

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field is required!"
    )
  
    @jwt_required()
    def get(self, name):
        if ItemModel.find_by_name(name):

            return {'item': ItemModel.find_by_name(name)}, 200
        else:
            return {'item': None}, 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item named '{name}' already exists!"}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        try:
            ItemModel.insert(item)
        except Exception as err:
            return {"message": f"Could not insert the item: {err}"}, 500


        return {"message": f"'{name}'' created successfully!"}, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        # Update item if item already exists
        if ItemModel.find_by_name(name):
            try:
                ItemModel.update(item)
            except Exception as err:
                return {"message": f"Could not update the item: {err}"}, 500

            return {"message": f"'{name}' updated successfully!"}, 201
        else:
            try:
                ItemModel.insert(item)
            except Exception as err:
                return {"message": f"Could not insert the item: {err}"}, 500

            return {"message": f"'{name}'' created successfully!"}, 201
    
    def delete(self, name):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        # Update item if item already exists
        if ItemModel.find_by_name(name):
            delete_query = "DELETE FROM items WHERE name=?"
            cursor.execute(delete_query, (name,))

            connection.commit()
            connection.close()

            return {"message": f"'{name}' deleted successfully!"}, 200

        return {'message': f"Item '{name}' does not exist!"}, 400
    