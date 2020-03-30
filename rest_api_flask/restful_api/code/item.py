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

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(select_query, (name,))

        row = result.fetchone()

        if row:
            item = {'name': row[1], 'price': row[2]}
        else:
            item = None

        connection.commit()
        connection.close()

        return item

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO items (name, price) VALUES (?, ?)"
        cursor.execute(insert_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        
        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (item['price'], item['name']))

        connection.commit()
        connection.close()
        
    #@jwt_required()
    def get(self, name):
        if Item.find_by_name(name):

            return {'item': Item.find_by_name(name)}, 200
        else:
            return {'item': None}, 404
    
    def post(self, name):
        if Item.find_by_name(name):
            return {'message': f"An item named '{name}' already exists!"}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        try:
            Item.insert(item)
        except Exception as err:
            return {"message": f"Could not insert the item: {err}"}, 500


        return {"message": f"'{name}'' created successfully!"}, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        # Update item if item already exists
        if Item.find_by_name(name):
            try:
                Item.update(item)
            except Exception as err:
                return {"message": f"Could not update the item: {err}"}, 500

            return {"message": f"'{name}' updated successfully!"}, 201
        else:
            try:
                Item.insert(item)
            except Exception as err:
                return {"message": f"Could not insert the item: {err}"}, 500

            return {"message": f"'{name}'' created successfully!"}, 201
    
    def delete(self, name):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        # Update item if item already exists
        if Item.find_by_name(name):
            delete_query = "DELETE FROM items WHERE name=?"
            cursor.execute(delete_query, (name,))

            connection.commit()
            connection.close()

            return {"message": f"'{name}' deleted successfully!"}, 200

        return {'message': f"Item '{name}' does not exist!"}, 400
    