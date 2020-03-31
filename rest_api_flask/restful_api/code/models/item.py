import sqlite3

class ItemModel():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    '''
    Returns a json formatted dictionary representing the item. 
    {'name': <itemname>, 'price': <itemprice>}
    '''
    def json(self) -> dict:
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name, database):
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        select_query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(select_query, (name,))

        row = result.fetchone()

        if row:
            item = ItemModel(row[1], row[2])
        else:
            item = None

        connection.commit()
        connection.close()

        return item
    
    '''
    Insert item model to .db file.
    '''
    def insert(self, database: str) -> None:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        insert_query = "INSERT INTO items (name, price) VALUES (?, ?)"
        cursor.execute(insert_query, (self.name, self.price))

        connection.commit()
        connection.close()

    '''
    Update item model at .db file. If item doesn't exist, create it.
    '''
    def update(self, database: str) -> None:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        
        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (self.price, self.name))

        connection.commit()
        connection.close()
        