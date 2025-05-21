import tkinter as tk
from tkinter import messagebox, font
import sys
import os

# Añadimos la ruta raíz del proyecto al sys.path para poder importar otros módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.login_controller import LoginController
from utils.styles import COLORS

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.controller = LoginController(self)
        self.setup_window()
        self.show_login()  # Por defecto mostramos la pantalla de login
        
    def setup_window(self):
        """Configura las propiedades generales de la ventana"""
        self.root.title("NutriPlan - Sistema de Planificación de Comidas")
        self.root.geometry("1920x1080")
        self.root.resizable(False, False)
        self.root.config(bg=COLORS['fondo'])
        
        # Configura fonts
        self.title_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        
        # Frame principal que contendrá todas las vistas
        self.main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frames para login y registro (se mostrarán según la navegación)
        self.login_container = None
        self.register_container = None
    
    def show_login(self):
        """Muestra la pantalla de login"""
        # Limpiar pantalla anterior si existe
        if self.register_container:
            self.register_container.destroy()
            
        # Crear el contenedor de login si no existe
        if not self.login_container:
            self.login_container = tk.Frame(self.main_frame, bg=COLORS['fondo'])
            self.login_container.pack(fill=tk.BOTH, expand=True)
            self.create_login_widgets()
    
    def show_register(self):
        """Muestra la pantalla de registro"""
        # Limpiar pantalla anterior si existe
        if self.login_container:
            self.login_container.destroy()
            self.login_container = None
            
        # Crear el contenedor de registro si no existe
        if not self.register_container:
            self.register_container = tk.Frame(self.main_frame, bg=COLORS['fondo'])
            self.register_container.pack(fill=tk.BOTH, expand=True)
            self.create_register_widgets()
        
    def create_login_widgets(self):
        """Crea todos los widgets de la ventana de login"""
        # Sección de bienvenida (izquierda)
        welcome_frame = tk.Frame(self.login_container, bg=COLORS['fondo'], padx=20, pady=20)
        welcome_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Título con logo de colores
        title_frame = tk.Frame(welcome_frame, bg=COLORS['fondo'])
        title_frame.pack(pady=20)
        
        # Logos con colores representativos de alimentos
        logo_size = 20
        logo_frame = tk.Frame(title_frame, bg=COLORS['fondo'])
        logo_frame.pack()
        
        # Cada color representa un grupo de alimentos/beneficios
        for color in [COLORS['verde'], COLORS['rojo'], COLORS['naranja'], 
                     COLORS['morado'], COLORS['blanco']]:
            tk.Canvas(logo_frame, width=logo_size, height=logo_size, bg=color, 
                      highlightthickness=0).pack(side=tk.LEFT, padx=2)
        
        tk.Label(title_frame, text="NutriPlan", font=self.title_font, 
                 bg=COLORS['fondo'], fg=COLORS['morado']).pack(pady=5)
        
        # Mensaje de bienvenida
        tk.Label(welcome_frame, text="¡Bienvenido al Sistema de Planificación de Comidas!", 
                 font=self.subtitle_font, bg=COLORS['fondo'], fg=COLORS['texto_oscuro']).pack(pady=10)
        
        tk.Label(welcome_frame, text="Organiza tus comidas de manera nutritiva y balanceada.", 
                 wraplength=300, justify=tk.CENTER, bg=COLORS['fondo'], 
                 fg=COLORS['texto_oscuro']).pack(pady=5)
        
        # Información de beneficios por colores
        benefits_frame = tk.Frame(welcome_frame, bg=COLORS['fondo'], padx=10, pady=10)
        benefits_frame.pack(pady=20)
        
        benefits = [
            ("Verde", "Salud visual y digestiva"),
            ("Rojo", "Antioxidantes y desarrollo cerebral"),
            ("Naranja/Amarillo", "Vitamina C para sistema respiratorio"),
            ("Morado", "Protección celular"),
            ("Blanco", "Control de presión arterial")
        ]
        
        for i, (color_name, benefit) in enumerate(benefits):
            frame = tk.Frame(benefits_frame, bg=COLORS['fondo'])
            frame.pack(anchor=tk.W, pady=2)
            
            color_key = color_name.lower() if color_name.lower() in COLORS else 'naranja'
            
            tk.Canvas(frame, width=10, height=10, bg=COLORS[color_key], 
                      highlightthickness=0).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"{color_name}: {benefit}", font=self.normal_font, 
                     bg=COLORS['fondo'], fg=COLORS['texto_oscuro']).pack(side=tk.LEFT)
        
        # Sección de login (derecha)
        login_frame = tk.Frame(self.login_container, bg=COLORS['blanco'], padx=30, pady=30, 
                              relief=tk.RIDGE, bd=1)
        login_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(login_frame, text="Iniciar Sesión", font=self.subtitle_font, 
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(pady=(0, 20))
        
        # Campo de usuario
        tk.Label(login_frame, text="Usuario:", anchor=tk.W, 
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.username_entry = tk.Entry(login_frame, font=self.normal_font)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Campo de contraseña
        tk.Label(login_frame, text="Contraseña:", anchor=tk.W, 
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.password_entry = tk.Entry(login_frame, show="•", font=self.normal_font)
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Botón de login
        login_button = tk.Button(login_frame, text="Entrar", font=self.normal_font,
                             bg=COLORS['verde'], fg=COLORS['texto_claro'],
                             activebackground=COLORS['verde'], activeforeground=COLORS['texto_claro'],
                             relief=tk.FLAT, padx=20, pady=8, command=self.login)
        login_button.pack(pady=10)
        
        # Enlace para crear cuenta
        register_frame = tk.Frame(login_frame, bg=COLORS['blanco'])
        register_frame.pack(pady=10)
        
        tk.Label(register_frame, text="¿No tienes cuenta? ", 
                 font=self.normal_font, bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(side=tk.LEFT)
        
        register_link = tk.Label(register_frame, text="Regístrate", font=self.normal_font, 
                             bg=COLORS['blanco'], fg=COLORS['morado'], cursor="hand2")
        register_link.pack(side=tk.LEFT)
        register_link.bind("<Button-1>", lambda e: self.show_register())
    
    def create_register_widgets(self):
        """Crea todos los widgets de la ventana de registro"""
        # Título
        title_frame = tk.Frame(self.register_container, bg=COLORS['fondo'])
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="NutriPlan", font=self.title_font, 
                 bg=COLORS['fondo'], fg=COLORS['morado']).pack()
        
        # Formulario de registro
        register_frame = tk.Frame(self.register_container, bg=COLORS['blanco'], padx=30, pady=30,
                                relief=tk.RIDGE, bd=1)
        register_frame.pack(expand=True, padx=50)
        
        tk.Label(register_frame, text="Crear una cuenta", font=self.subtitle_font,
                bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(pady=(0, 20))
        
        # Nombre completo
        tk.Label(register_frame, text="Nombre completo:", anchor=tk.W,
                bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.fullname_entry = tk.Entry(register_frame, font=self.normal_font)
        self.fullname_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Correo electrónico
        tk.Label(register_frame, text="Correo electrónico:", anchor=tk.W,
                bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.email_entry = tk.Entry(register_frame, font=self.normal_font)
        self.email_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Nombre de usuario
        tk.Label(register_frame, text="Nombre de usuario:", anchor=tk.W,
                bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.reg_username_entry = tk.Entry(register_frame, font=self.normal_font)
        self.reg_username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Contraseña
        tk.Label(register_frame, text="Contraseña:", anchor=tk.W,
                bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.reg_password_entry = tk.Entry(register_frame, show="•", font=self.normal_font)
        self.reg_password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Confirmar contraseña
        tk.Label(register_frame, text="Confirmar contraseña:", anchor=tk.W,
                bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.confirm_password_entry = tk.Entry(register_frame, show="•", font=self.normal_font)
        self.confirm_password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Botones
        buttons_frame = tk.Frame(register_frame, bg=COLORS['blanco'])
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Botón para volver al login
        back_button = tk.Button(buttons_frame, text="Volver", font=self.normal_font,
                             bg=COLORS['borde'], fg=COLORS['texto_oscuro'],
                             relief=tk.FLAT, padx=15, pady=8, command=self.show_login)
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Botón para registrarse
        register_button = tk.Button(buttons_frame, text="Registrarse", font=self.normal_font,
                                bg=COLORS['morado'], fg=COLORS['texto_claro'],
                                activebackground=COLORS['morado'], activeforeground=COLORS['texto_claro'],
                                relief=tk.FLAT, padx=15, pady=8, command=self.register)
        register_button.pack(side=tk.RIGHT, padx=5)
    
    def login(self):
        """Maneja el evento de login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor ingresa usuario y contraseña")
            return
        
        # Llama al controlador para verificar las credenciales
        self.controller.validate_login(username, password)
    
    def register(self):
        """Maneja el evento de registro"""
        fullname = self.fullname_entry.get()
        email = self.email_entry.get()
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validación básica
        if not all([fullname, email, username, password, confirm_password]):
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        # Llama al controlador para registrar al usuario
        self.controller.register_user(fullname, email, username, password)
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        messagebox.showerror("Error", message)
    
    def show_success(self, message):
        """Muestra un mensaje de éxito"""
        messagebox.showinfo("Éxito", message)
    
    def open_main_app(self, user_data):
        """Cierra la ventana de login y abre la aplicación principal"""
        self.root.withdraw()  # Oculta la ventana de login
        
        # Crea una nueva ventana para la aplicación principal
        main_window = tk.Toplevel(self.root)
        main_window.protocol("WM_DELETE_WINDOW", self.root.destroy)  # Cierra la app al cerrar esta ventana
        
        # Aquí importaríamos el módulo de la aplicación principal
        from ui.weekly_planner_gui import WeeklyPlannerGUI
        app = WeeklyPlannerGUI(main_window, user_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()