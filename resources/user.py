from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
     create_access_token, 
     create_refresh_token, 
     jwt_refresh_token_required, 
     get_jwt_identity
)

from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="Username is required!"
                    )
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="Password is required!"
                    )
                        
class UserRegister(Resource):
    
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel(**data)

        if UserModel.find_by_username(data['username']):
            return {"message": f"User '{data['username']} already exists!"}, 400

        try:
            user.save_to_db()
        except Exception as err:
            return {"message": f"Could not insert the item: {err}"}, 500

        return {"message": f"{data['username']} created successfully!"}, 201
              
class User(Resource):
    
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        return {'user': user.json()}, 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        try:
            user.delete_from_db()
            return {'message': f'{user.json()} successfully deleted.'}, 200
        except:
            return {'message': f'Could not delete {user.json()}'}, 500

class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials. Nice try.'}, 401
       

class TokenRefresh(Resource):

    '''
    Receives a refresh_token and returns a access_token (not fresh) for logged in user
    '''
    @jwt_refresh_token_required
    def post(self):
        user_identity = get_jwt_identity()

        new_token = create_access_token(identity=user_identity, fresh=False)

        return {'access_token': new_token}, 200