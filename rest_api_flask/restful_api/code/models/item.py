import sqlite3

class ItemModel():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

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
        