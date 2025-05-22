from models.recipe import Recipe
from repositories.mongo_connection import get_db_connection
from bson import ObjectId


class RecipeRepository:

    def __init__(self):
        self.db = get_db_connection()
        self.collection = self.db['recipes']
      
    def save(self, recipe):
        """_summary_

        Args:
            recipe (dict): Diccionario con la informacion de la receta que se desea guardar
        """
        recipe_dict = recipe.to_dict()
        result = self.collection.insert_one(recipe_dict)
        recipe.recipe_id = str(result.inserted_id)
        return recipe
    
    def find_by_id(self, recipe_id):
        """Busca una receta por su ID

        Args:
            recipe_id (str): ID de la receta a buscar
        """
        try:
            if isinstance(recipe_id, str):
                try:
                    # Intentar primero con ObjectId
                    recipe_data = self.collection.find_one({'_id': ObjectId(recipe_id)})
                    if recipe_data:
                        return Recipe.from_dict(recipe_data, str(recipe_data['_id']))
                except:
                    # Si falla, intentar con recipe_id como string
                    recipe_data = self.collection.find_one({'recipe_id': recipe_id})
            else:
                recipe_data = self.collection.find_one({'recipe_id': recipe_id})
                
            if recipe_data:
                return Recipe.from_dict(recipe_data, str(recipe_data['_id']))
            
            # Si todo lo anterior falla, intentar una búsqueda por cualquier campo que contenga el id
            print(f"Buscando receta con id: {recipe_id}")
            recipe_data = self.collection.find_one({'$or': [
                {'_id': recipe_id},
                {'recipe_id': recipe_id},
                {'id': recipe_id}
            ]})
            
            if recipe_data:
                return Recipe.from_dict(recipe_data, str(recipe_data['_id']))
                
            return None
        except Exception as e:
            print(f"Error al buscar receta por ID: {str(e)}")
            return None
         
    def find_by_name(self, name):
        """_summary_

        Args:
            name (string): Nombre de la receta que se desea buscar
        """
        recipe_data = self.collection.find_one({'name': name})
        if recipe_data:
            return Recipe.from_dict(recipe_data, str(recipe_data['_id']))
        return None
    
    def find_all(self):
        """Recupera todas las recetas almacenadas en la colección recipes."""
        recipes = []
        for recipe_data in self.collection.find():
            recipes.append(Recipe.from_dict(recipe_data, str(recipe_data['_id'])))
        return recipes
        
    def update(self, recipe_id, recipe):
        """Actualiza una receta existente en la coleccion recipes por su id

        Args:
            recipe_id (str): ID de la receta a actualizar
            recipe (Recipe): Objeto Recipe con los nuevos datos
        """
        recipe_dict = recipe.to_dict()
        # No se actualiza el _id
        
        if '_id' in recipe_dict:
            del recipe_dict['_id']
        result = self.collection.update_one(
            {'_id': ObjectId(recipe_id)},
            {'$set': recipe_dict}
        )
        
        return result.modified_count > 0
    
    def delete(self, recipe_id):
        """Elimina una receta de la colección recipes por su id.

        Args:
            id (str): ID de la receta a eliminar
        """
        result = self.collection.delete_one({'_id': ObjectId(recipe_id)})
        return result.deleted_count > 0

