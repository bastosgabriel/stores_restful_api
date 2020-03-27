import sqlite3

connection = sqlite3.connect('store.db')

cursor = connection.cursor()

create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
create_items_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price smallmoney)"

cursor.execute(create_users_table)

connection.commit()
connection.close()