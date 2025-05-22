from services.recipe_service import RecipeService

class SearchController:
    def __init__(self, view):
        self.view = view
        self.recipe_service = RecipeService()
    
    def search_recipes(self, query):
        """
        Busca recetas según la consulta proporcionada
        Si la consulta está vacía, devuelve todas las recetas
        """
        if query.strip() == "":
            recipes = self.recipe_service.get_all_recipes()
        else:
            recipes = self.recipe_service.search_recipes(query)
            
        self.view.update_recipe_list(recipes)

    def select_recipe(self, recipe_id):
        """Selecciona una receta por su ID"""
        recipe = self.recipe_service.get_recipe_by_id(recipe_id)
        if recipe:
            self.view.on_recipe_selected(recipe)
        else:
            self.view.show_error("Receta no encontrada")