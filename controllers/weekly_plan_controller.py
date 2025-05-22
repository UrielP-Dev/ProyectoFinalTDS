from services.weekly_plan_service import WeeklyPlanService
from services.meal_plan_service import MealPlanService
from services.recipe_service import RecipeService

class WeeklyPlanController:
    def __init__(self, view, user_data):
        self.view = view
        self.user_data = user_data
        self.weekly_plan_service = WeeklyPlanService()
        self.meal_plan_service = MealPlanService()
        self.recipe_service = RecipeService()
        
        # Cargar datos iniciales
        self.load_weekly_plan()
    
    def load_weekly_plan(self):
        """Carga el plan semanal del usuario"""
        # Obtener el plan semanal actual
        weekly_plan = self.weekly_plan_service.get_user_plan(self.user_data._id)
        
        # Obtener todos los planes de comida del usuario
        meal_plans = self.meal_plan_service.get_meal_plans_by_user(self.user_data._id)
        
        # Organizar los planes por día y tipo de comida
        self.user_data.meal_plans = {}
        for meal_plan in meal_plans:
            key = f"{meal_plan.day}_{meal_plan.meal_type}"
            self.user_data.meal_plans[key] = meal_plan
        
        # Actualizar la vista
        self.view.load_weekly_plan()
    
    def add_recipe_to_weekly_plan(self, recipe_id):
        """Añade una receta al plan semanal"""
        try:
            self.weekly_plan_service.add_recipe_to_plan(self.user_data._id, recipe_id)
            return True
        except Exception as e:
            print(f"Error al añadir receta al plan semanal: {e}")
            return False
    
    def remove_recipe_from_weekly_plan(self, recipe_id):
        """Elimina una receta del plan semanal"""
        try:
            self.weekly_plan_service.remove_recipe_from_plan(self.user_data._id, recipe_id)
            # Actualizar la vista
            self.load_weekly_plan()
            return True
        except Exception as e:
            print(f"Error al eliminar receta del plan semanal: {e}")
            return False 