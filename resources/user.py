from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        data = UserRegister.parser.parse_args()
        user = UserModel(**data)

        if UserModel.find_by_username(data['username']):
            return {"message": f"User '{data['username']} already exists!"}, 400

        try:
            user.save_to_db()
        except Exception as err:
            return {"message": f"Could not insert the item: {err}"}, 500

        return {"message": f"{data['username']} created successfully!"}, 201
        

    @jwt_required()
    def get(self):  # THIS METHOD IS JUST FOR TESTING
        return {'users': [user.json() for user in UserModel.query.all()]}, 200
        
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