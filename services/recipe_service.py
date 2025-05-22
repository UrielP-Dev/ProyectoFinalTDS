from repositories.recipe_repository import RecipeRepository

class RecipeService:
    def __init__(self):
        self.recipe_repo = RecipeRepository()
    
    def get_all_recipes(self):
        """Obtiene todas las recetas disponibles"""
        return self.recipe_repo.find_all()
    
    def get_recipe_by_id(self, recipe_id):
        """Obtiene una receta por su ID"""
        return self.recipe_repo.find_by_id(recipe_id)
    
    def search_recipes(self, query):
        """Busca recetas que coincidan con la consulta
        
        Actualmente busca por nombre aproximado. Si necesitas una búsqueda más 
        avanzada, esto se puede modificar para usar regex o índices de texto.
        """
        # Obtener todas las recetas
        all_recipes = self.recipe_repo.find_all()
        
        # Si la consulta está vacía, devolver todas
        if not query:
            return all_recipes
        
        # Filtrar las recetas que contienen la consulta en su nombre (case insensitive)
        query_lower = query.lower()
        return [r for r in all_recipes if query_lower in r.name.lower()]
    
    def add_recipe(self, recipe):
        """Añade una nueva receta"""
        return self.recipe_repo.save(recipe)
    
    def update_recipe(self, recipe_id, recipe):
        """Actualiza una receta existente"""
        return self.recipe_repo.update(recipe_id, recipe)
    
    def delete_recipe(self, recipe_id):
        """Elimina una receta"""
        return self.recipe_repo.delete(recipe_id)
 