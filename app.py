from datetime import timedelta
from flask import Flask
from flask_restplus import Api

from flask_jwt import JWT
from security import authentication, identity


def register_extensions(app):
    from db import db
    db.init_app(app)

    app.config['JWT_AUTH_URL_RULE'] = '/login'
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)  # setting half hour of token expiring time

    jwt = JWT(app, authentication, identity)


def register_endpoints(app):
    from resources.user import UserRegister
    from resources.ingredient import Ingredient, IngredientList
    from resources.recipe import Recipe
    from resources.shopping_item import (
        ShoppingItem, ShoppingItemList, ShoppingItemUpdate,
        IngredientsToShoppingList
    )

    from db import api
    api.init_app(app)

    api.add_resource(Recipe, '/recipe', '/recipe/<int:recipe_id>', endpoint='recipe')
    api.add_resource(
        IngredientsToShoppingList, '/toShoppingList/<int:recipe_id>'
    )

    api.add_resource(ShoppingItem, '/shoppingItem/<string:name>')
    api.add_resource(ShoppingItemUpdate, '/shoppingItemUpdate/<int:_id>')
    api.add_resource(ShoppingItemList, '/shoppingItemList')

    api.add_resource(UserRegister, "/UserRegister")

    return api


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:mymotog2P@localhost:5432/recipe_db'
    app.secret_key = 'sec'

    return app


app = create_app()
register_extensions(app)
api = register_endpoints(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
