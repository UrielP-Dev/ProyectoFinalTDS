from services.meal_plan_service import MealPlanService
from services.recipe_service import RecipeService
from services.weekly_plan_service import WeeklyPlanService
from tkinter import messagebox

class MealPlanController:
    def __init__(self, user_data, day, meal_type):
        self.user_data = user_data
        self.day = day
        self.meal_type = meal_type
        self.gui = None
        self.meal_plan_service = MealPlanService()
        self.recipe_service = RecipeService()
        self.weekly_plan_service = WeeklyPlanService()
        
    def set_gui(self, gui):
        """Establece la interfaz gráfica"""
        self.gui = gui
        
        # Cargar el plan actual
        self.load_current_meal_plan()
    
    def load_current_meal_plan(self):
        """Carga el plan de comida actual para mostrar en la interfaz"""
        if self.gui:
            meal_plan = self.meal_plan_service.get_meal_plan_by_user_day_meal(
                self.user_data._id, self.day, self.meal_type
            )
            self.gui.set_current_meal_plan(meal_plan)
    
    def search_recipes(self, query=""):
        """Busca recetas según un criterio de búsqueda"""
        if self.gui:
            recipes = self.recipe_service.search_recipes(query)
            self.gui.update_recipe_list(recipes)
    
    def save_meal_plan(self, recipe_id):
        """Guarda un plan de comida para el día y tipo de comida actual"""
        try:
            # Guardar en el plan diario
            self.meal_plan_service.add_meal_plan(
                self.user_data._id, self.day, self.meal_type, recipe_id
            )
            
            # También guardar en el plan semanal
            self.weekly_plan_service.add_recipe_to_plan(
                self.user_data._id, recipe_id
            )
            
            return True
        except Exception as e:
            print(f"Error al guardar el plan de comida: {e}")
            return False
    
    def save_meal_plan_for_day(self, recipe_id, day):
        """Guarda un plan de comida para un día específico"""
        try:
            # Guardar en el plan diario para el día específico
            self.meal_plan_service.add_meal_plan(
                self.user_data._id, day, self.meal_type, recipe_id
            )
            
            # También guardar en el plan semanal
            self.weekly_plan_service.add_recipe_to_plan(
                self.user_data._id, recipe_id
            )
            
            return True
        except Exception as e:
            print(f"Error al guardar el plan de comida: {e}")
            return False
    
    def delete_meal_plan(self):
        """Elimina el plan de comida actual"""
        try:
            # Obtener el plan actual
            meal_plan = self.meal_plan_service.get_meal_plan_by_user_day_meal(
                self.user_data._id, self.day, self.meal_type
            )
            
            if meal_plan:
                # Eliminar del plan diario
                self.meal_plan_service.delete_meal_plan(meal_plan.id)
                
                # Eliminar del plan semanal
                self.weekly_plan_service.remove_recipe_from_plan(
                    self.user_data._id, meal_plan.recipe_id
                )
                
                return True
            
            return False
        except Exception as e:
            print(f"Error al eliminar el plan de comida: {e}")
            return False 