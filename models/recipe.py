class Recipe:
    def __init__(self, name, ingredients, steps):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            ingredients=data.get("ingredients", []),
            steps=data.get("steps", [])
        )
