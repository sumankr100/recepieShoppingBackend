from flask_restplus import Resource, reqparse, fields
from models.user import UserModel

from db import api


user_post_model = api.model('UserRegister', {
    'username': fields.String,
    'password': fields.String
})


response_model = api.model('UserRegisterResponse', {
    'ok': fields.Boolean,
    'message': fields.String
})


class UserRegister(Resource):
    @api.expect(user_post_model, validate=True)
    @api.marshal_with(response_model)
    def post(self):
        """
        Accepts username and password in json format and return message \
        whether user is created or not
        """
        data = api.payload

        username = data.get('username', 'BLANK')

        if UserModel.find_user_by_name(username):
            return {
                "ok": False,
                "message": f"User with name {username} already exists"
            }, 400

        user = UserModel(**data)

        user.save_to_db()

        return {
            "ok": True, 
            "message": f"User {username} created successfully."
        }

