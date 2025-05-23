class Recipe:

    def __init__(self, name, description, ingredients, steps, recipe_id = None):
        """_summary_

        Args:
            name (_string_): Nombre de la receta
            description (_string_): Una breve descripcion del platillo
            ingredients (_list_dict_): _Es un diccionario de datos que contiene detalles del ingrediente, como el nombre y la cantidad a utilizar
            steps (:list_): _Es una lista de cadenas que contiene los pasos con los que se va a realizar el platillo_
        """
        self.recipe_id = recipe_id
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.steps = steps
    
    def __str__(self):
        """Representación en string del objeto Recipe"""
        return self.name
    
    def __repr__(self):
        """Representación en string para depuración"""
        return f"Recipe(name='{self.name}', id={self.recipe_id})"
        
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            'name': self.name,
            'description': self.description,
            'ingredients': self.ingredients,
            'steps': self.steps                       
        }
        
    @classmethod
    def from_dict(cls, data, recipe_id = None):
        """Crea un objeto Recipe desde un diccionario"""
        return cls(
            name = data.get('name'),
            description = data.get('description'),
            ingredients = data.get('ingredients'), 
            steps = data.get('steps'),
            recipe_id = recipe_id
        )

