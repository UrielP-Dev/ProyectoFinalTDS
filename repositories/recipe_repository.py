from repositories.mongo_connection import db

def get_recipe_by_id(recipe_id):
    return db["recipes"].find_one({"_id": recipe_id})
