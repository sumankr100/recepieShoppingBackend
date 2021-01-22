from flask import g
from flask_restplus import fields, Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.recipe import RecipeModel
from models.ingredient import IngredientModel
from db import api


ingredients_nested_fields = api.model('Ingredient', {
    'name': fields.String,
    'amount': fields.Integer
})

recipe_post_model = api.model('RecipeModel', {
    'name': fields.String,
    'description': fields.String,
    'imagePath': fields.String,
    'ingredients': fields.List(fields.Nested(ingredients_nested_fields))
})

recipe_resp_model = api.model('RecipeModel', {
    "id": fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'imagePath': fields.String,
    'ingredients': fields.List(fields.Nested(ingredients_nested_fields))
})

recipes_response_model = api.model('RecipeListResponseModel', {
    "recipes": fields.List(fields.Nested(recipe_resp_model))
})

recipe_delete_response = api.model('RecipeDeleteResponse', {
    'ok': fields.Boolean,
    'message': fields.String
})


class Recipe(Resource):
    @jwt_required()
    @api.doc(params={'recipe_id':'A recipe ID'})
    @api.marshal_with(recipe_resp_model)
    def get(self, recipe_id):
        """
        Recipe Details API. Takes Recipe ID from URL Param and return Recipe \
        Object
        """
        user_id = current_identity.id

        recipe = RecipeModel.query.filter(
            RecipeModel.id==recipe_id, RecipeModel.user_id==user_id
        ).first()

        if not recipe:
            return {
                "ok": False, "message": f"Recipe {recipe_id} not found."
            }, 404

        return recipe.json()

    @jwt_required()
    @api.marshal_with(recipe_delete_response)
    def delete(self, recipe_id):
        """
        Delete Recipe API.
        """
        recipe = RecipeModel.query.get(recipe_id)

        if recipe:
            recipe.delete_from_db()
            return {"ok": True, "message": f"Recipe {recipe_id} deleted"}

        return {"ok": False, "message": f"Recipe {recipe_id} not found."}, 404

    @jwt_required()
    @api.expect(recipe_post_model, validate=True)
    @api.marshal_with(recipe_resp_model, code=201)
    def put(self, recipe_id):
        """
        PUT Recipe API
        """
        data = api.payload
        recipe = RecipeModel.query.get(recipe_id)

        _ = data.pop('id', None)

        user_id = current_identity.id

        if not recipe:
            recipe = RecipeModel.add(data, user_id=user_id)
        else:
            recipe.update(data, user_id=user_id)

        return recipe.json(), 201


class RecipeList(Resource):
    @jwt_required()
    @api.marshal_with(recipes_response_model)
    def get(self):
        """
        Recipe List API
        """
        user_id = current_identity.id
        return {
            "recipes": [
                recipe.json() for recipe in RecipeModel.query.filter(
                    RecipeModel.user_id==user_id
                ).all()
            ]
        }

    @jwt_required()
    @api.expect(recipe_post_model, validate=True)
    @api.marshal_with(recipe_resp_model, code=201)
    def post(self):
        """
        Recipe Post API.
        """
        data = api.payload
        name = data.get('name')
        recipe_obj = None

        user_id = current_identity.id

        try:
            recipe_obj = RecipeModel.add(data, user_id=user_id)
        except Exception as exc:
            print(exc)
            return {
                "ok": False,
                "message": f"An error occurred while creating recipe {name}"
            }, 500
        return recipe_obj.json(), 201
