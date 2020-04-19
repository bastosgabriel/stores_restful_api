import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///store.db")
app.config['PROPAGATE_EXCEPTIONS'] = True


app.secret_key = 'bobiki'
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hard-coding, you should read from a config file or database
        return {'is_admin': True}
    return {'is_admin': False}


# The following callbacks are used for customizing jwt response/error messages.

@jwt.expired_token_loader
def expired_token_callback():
    return {
        'description': 'The token has expired. :(',
        'error': 'token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'description': 'Signature verification failed. Did you try something?',
        'error': 'invalid_token'
    }, 401

@jwt.unauthorized_loader
def unauthorized_token_callback(error):
    return {
        'description': 'Request does not contain an access token. Did you forget something?',
        'error': 'unauthorization_required'
    }, 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return {
        'description': 'This token is not fresh. :(',
        'error': 'fresh_token_required'
    }, 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return {
        'description': 'The token has been revoked!',
        'error': 'token_revoked'
    }, 401

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
    