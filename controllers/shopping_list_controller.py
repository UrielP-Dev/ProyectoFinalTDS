# controllers/shopping_list_controller.py

class ShoppingListController:
    def __init__(self):
        pass

    def generar_lista_compras(self, seleccion_usuario):
        # Esto es un mock: genera una lista de prueba
        if seleccion_usuario.strip() == "":
            raise ValueError("Debes ingresar una semana o criterio válido.")
        
        # Simula ingredientes recolectados de recetas
        return ["pollo", "arroz", "cebolla", "tomate"]
