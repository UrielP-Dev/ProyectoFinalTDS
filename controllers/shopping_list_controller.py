from services.shopping_list_service import ShoppingListService

class ShoppingListController:
    def __init__(self):
        self.service = ShoppingListService()

    def get_user_info(self, user_id):
        return self.service.get_user_info(user_id)

    def generate_shopping_list(self, user_id):
        return self.service.generate_shopping_list(user_id)
