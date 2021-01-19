from flask import g
from flask_restplus import fields, Resource, reqparse
from models.recipe import RecipeModel
from models.ingredient import IngredientModel

from db import api


class Recipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="Description field cannot be left blank!")
    parser.add_argument('imagePath',
                        type=str,
                        required=True,
                        help="Needs an image path!")
    parser.add_argument('ingredients',
                        type=list,
                        required=False,
                        help="List of ingredients.!")

ingredients_nested_fields = api.model('Ingredient', {
    'name': fields.String,
    'amount': fields.Integer
})

recipe_post_model = api.model('RecipeModel', {
    'description': fields.String,
    'imagePath': fields.String,
    'ingredients': fields.List(fields.Nested(ingredients_nested_fields))
})


class Recipe(Resource):
    def get(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json()
        return {"message": "Recipe {} not found.".format(name)}, 404

    @api.expect(recipe_post_model, validate=True)
    def post(self, name):
        if RecipeModel.find_by_name(name):
            return {"message": "A recipe with name {} already exist.".format(name)}, 400
        data = api.payload

        recipe_obj = None

        try:
            recipe_obj = RecipeModel.add(data)
        except Exception as exc:
            print(exc)
            return {"message": "An error occurred while creating recipe {}.".format(name)}, 500
        return recipe_obj.json(), 201

    def delete(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            recipe.delete_from_db()
            return {"message": "Recipe {} deleted.".format(name)}
        return {"message": "Recipe {} not found.".format(name)}

    @api.expect(recipe_post_model, validate=True)
    def put(self, name):
        data = api.payload
        recipe = RecipeModel.find_by_name(name)

        if not recipe:
            recipe = RecipeModel(name, **data)
            recipe.save_to_db()
        else:
            recipe.update(data)

        return recipe.json(), 201


class RecipeList(Resource):
    def get(self):
        return {"recipes": [recipe.json() for recipe in RecipeModel.query.all()]}

