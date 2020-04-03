import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username is required!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password is required!"
                        )

    def post(self):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        user = UserRegister.parser.parse_args()

        if UserModel.find_by_username(user['username']):
            return {
                    "message": f"User '{user['username']} already exists!"}, 400

        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(insert_query, (user['username'], user['password']))

        connection.commit()
        connection.close()

        return {"message": f"{user['username']} created successfully!"}, 201

    def get(self):  # THIS METHOD IS JUST FOR TESTING
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users"

        result = cursor.execute(select_query)
        rows = result.fetchall()

        connection.commit()
        connection.close()

        return rows
