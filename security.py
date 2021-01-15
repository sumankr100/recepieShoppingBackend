from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authentication(username, password):
    user = UserModel.find_user_by_name(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_user_by_id(user_id)

