from services.search_service import SearchService

class SearchController:
    def __init__(self, search_service: SearchService, view):
        self.search_service = search_service
        self.view = view

    def search_recipes(self, query: str):
        recipes = self.search_service.search_recipes(query)
        self.view.update_recipe_list(recipes)

    def select_recipe(self, recipe_id: str):
        recipe = self.search_service.select_recipe(recipe_id)
        if recipe:
            self.view.on_recipe_selected(recipe)
        else:
            self.view.show_error("Receta no encontrada")