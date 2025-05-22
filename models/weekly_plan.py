class WeeklyPlan:
    def __init__(self, id=None, user_id=None, recipes=None, week="current"):
        self.id = id
        self.user_id = user_id
        # recipes ahora es un diccionario {recipe_id: count}
        self.recipes = recipes if recipes else {}
        self.week = week

    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenar en la base de datos"""
        plan_dict = {
            "user_id": self.user_id,
            "recipes": self.recipes,
            "week": self.week,
            "id": self.id
        }
        return plan_dict

    @staticmethod
    def from_dict(data):
        """Crea un objeto WeeklyPlan desde un diccionario"""
        id_value = data.get("id")
        if id_value is None and "_id" in data:
            id_value = str(data.get("_id"))
        # recipes puede venir como lista (legacy) o dict (nuevo)
        recipes = data.get("recipes", {})
        if isinstance(recipes, list):
            # Convertir lista a dict con conteo
            recipe_counts = {}
            for rid in recipes:
                recipe_counts[rid] = recipe_counts.get(rid, 0) + 1
            recipes = recipe_counts
        return WeeklyPlan(
            id=id_value,
            user_id=data.get("user_id"),
            recipes=recipes,
            week=data.get("week", "current")
        )