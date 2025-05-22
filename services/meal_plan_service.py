from models.meal_plan import MealPlan
from repositories.meal_plan_repository import MealPlanRepository
from repositories.recipe_repository import RecipeRepository

class MealPlanService:
    def __init__(self):
        self.meal_plan_repo = MealPlanRepository()
        self.recipe_repo = RecipeRepository()
    
    def add_meal_plan(self, user_id, day, meal_type, recipe_id):
        """Añade un nuevo plan de comida o actualiza uno existente"""
        # Comprobar si ya existe un plan para ese usuario, día y tipo de comida
        existing_plan = self.meal_plan_repo.get_by_user_day_meal(user_id, day, meal_type)
        
        if existing_plan:
            # Actualizar el plan existente
            existing_plan.recipe_id = recipe_id
            return self.meal_plan_repo.save(existing_plan)
        else:
            # Crear un nuevo plan
            new_plan = MealPlan(
                user_id=user_id,
                day=day,
                meal_type=meal_type,
                recipe_id=recipe_id
            )
            return self.meal_plan_repo.save(new_plan)
    
    def get_meal_plan(self, meal_plan_id):
        """Obtiene un plan de comida por su ID"""
        return self.meal_plan_repo.get_by_id(meal_plan_id)
    
    def get_meal_plans_by_user(self, user_id):
        """Obtiene todos los planes de comida de un usuario"""
        return self.meal_plan_repo.get_by_user(user_id)
    
    def delete_meal_plan(self, meal_plan_id):
        """Elimina un plan de comida"""
        return self.meal_plan_repo.delete(meal_plan_id)
    
    def get_meal_plan_by_user_day_meal(self, user_id, day, meal_type):
        """Obtiene un plan de comida por usuario, día y tipo de comida"""
        return self.meal_plan_repo.get_by_user_day_meal(user_id, day, meal_type) 