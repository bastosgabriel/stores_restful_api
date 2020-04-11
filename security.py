from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Authenticates the user checking if the given
    <username> exists on the database
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """
    Gets the payload containing the identity (id) of the user and
    returns the user with that given id
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
