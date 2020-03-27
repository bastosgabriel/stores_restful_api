import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Items(Resource):
    
    def get(self):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM items"
        result = cursor.execute(select_query)
        rows = result.fetchall()

        connection.commit()
        connection.close()

        return {"items": rows}, 200

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field is required!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(select_query, (name,))

        row = result.fetchone()

        if row:
            item = row
        else:
            item = None

        connection.commit()
        connection.close()

        return item

    @jwt_required()
    def get(self, name):
        if Item.find_by_name(name):
            return {'item': Item.find_by_name(name)}, 200
        else:
            return {'item': None}, 404
    
    def post(self, name):
        if Item.find_by_name(name):
            return {'message': f"An item named '{name}' already exists!"}, 400

        data = Item.parser.parse_args()

        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO items (name, price) VALUES (?, ?)"
        cursor.execute(insert_query, (name, data['price']))

        connection.commit()
        connection.close()

        return {"message": f"'{name}'' created successfully!"}, 201

    
    def put(self, name):
        data = Item.parser.parse_args()

        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        # Update item if item already exists
        if Item.find_by_name(name):
            update_query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(update_query, (data['price'], name))

            connection.commit()
            connection.close()

            return {"message": f"'{name}' updated successfully!"}, 201

        insert_query = "INSERT INTO items (name, price) VALUES (?, ?)"
        cursor.execute(insert_query, (name, data['price']))

        connection.commit()
        connection.close()

        return {"message": f"'{name}'' created successfully!"}, 201


    '''
    def delete(self, name):
        for index, item in enumerate(items):
            if item['name'].lower() == name.lower():
                return items.pop(index), 200

        return {'message': f"Item '{name}' does not exist!"}, 400
    '''