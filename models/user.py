class User:
    def __init__(self, username, password, fullname, email, role='user',_id=None):
        self._id = _id
        self.username = username
        self.password = password  
        self.fullname = fullname
        self.email = email
        self.role = role
    
    def to_dict(self):
        """Convierte el objeto a un diccionario (útil para almacenamiento)"""
        return {
            'username': self.username,
            'password': self.password,
            'fullname': self.fullname,
            'email': self.email,
            'role': self.role
        }
    
    @classmethod
    def from_dict(cls, data, user_id=None):
        """Crea un objeto User desde un diccionario"""
        return cls(
            username=data.get('username'),
            password=data.get('password'),
            fullname=data.get('fullname'),
            email=data.get('email'),
            role=data.get('role', 'user'),
            _id=user_id
        ) 