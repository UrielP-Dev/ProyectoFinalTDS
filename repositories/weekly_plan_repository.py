from pymongo import MongoClient
from bson.objectid import ObjectId
from models.weekly_plan import WeeklyPlan
from repositories.mongo_connection import get_db_connection

class WeeklyPlanRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.collection = self.db["weekly_plans"]
    
    def save(self, weekly_plan):
        """Guarda un plan semanal en la base de datos"""
        plan_dict = weekly_plan.to_dict()
        
        # Eliminar ID si es None para que MongoDB genere uno automáticamente
        if plan_dict.get("id") is None:
            # Quitar id del diccionario
            if "id" in plan_dict:
                del plan_dict["id"]
            result = self.collection.insert_one(plan_dict)
            weekly_plan.id = str(result.inserted_id)
        else:
            # Si el ID es un string (ObjectId de MongoDB), convertirlo
            if isinstance(plan_dict["id"], str):
                object_id = ObjectId(plan_dict["id"])
                del plan_dict["id"]
                self.collection.update_one({"_id": object_id}, {"$set": plan_dict})
            else:
                # Si es un ID numérico, actualizarlo por ese ID
                _id = plan_dict["id"]
                del plan_dict["id"]
                self.collection.update_one({"id": _id}, {"$set": plan_dict})
        
        return weekly_plan
    
    def get_by_user(self, user_id, week="current"):
        """Obtiene el plan semanal de un usuario para una semana específica"""
        query = {
            "user_id": user_id,
            "week": week
        }
        
        plan_data = self.collection.find_one(query)
        
        if plan_data:
            # Convertir _id a string si existe
            if "_id" in plan_data:
                plan_data["id"] = str(plan_data["_id"])
            
            return WeeklyPlan.from_dict(plan_data)
        
        return None
    
    def add_recipe_to_plan(self, user_id, recipe_id, week="current"):
        """Añade una receta al plan semanal. Si no existe el plan, lo crea"""
        # Buscar si ya existe un plan para este usuario y semana
        plan = self.get_by_user(user_id, week)
        
        if plan:
            # Si ya existe el plan, añadir la receta si no está ya
            if recipe_id not in plan.recipes:
                plan.recipes.append(recipe_id)
                return self.save(plan)
            return plan
        else:
            # Si no existe, crear un nuevo plan con esta receta
            new_plan = WeeklyPlan(
                user_id=user_id,
                recipes=[recipe_id],
                week=week
            )
            return self.save(new_plan)
    
    def remove_recipe_from_plan(self, user_id, recipe_id, week="current"):
        """Elimina una receta del plan semanal"""
        plan = self.get_by_user(user_id, week)
        
        if plan and recipe_id in plan.recipes:
            plan.recipes.remove(recipe_id)
            return self.save(plan)
        
        return None
    
    def delete(self, plan_id):
        """Elimina un plan semanal por su ID"""
        # Intentar convertir a ObjectId si es un string
        if isinstance(plan_id, str):
            try:
                query = {"_id": ObjectId(plan_id)}
            except:
                query = {"id": plan_id}
        else:
            query = {"id": plan_id}
        
        result = self.collection.delete_one(query)
        
        return result.deleted_count > 0 