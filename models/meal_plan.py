class MealPlan:
    def __init__(self, id=None, user_id=None, day=None, meal_type=None, recipe_id=None, recipe=None):
        self.id = id
        self.user_id = user_id
        self.day = day
        self.meal_type = meal_type
        self.recipe_id = recipe_id
        self.recipe = recipe  # Objeto receta relacionado
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenar en la base de datos"""
        meal_dict = {
            "user_id": self.user_id,
            "day": self.day,
            "meal_type": self.meal_type,
            "recipe_id": self.recipe_id,
            "id": self.id  # Incluir id siempre, incluso si es None
        }
        
        return meal_dict
    
    @staticmethod
    def from_dict(data, recipe=None):
        """Crea un objeto MealPlan desde un diccionario"""
        # Manejar caso donde _id está presente en lugar de id
        id_value = data.get("id")
        if id_value is None and "_id" in data:
            id_value = str(data.get("_id"))
            
        return MealPlan(
            id=id_value,
            user_id=data.get("user_id"),
            day=data.get("day"),
            meal_type=data.get("meal_type"),
            recipe_id=data.get("recipe_id"),
            recipe=recipe
        ) 