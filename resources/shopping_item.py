from flask_restplus import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.shopping_item import ShoppingItemModel
from models.recipe import RecipeModel


class ShoppingItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=False,
                        help="This is id field to store in database!")
    parser.add_argument('name',
                        type=str,
                        required=False,
                        help="This field contains the name of item!")
    parser.add_argument('amount',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!")

    @jwt_required()
    def post(self, name):
        data = ShoppingItem.parser.parse_args()

        user = current_identity

        item = ShoppingItemModel(name, data['amount'], user_id=user.id)
        ShoppingItemModel.user_id = current_identity.id
        try:
            item.save_to_db()
        except:
            return {"message": "Error in inserting item {}".format(name)}, 500
        return item.json(), 201


class ShoppingItemUpdate(Resource):
    @jwt_required()
    def get(self, _id):
        """

        :param _id:
        :return:
        """
        user = current_identity

        item = ShoppingItemModel.query.filter(
            ShoppingItemModel.id == _id,
            ShoppingItemModel.user_id == user.id
        ).first()

        if item:
            return item.json(), 200
        return {"message": "Item {} not found.".format(_id)}, 404

    @jwt_required()
    def delete(self, _id):
        user = current_identity
        item = ShoppingItemModel.find_by_id(_id)
        if item:
            item.delete_from_db()
            return {"message": "Item {} deleted".format(_id)}
        return {"message": "Item {} does not exist.".format(_id)}

    @jwt_required()
    def put(self, _id):
        data = ShoppingItem.parser.parse_args()
        item = ShoppingItemModel.find_by_id(_id)
        user = current_identity
        if not item:
            item = ShoppingItemModel(
                data['name'], data['amount'], 
                _id, user_id=user.id
            )
        else:
            item.name = data['name']
            item.amount = data['amount']
        item.save_to_db()
        return item.json(), 201


class ShoppingItemList(Resource):
    @jwt_required()
    def get(self):
        user = current_identity
        items = [item.json() for item in ShoppingItemModel.query.filter(
            ShoppingItemModel.user_id == user.id
        ).all()]
        return ({"items": items}, 200) if items else ({"message": "Not a single Item present"}, 400)


class IngredientsToShoppingList(Resource):
    @jwt_required()
    def post(self, recipe_id):
        recipe = RecipeModel.query.get(recipe_id)
        user = current_identity

        if not recipe:
            return {
                "ok": False, "err_msg": f"Recipe {recipe_id} not Found"
            }, 404
        try:
            ShoppingItemModel.bulk_add(
                recipe.ingredients.all(), user_id=user.id
            )
        except Exception as exc:
            print(exc)
            return {
                "ok": False, "err_msg": "Failed to add to shopping list"
            }, 500
        return {"ok": True}, 201
