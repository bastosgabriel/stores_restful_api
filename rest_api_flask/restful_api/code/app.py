from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///store.db"

app.secret_key = 'bobiki'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
    