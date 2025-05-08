from repositories.user_repository import UserRepository
from models.user import User
import hashlib

class LoginController:
    def __init__(self, view):
        self.view = view
        self.user_repository = UserRepository()
    
    def validate_login(self, username, password):
        """Valida las credenciales del usuario"""
        # Encriptar contraseña para comparar con la almacenada
        hashed_password = self._hash_password(password)
        
        # Buscar usuario en la base de datos
        user = self.user_repository.find_by_username(username)
        
        if not user:
            self.view.show_error("Usuario no encontrado")
            return
        
        if user.password != hashed_password:
            self.view.show_error("Contraseña incorrecta")
            return
        
        # Si las credenciales son correctas, abre la aplicación principal
        self.view.open_main_app(user)
    
    def register_user(self, fullname, email, username, password):
        """Registra un nuevo usuario"""
        # Verificar si el usuario ya existe
        existing_user = self.user_repository.find_by_username(username)
        if existing_user:
            self.view.show_error("El nombre de usuario ya está en uso")
            return
        
        # Verificar si el email ya existe
        existing_email = self.user_repository.find_by_email(email)
        if existing_email:
            self.view.show_error("El correo electrónico ya está registrado")
            return
        
        # Encriptar contraseña
        hashed_password = self._hash_password(password)
        
        # Crear nuevo usuario
        new_user = User(
            username=username,
            password=hashed_password,
            fullname=fullname,
            email=email,
            role="user"  # Por defecto, rol de usuario
        )
        
        # Guardar en la base de datos
        self.user_repository.save(new_user)
        
        # Mostrar mensaje de éxito y volver a la pantalla de login
        self.view.show_success("Registro exitoso. Ya puedes iniciar sesión.")
        self.view.show_login()
    
    def _hash_password(self, password):
        """Encripta la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest() 