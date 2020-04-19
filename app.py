import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///store.db")
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'bobiki'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
    