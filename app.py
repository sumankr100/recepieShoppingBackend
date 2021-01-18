from datetime import timedelta
from flask import Flask
from flask_restplus import Api
from flask_jwt import JWT

from security import authentication, identity
from resources.user import UserRegister
from resources.ingredient import Ingredient, IngredientList
from resources.recipe import Recipe, RecipeList

from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.secret_key = 'sec'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authentication, identity)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)  # setting half hour of token expiring time


@app.before_first_request
def create_table():
    db.create_all()


db.init_app(app)

api.add_resource(Ingredient, '/ingredient/<string:name>')
api.add_resource(IngredientList, '/ingredientList')
api.add_resource(Recipe, '/recipe/<string:name>')
api.add_resource(RecipeList, '/recipeList')
api.add_resource(UserRegister, "/UserRegister")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
