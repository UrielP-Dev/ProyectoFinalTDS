import tkinter as tk
from tkinter import messagebox, font
import sys
import os
import utils.session as session  

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.login_controller import LoginController
from utils.styles import COLORS
from ui.register_window import RegisterWindow  

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.controller = LoginController(self)
        self.setup_window()
        self.show_login()

    def setup_window(self):
        self.root.title("NutriPlan - Sistema de Planificación de Comidas")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.config(bg=COLORS['fondo'])
        self.title_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        self.main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_login(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        welcome_frame = tk.Frame(self.main_frame, bg=COLORS['fondo'], padx=20, pady=20)
        welcome_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_frame = tk.Frame(welcome_frame, bg=COLORS['fondo'])
        title_frame.pack(pady=20)
        
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
        login_frame = tk.Frame(self.main_frame, bg=COLORS['blanco'], padx=30, pady=30, 
                              relief=tk.RIDGE, bd=1)
        login_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(login_frame, text="Iniciar Sesión", font=self.subtitle_font, 
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(pady=(0, 20))
        
        tk.Label(login_frame, text="Usuario:", anchor=tk.W, 
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.username_entry = tk.Entry(login_frame, font=self.normal_font)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(login_frame, text="Contraseña:", anchor=tk.W, 
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
        self.password_entry = tk.Entry(login_frame, show="•", font=self.normal_font)
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        login_button = tk.Button(login_frame, text="Entrar", font=self.normal_font,
                             bg=COLORS['verde'], fg=COLORS['texto_claro'],
                             activebackground=COLORS['verde'], activeforeground=COLORS['texto_claro'],
                             relief=tk.FLAT, padx=20, pady=8, command=self.login)
        login_button.pack(pady=10)
        
        register_frame = tk.Frame(login_frame, bg=COLORS['blanco'])
        register_frame.pack(pady=10)
        
        tk.Label(register_frame, text="¿No tienes cuenta? ", 
                 font=self.normal_font, bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(side=tk.LEFT)
        
        register_link = tk.Label(register_frame, text="Regístrate", font=self.normal_font, 
                             bg=COLORS['blanco'], fg=COLORS['morado'], cursor="hand2")
        register_link.pack(side=tk.LEFT)
        register_link.bind("<Button-1>", lambda e: self.show_register())

    def show_register(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        RegisterWindow(self.main_frame, self.show_login, self.controller)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Por favor ingresa usuario y contraseña")
            return
        self.controller.validate_login(username, password)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success(self, message):
        messagebox.showinfo("Éxito", message)

    def open_main_app(self, user_data):
        import utils.session as session
        session.user_id = user_data._id  
        self.root.withdraw()
        from ui.weekly_planner_gui import WeeklyPlannerGUI
        main_window = tk.Toplevel(self.root)
        main_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        app = WeeklyPlannerGUI(main_window, user_data)
        print(session.user_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

