from db import db


class IngredientModel(db.Model):

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    amount = db.Column(db.Float(precision=2))

    recipe_id = db.Column(
        db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE')
    )
    recipe = db.relationship('RecipeModel', passive_deletes=True)

    def __init__(self, name, amount, recipe_id=None):
        self.name = name
        self.amount = amount
        self.recipe_id = recipe_id

    def json(self):
        return {'name': self.name, 'amount': self.amount}

    @classmethod
    def find_by_name(cls, name, recipe_id=None):
        return cls.query.filter_by(name=name).filter_by(recipe_id=recipe_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
