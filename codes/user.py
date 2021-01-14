import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_user_by_name(cls, username):
        connection = sqlite3.connect("database/data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_user_by_id(cls, _id):
        connection = sqlite3.connect("database/data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user


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

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_user_by_name(data['username']):
            return {"message": "User with name {} already exists.".format(data['username'])}, 400
        connection = sqlite3.connect("database/data.db")
        cursor = connection.cursor()
        in_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(in_query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {"message": "User {} created successfully.".format(data["username"])}


