from repositories.recipe_repository import RecipeRepository
from models.recipe import Recipe

class RecipeController:
    def __init__(self, view):
        self.view = view
        self.recipe_repository = RecipeRepository()
        
    #Proceso de creacion (CREATE)
    def register_recipe(self, name, description, ingredients, steps):
        """Registra una nueva receta"""
        # Verificar si la receta ya existe
        existing_recipe = self.recipe_repository.find_by_name(name)
        if existing_recipe:
            self.view.show_error("Ya hay una receta registrada con este nombre")
            return

        # Crear nueva receta
        new_recipe = Recipe(
            name=name,
            description=description,
            ingredients=ingredients,
            steps=steps
        )

        # Guardar en la base de datos
        try:
            self.recipe_repository.save(new_recipe)
            # Mostrar mensaje de exito
            self.view.show_success("Registro exitoso, Receta guardada")
        except Exception as e:
            self.view.show_error(f"No se pudo guardar la receta: {str(e)}")

    #Proceso de lectura de datos (READ)
    def get_all_recipes(self):
        """Obtiene todas las recetas almacenadas"""
        try:
            recipes = self.recipe_repository.find_all()
            return recipes
        except Exception as e:
            self.view.show_error(f"No se pudieron obtener las recetas: {str(e)}")
            return []
       
    #Proceso de actualizacion de los datos (UPDATE)
    def get_recipe_by_name(self, name):
        """Obtiene una receta por medio de su nombre"""
        try:
            recipe = self.recipe_repository.find_by_name(name)
            return recipe
        except Exception as e:
            self.view.show_error(f"No se pudo obtener la receta: {str(e)}")  
            return None
        
    def update_recipe(self, recipe_id, name, description, ingredients, steps):
        """Actualiza una receta existente"""
        try:
            update_recipe = Recipe(
                name=name,
                description=description,
                ingredients=ingredients,
                steps=steps,
                recipe_id=recipe_id
            )
            
            success = self.recipe_repository.update(recipe_id, update_recipe)
            if success:
                self.view.show_success("Receta actualizada correctamente")
            else:
                self.view.show_error("No se puede actualizar la receta")
        except Exception as e:
            self.view.show_error(f"Error al actualizar la receta: {str(e)}")
      
    #Proceso de eliminacion (DELETE)
    def delete_recipe(self, recipe_id):
        """Elimina una receta por su ID"""
        try:
            success = self.recipe_repository.delete(recipe_id)
            if success:
                self.view.show_success("Receta eliminada correctamente")
            else:
                self.view.show_error("No se pudo eliminar la receta")            
        except Exception as e:
            self.view.show_error(f"Error al eliminar la receta: {str(e)}")
        
    
    
    