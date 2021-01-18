from flask_restplus import Resource, reqparse
from flask_jwt import jwt_required
from models.shopping_item import ShoppingItemModel


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

    # @jwt_required()
    def post(self, name):
        data = ShoppingItem.parser.parse_args()
        item = ShoppingItemModel(name, data['amount'])
        try:
            item.save_to_db()
        except:
            return {"message": "Error in inserting item {}".format(name)}, 500
        return item.json(), 201


class ShoppingItemUpdate(Resource):

    def get(self, _id):
        """

        :param _id:
        :return:
        """
        item = ShoppingItemModel.find_by_id(_id)
        if item:
            return item.json(), 200
        return {"message": "Item {} not found.".format(name)}, 404

    # @jwt_required()
    def delete(self, _id):
        item = ShoppingItemModel.find_by_id(_id)
        if item:
            item.delete_from_db()
            return {"message": "Item {} deleted".format(_id)}
        return {"message": "Item {} does not exist.".format(_id)}

    # @jwt_required()
    def put(self, _id):
        data = ShoppingItem.parser.parse_args()
        item = ShoppingItemModel.find_by_id(_id)
        if not item:
            item = ShoppingItemModel(data['name'], data['amount'], _id)
        else:
            item.name = data['name']
            item.amount = data['amount']
        item.save_to_db()
        return item.json(), 201


class ShoppingItemList(Resource):
    def get(self):
        items = [item.json() for item in ShoppingItemModel.query.all()]
        # items = list(map(lambda x: x.json(), ItemModel.query.all()))
        return ({"items": items}, 200) if items else ({"message": "Not a single Item present"}, 400)
