from werkzeug.security import safe_str_cmp
from user import User


def authentication(username, password):
    user = User.find_user_by_name(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_user_by_id(user_id)

