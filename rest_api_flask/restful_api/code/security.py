users = [
    {
        'id': 1,
        'username': 'bobi',
        'password': 'senhadobob'
    }
]


username_mapping = {
    'bobi': {
        'id': 1,
        'username': 'bobi',
        'password': 'senhadobob'
    }
}

userid_mapping = {
    1: {
        'id': 1,
        'username': 'bobi',
        'password': 'senhadobob'
    }
}

def authenticate(username,password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)    