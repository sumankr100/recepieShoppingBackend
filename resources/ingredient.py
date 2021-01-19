from flask_restplus import Resource, reqparse
from flask_jwt import jwt_required
from models.ingredient import IngredientModel


class Ingredient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount',
                        type=float,
                        required=True,
                        help="Amount field cannot be left blank!")

    def get(self, name):
        """
        To get the ingredient details
        :param name: Name of the ingredient.
        :return: Returns the details of ingredients with name and amount.
        """
        ingredient = IngredientModel.find_by_name(name)
        if ingredient:
            return ingredient.json(), 200
        return {"message": "Ingredient {} not found.".format(name)}, 404

    @jwt_required()
    def post(self, name):
        if IngredientModel.find_by_name(name):
            return {'message': 'An ingredient with name {} already exist'.format(name)}, 400
        # data = request.get_json(silent=True)
        data = Ingredient.parser.parse_args()
        ingredient = IngredientModel(name, **data)
        try:
            ingredient.save_to_db()
        except:
            return {"message": "Error in inserting ingredient {}".format(name)}, 500
        return ingredient.json(), 201

    @jwt_required()
    def delete(self, name):
        ingredient = IngredientModel.find_by_name(name)
        if ingredient:
            ingredient.delete_from_db()
            return {"message": "Ingredient {} deleted".format(name)}
        return {"message": "Ingredient {} does not exist.".format(name)}

    @jwt_required()
    def put(self, name):
        data = Ingredient.parser.parse_args()
        ingredient = IngredientModel.find_by_name(name)
        if not ingredient:
            ingredient = IngredientModel(name, **data)
        else:
            ingredient.price = data['amount']
        ingredient.save_to_db()
        return ingredient.json(), 201


class IngredientList(Resource):
    def get(self):
        ingredients = [ingredient.json() for ingredient in IngredientModel.query.filter_by(recipe_id=None)]
        # ingredients = [ingredient.json() for ingredient in IngredientModel.query.all()]
        return ({"ingredients": ingredients}, 200) if ingredients else ({"message": "Not a single Ingredient present"}, 400)
