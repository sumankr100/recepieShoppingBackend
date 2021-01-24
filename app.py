from flask import Flask, render_template
from flask_restplus import Api

from flask_jwt import JWT
from security import authentication, identity
from config import BASE_URL_PREFIX, HOST_URL


def register_extensions(app):
    from db import db
    db.init_app(app)

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

    api.add_resource(Recipe, f'{BASE_URL_PREFIX}/recipe/<int:recipe_id>', endpoint='recipe')
    api.add_resource(RecipeList, f'{BASE_URL_PREFIX}/recipe', endpoint='recipe-list')
    api.add_resource(
        IngredientsToShoppingList, f'{BASE_URL_PREFIX}/toShoppingList/<int:recipe_id>'
    )

    api.add_resource(ShoppingItem, f'{BASE_URL_PREFIX}/shoppingItem/<string:name>')
    api.add_resource(ShoppingItemUpdate, f'{BASE_URL_PREFIX}/shoppingItemUpdate/<int:_id>')
    api.add_resource(ShoppingItemList, f'{BASE_URL_PREFIX}/shoppingItemList')

    api.add_resource(UserRegister, f"{BASE_URL_PREFIX}/UserRegister")

    return api


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route(f'{BASE_URL_PREFIX}/redoc')
    def send_redoc():
        ctx = {
            "HOST_URL": HOST_URL
        }
        return render_template('recipe/redoc.html', **ctx)

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
