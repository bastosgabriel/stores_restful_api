import sqlite3

class User():

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "SELECT * from users WHERE username=?"

        result = cursor.execute(query, (username,))

        row = result.fetchone()

        if row:
            user = cls(*row) # User(id, username, password)
        else:
            user = None

        connection.close()

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "SELECT * from users WHERE id=?"

        result = cursor.execute(query, (_id,))

        row = result.fetchone()

        if row:
            user = cls(*row) # User(id, username, password)
        else:
            user = None

        connection.close()

        return user