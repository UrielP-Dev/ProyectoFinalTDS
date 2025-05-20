from repositories.recipe_repository import RecipeRepository

class SearchService:
    def __init__(self, recipe_repo: RecipeRepository):
        self.recipe_repo = recipe_repo

    def search_recipes(self, query: str):
        if not query:
            return self.recipe_repo.get_all_recipes()  # Si no hay consulta, mostrar todas
        return self.recipe_repo.search_recipes(query)

    def select_recipe(self, recipe_id: str):
        # En este caso, simplemente devolvemos la receta seleccionada
        # La lógica de asignación al plan semanal se manejará en el módulo de planificación
        recipes = self.recipe_repo.get_all_recipes()
        for recipe in recipes:
            if recipe.id == recipe_id:
                return recipe
        return None