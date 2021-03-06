from db import db


class ShoppingItemModel(db.Model):

    __tablename__ = "shopping_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    amount = db.Column(db.Integer)

    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id')
    )

    def __init__(self, name, amount, user_id, _id=None):
        self.id = _id
        self.name = name
        self.user_id = user_id
        self.amount = amount

    def json(self):
        return {'id': self.id, 'name': self.name, 'amount': self.amount}

    @classmethod
    def find_by_name(cls, name, _id=None):
        if _id:
            return cls.query.filter_by(name=name).filter_by(id=_id).first()
        else:
            return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def bulk_add(cls, ingredient_objs, user_id):
        db.session.add_all([
            cls(name=ing_obj.name, amount=ing_obj.amount, user_id=user_id) \
                for ing_obj in ingredient_objs]
        )
        db.session.commit()
