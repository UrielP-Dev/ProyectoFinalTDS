from pymongo import MongoClient
from bson.objectid import ObjectId
from models.meal_plan import MealPlan
from repositories.recipe_repository import RecipeRepository
from repositories.mongo_connection import get_db_connection

class MealPlanRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.collection = self.db["meal_plans"]
        self.recipe_repo = RecipeRepository()
    
    def save(self, meal_plan):
        """Guarda un plan de comida en la base de datos"""
        meal_plan_dict = meal_plan.to_dict()
        
        # Eliminar ID si es None para que MongoDB genere uno automáticamente
        if meal_plan_dict.get("id") is None:
            # Quitar id del diccionario
            if "id" in meal_plan_dict:
                del meal_plan_dict["id"]
            result = self.collection.insert_one(meal_plan_dict)
            meal_plan.id = str(result.inserted_id)
        else:
            # Si el ID es un string (ObjectId de MongoDB), convertirlo
            if isinstance(meal_plan_dict["id"], str):
                object_id = ObjectId(meal_plan_dict["id"])
                del meal_plan_dict["id"]
                self.collection.update_one({"_id": object_id}, {"$set": meal_plan_dict})
            else:
                # Si es un ID numérico, actualizarlo por ese ID
                _id = meal_plan_dict["id"]
                del meal_plan_dict["id"]
                self.collection.update_one({"id": _id}, {"$set": meal_plan_dict})
        
        return meal_plan
    
    def get_by_id(self, meal_plan_id):
        """Obtiene un plan de comida por su ID"""
        # Intentar convertir a ObjectId si es un string
        if isinstance(meal_plan_id, str):
            try:
                query = {"_id": ObjectId(meal_plan_id)}
            except:
                query = {"id": meal_plan_id}
        else:
            query = {"id": meal_plan_id}
        
        meal_plan_data = self.collection.find_one(query)
        
        if meal_plan_data:
            # Convertir _id a string si existe
            if "_id" in meal_plan_data:
                meal_plan_data["id"] = str(meal_plan_data["_id"])
            
            recipe = self.recipe_repo.find_by_id(meal_plan_data["recipe_id"])
            return MealPlan.from_dict(meal_plan_data, recipe)
        
        return None
    
    def get_by_user_day_meal(self, user_id, day, meal_type):
        """Obtiene un plan de comida por usuario, día y tipo de comida"""
        query = {
            "user_id": user_id,
            "day": day,
            "meal_type": meal_type
        }
        
        meal_plan_data = self.collection.find_one(query)
        
        if meal_plan_data:
            # Convertir _id a string si existe
            if "_id" in meal_plan_data:
                meal_plan_data["id"] = str(meal_plan_data["_id"])
            
            recipe = self.recipe_repo.find_by_id(meal_plan_data["recipe_id"])
            return MealPlan.from_dict(meal_plan_data, recipe)
        
        return None
    
    def get_by_user(self, user_id):
        """Obtiene todos los planes de comida de un usuario"""
        query = {"user_id": user_id}
        
        meal_plans_data = self.collection.find(query)
        
        meal_plans = []
        for meal_plan_data in meal_plans_data:
            # Convertir _id a string si existe
            if "_id" in meal_plan_data:
                meal_plan_data["id"] = str(meal_plan_data["_id"])
            
            recipe = self.recipe_repo.find_by_id(meal_plan_data["recipe_id"])
            meal_plans.append(MealPlan.from_dict(meal_plan_data, recipe))
        
        return meal_plans
    
    def delete(self, meal_plan_id):
        """Elimina un plan de comida por su ID"""
        # Intentar convertir a ObjectId si es un string
        if isinstance(meal_plan_id, str):
            try:
                query = {"_id": ObjectId(meal_plan_id)}
            except:
                query = {"id": meal_plan_id}
        else:
            query = {"id": meal_plan_id}
        
        result = self.collection.delete_one(query)
        
        return result.deleted_count > 0 