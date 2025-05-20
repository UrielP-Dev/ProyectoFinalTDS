class Recipe:
    def __init__(self, id=None, name="", ingredients=None, steps=None):
        self.id = id 
        self.name = name
        self.ingredients = ingredients if ingredients else []
        self.steps = steps if steps else []

    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "steps": self.steps
        }

    @staticmethod
    def from_dict(data):
        return Recipe(
            id=str(data.get("_id")),
            name=data.get("name", ""),
            ingredients=data.get("ingredients", []),
            steps=data.get("steps", [])
        )

    def __str__(self):
        return f"Receta: {self.name} (Ingredientes: {', '.join(self.ingredients)})"