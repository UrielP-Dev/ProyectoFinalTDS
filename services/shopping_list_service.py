from pymongo import MongoClient
from bson import ObjectId
from models.recipe import Recipe

class ShoppingListService:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["nutriplan"]
        self.users = self.db["users"]
        self.recipes = self.db["recipes"]
        self.weekly_plans = self.db["weekly_plans"]

    def get_ingredients_for_user(self, username):
        user = self.users.find_one({"username": username})
        if not user:
            raise Exception("Usuario no encontrado.")

        plan = self.weekly_plans.find_one({"user_id": user["_id"]})
        if not plan:
            raise Exception("No hay planificación semanal para este usuario.")

        recipe_ids = []
        for day, meals in plan["days"].items():
            for meal in ["desayuno", "almuerzo", "cena"]:
                recipe_id = meals.get(meal)
                if recipe_id:
                    recipe_ids.append(recipe_id)

        ingredients = set()
        for r_id in recipe_ids:
            recipe_data = self.recipes.find_one({"_id": ObjectId(r_id)})
            if recipe_data:
                recipe = Recipe.from_dict(recipe_data)
                ingredients.update(recipe.ingredients)

        return list(ingredients)
