from db import db


class RecipeModel(db.Model):

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    imagePath = db.Column(db.String)

    ingredients = db.relationship('IngredientModel', lazy='dynamic', passive_deletes=True)

    def __init__(self, name, description, imagePath):
        self.name = name
        self.description = description
        self.imagePath = imagePath

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'imagePath': self.imagePath,
            'ingredients': [
                ingredient.json() for ingredient in self.ingredients.all()
            ]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def add(cls, data):
        ingredients = data.pop('ingredients', [])

        recipe_obj = cls(**data)
        recipe_obj.save_to_db()

        recipe_obj.add_ingredients(ingredients)

        return recipe_obj

    def update(self, data):
        self.delete_ingredients()
        ingredients = data.pop('ingredients', [])

        self.name = data.get('name')
        self.description = data.get('description')
        self.imagePath = data.get('imagePath')

        self.add_ingredients(ingredients)

        self.save_to_db()

    def add_ingredients(self, ingredients_data):
        from .ingredient import IngredientModel
        db.session.add_all([
            IngredientModel(**ing_data, recipe_id=self.id) \
                for ing_data in ingredients_data]
        )
        db.session.commit()

    def delete_ingredients(self):
        self.ingredients.delete()
        db.session.commit()
