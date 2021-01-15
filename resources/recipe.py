from flask_restplus import Resource, reqparse
from models.recipe import RecipeModel


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

    def get(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json()
        return {"message": "Recipe {} not found.".format(name)}, 404

    def post(self, name):
        if RecipeModel.find_by_name(name):
            return {"message": "A recipe with name {} already exist.".format(name)}, 400
        data = Recipe.parser.parse_args()
        recipe = RecipeModel(name, **data)
        try:
            recipe.save_to_db()
        except:
            return {"message": "An error occurred while creating recipe {}.".format(name)}, 500
        return recipe.json(), 201

    def delete(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            recipe.delete_from_db()
        return {"message": "Recipe {} deleted.".format(name)}

    def put(self, name):
        data = Recipe.parser.parse_args()
        recipe = RecipeModel.find_by_name(name)
        if not recipe:
            recipe = RecipeModel(name, **data)
        else:
            recipe.description = data['description']
            recipe.imagePath = data['imagePath']
        recipe.save_to_db()
        return recipe.json(), 201


class RecipeList(Resource):
    def get(self):
        return {"recipes": [recipe.json() for recipe in RecipeModel.query.all()]}
