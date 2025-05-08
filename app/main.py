import os
import sys
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

def initialize_database():
    """Verifica la conexión con la base de datos"""
    try:
        from repositories.mongo_connection import get_db_connection
        db = get_db_connection()
        return True
    except Exception as e:
        messagebox.showerror(
            "Error de conexión", 
            f"No se pudo conectar a la base de datos.\n\n"
            f"Error: {str(e)}\n\n"
            f"Verifique que:\n"
            f"1. El archivo .env contiene las credenciales correctas\n"
            f"2. Su conexión a internet está funcionando\n"
            f"3. Las direcciones IP están permitidas en MongoDB Atlas"
        )
        return False

def initialize_app():
    """Inicializa la aplicación"""
    try:
        # Comprobar si tenemos conexión a la base de datos
        if not initialize_database():
            return
            
        # Inicializa la ventana principal
        root = tk.Tk()
        root.title("NutriPlan - Cargando...")
        
        # Configurar un icono si está disponible
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "..", "assets", "icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except Exception:
            pass  # Si no podemos cargar el icono, continuamos sin él
            
        # Cargar la ventana de login
        from ui.login_window import LoginWindow
        app = LoginWindow(root)
        
        # Iniciar el loop principal de Tkinter
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror(
            "Error de inicialización", 
            f"Ocurrió un error al iniciar la aplicación:\n{str(e)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    initialize_app() 