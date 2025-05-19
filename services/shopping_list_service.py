from bson import ObjectId
from collections import defaultdict
from repositories.mongo_connection import db

def generate_shopping_list(user_id):
    try:
        user_id = ObjectId(user_id)
    except Exception:
        return []

    weekly_plan = db.weekly_plans.find_one({"user_id": user_id})
    if not weekly_plan:
        return []

    recipe_ids = weekly_plan.get("recipes", [])
    ingredient_totals = defaultdict(float)

    for recipe_id in recipe_ids:
        recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})
        if not recipe:
            continue

        for ing in recipe.get("ingredients", []):
            name = ing.get("name", "").strip().lower()
            unit = ing.get("unit", "").strip().lower()
            qty = ing.get("quantity", 0)

            if name:  # aseguramos que hay nombre
                key = (name, unit)
                ingredient_totals[key] += qty

    shopping_list = [
        {"name": name.capitalize(), "quantity": quantity, "unit": unit}
        for (name, unit), quantity in ingredient_totals.items()
    ]

    return shopping_list