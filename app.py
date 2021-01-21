from datetime import timedelta
from flask import Flask, render_template
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
    from resources.recipe import Recipe, RecipeList
    from resources.shopping_item import (
        ShoppingItem, ShoppingItemList, ShoppingItemUpdate,
        IngredientsToShoppingList
    )

    from db import api
    api.init_app(
        app,
        title='Recipe Shopping API',
        description="Recipe Shopping API is Demo POC to demonstrate Angular +"
        +" flask CRUD Actions"
    )

    api.add_resource(Recipe, '/recipe/<int:recipe_id>', endpoint='recipe')
    api.add_resource(RecipeList, '/recipe', endpoint='recipe-list')
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
    app.config['DEBUG'] = False
    app.config['PROPOGATE_EXCEPTIONS'] = True
    app.secret_key = '+\xba\xa5\xe6\xefv\x9c#\xba\xd9\x05pL\xc1\x11\x13\xc9\x1b-k1Rlr'

    @app.route('/redoc')
    def send_redoc():
        return render_template('recipe/redoc.html')

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
