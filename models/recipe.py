from db import db


class RecipeModel(db.Model):

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    imagePath = db.Column(db.String)

    ingredients = db.relationship('IngredientModel', lazy='dynamic')

    def __init__(self, name, description, imagePath):
        self.name = name
        self.description = description
        self.imagePath = imagePath

    def json(self):
        return {'name': self.name,
                'description': self.description,
                'imagePath': self.imagePath,
                'ingredients': [ingredient.json() for ingredient in self.ingredients.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()