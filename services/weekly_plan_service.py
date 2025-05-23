from models.weekly_plan import WeeklyPlan
from repositories.weekly_plan_repository import WeeklyPlanRepository

class WeeklyPlanService:
    def __init__(self):
        self.weekly_plan_repo = WeeklyPlanRepository()
    
    def get_user_plan(self, user_id, week="current"):
        """Obtiene el plan semanal de un usuario"""
        return self.weekly_plan_repo.get_by_user(user_id, week)
    
    def add_recipe_to_plan(self, user_id, recipe_id, week="current"):
        """Añade una receta al plan semanal de un usuario"""
        return self.weekly_plan_repo.add_recipe_to_plan(user_id, recipe_id, week)
    
    def remove_recipe_from_plan(self, user_id, recipe_id, week="current"):
        """Elimina una receta del plan semanal de un usuario"""
        return self.weekly_plan_repo.remove_recipe_from_plan(user_id, recipe_id, week)
    
    def create_weekly_plan(self, user_id, recipes=None, week="current"):
        """Crea un nuevo plan semanal para un usuario"""
        weekly_plan = WeeklyPlan(
            user_id=user_id,
            recipes=recipes if recipes else [],
            week=week
        )
        return self.weekly_plan_repo.save(weekly_plan)
    
    def delete_weekly_plan(self, plan_id):
        """Elimina un plan semanal"""
        return self.weekly_plan_repo.delete(plan_id) 