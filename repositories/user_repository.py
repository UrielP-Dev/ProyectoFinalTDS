from models.user import User
from repositories.mongo_connection import get_db_connection

class UserRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.collection = self.db['users']
    
    def find_by_username(self, username):
        """Busca un usuario por su nombre de usuario"""
        user_data = self.collection.find_one({'username': username})
        if user_data:
            return User.from_dict(user_data, str(user_data['_id']))
        return None
    
    def find_by_email(self, email):
        """Busca un usuario por su correo electrónico"""
        user_data = self.collection.find_one({'email': email})
        if user_data:
            return User.from_dict(user_data, str(user_data['_id']))
        return None
    
    def save(self, user):
        """Guarda un nuevo usuario en la base de datos"""
        user_dict = user.to_dict()
        result = self.collection.insert_one(user_dict)
        user.user_id = str(result.inserted_id)
        return user 