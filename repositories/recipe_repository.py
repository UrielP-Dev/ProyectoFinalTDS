from pymongo import MongoClient
from models.recipe import Recipe

class RecipeRepository:
    def __init__(self, client: MongoClient):
        self.db = client["plan_comidas"]
        self.collection = self.db["recipes"]

    def search_recipes(self, query: str):
        filter_query = {"name": {"$regex": query, "$options": "i"}}
        results = self.collection.find(filter_query)
        return [Recipe.from_dict(doc) for doc in results]

    def get_all_recipes(self):
        results = self.collection.find()
        return [Recipe.from_dict(doc) for doc in results]