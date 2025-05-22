class WeeklyPlan:
    def __init__(self, id=None, user_id=None, recipes=None, week="current"):
        self.id = id
        self.user_id = user_id
        self.recipes = recipes if recipes else []
        self.week = week
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenar en la base de datos"""
        plan_dict = {
            "user_id": self.user_id,
            "recipes": self.recipes,
            "week": self.week,
            "id": self.id  # Incluir id siempre, incluso si es None
        }
        
        return plan_dict
    
    @staticmethod
    def from_dict(data):
        """Crea un objeto WeeklyPlan desde un diccionario"""
        # Manejar caso donde _id está presente en lugar de id
        id_value = data.get("id")
        if id_value is None and "_id" in data:
            id_value = str(data.get("_id"))
            
        return WeeklyPlan(
            id=id_value,
            user_id=data.get("user_id"),
            recipes=data.get("recipes", []),
            week=data.get("week", "current")
        ) 