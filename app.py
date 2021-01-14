from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authentication, identity
from user import UserRegister


app = Flask(__name__)
app.secret_key = 'sec'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authentication, identity)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


api.add_resource(UserRegister, "/UserRegister")

if __name__ == "__main__":
    app.run(port=5000)
