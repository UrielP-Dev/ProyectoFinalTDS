from bson import ObjectId
from collections import defaultdict
from repositories.mongo_connection import db

def generate_shopping_list(user_id):
    print(f"ID recibido en shopping_list_service: {user_id}")
    try:
        user_id_obj = ObjectId(user_id)
        print(f"ID convertido a ObjectId: {user_id_obj}")
    except Exception as e:
        print(f"Error al convertir ID: {e}")
        return []

    weekly_plan = db.weekly_plans.find_one({"user_id": user_id_obj})
    
    if not weekly_plan:
        print(f"No se encontró ningún plan semanal para el usuario")
        all_plans = list(db.weekly_plans.find())
        print(f"Planes disponibles: {all_plans}")
        return []
    
    print(f"Plan semanal encontrado: {weekly_plan}")
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