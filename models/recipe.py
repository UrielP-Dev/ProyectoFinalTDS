class Recipe:
    def __init__(self, id=None, name="", description="", ingredients=None):
        self.id = id  # ObjectId de MongoDB
        self.name = name
        self.description = description
        self.ingredients = ingredients if ingredients else []  # Lista de diccionarios {name, quantity, unit}

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients
        }

    @staticmethod
    def from_dict(data):
        return Recipe(
            id=str(data.get("_id")),
            name=data.get("name", ""),
            description=data.get("description", ""),
            ingredients=data.get("ingredients", [])
        )

    def __str__(self):
        ingredients_str = ", ".join([f"{ing['name']} ({ing['quantity']} {ing['unit']})" for ing in self.ingredients])
        return f"Receta: {self.name} - {self.description} (Ingredientes: {ingredients_str})"