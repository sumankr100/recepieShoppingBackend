# from flask_restful import Resource, reqparse
from flask_restplus import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username is required for register.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password is required for register.")

    @staticmethod
    def post():
        """
        Accepts username and password in json format and return message whether user is created or not
        {
            "username": test_user,
            "password": test_password
        }
        :return: confirmation
        """
        data = UserRegister.parser.parse_args()
        if UserModel.find_user_by_name(data['username']):
            return {"message": "User with name {} already exists.".format(data['username'])}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User {} created successfully.".format(data["username"])}


