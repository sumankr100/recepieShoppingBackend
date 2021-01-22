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
        try:
            item.save_to_db()
        except:
            return {"message": f"Error in inserting item {name}"}, 500
        return item.json(), 201


class ShoppingItemUpdate(Resource):
    @jwt_required()
    def get(self, _id):
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
        shopping_items = ShoppingItemModel.query.filter_by(user_id=user.id).all()
        print(len(shopping_items), f'items found for {user.id}')
        items = [item.json() for item in shopping_items]
        return ({"items": items}, 200)


class IngredientsToShoppingList(Resource):
    @jwt_required()
    def post(self, recipe_id):
        from models.ingredient import IngredientModel

        ings = IngredientModel.query.filter(
            IngredientModel.recipe_id == recipe_id
        ).all()

        user = current_identity

        try:
            print(len(ings), 'ings moved to list for {user.id} user')
            ShoppingItemModel.bulk_add(
                ings, user_id=user.id
            )
        except Exception as exc:
            print(exc)
            return {
                "ok": False, "err_msg": "Failed to add to shopping list"
            }, 500
        return {"ok": True}, 201
