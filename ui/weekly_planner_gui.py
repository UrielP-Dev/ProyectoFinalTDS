import tkinter as tk
from tkinter import ttk, messagebox

class WeeklyPlannerGUI:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        
        # Configurar ventana principal
        self.root.title(f"NutriPlan - Planificador Semanal - Usuario: {user_data.username}")
        self.root.geometry("1000x600")
        
        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Mensaje de bienvenida temporal
        welcome_label = tk.Label(
            self.main_frame, 
            text=f"Bienvenido(a) {user_data.fullname} al Planificador Semanal",
            font=("Helvetica", 14, "bold")
        )
        welcome_label.pack(pady=20)
        
        # Mensaje temporal mientras se desarrolla esta sección
        tk.Label(
            self.main_frame,
            text="La interfaz del planificador semanal está en desarrollo...",
            font=("Helvetica", 12)
        ).pack(pady=10)
        
        # Botón para cerrar sesión
        logout_button = tk.Button(
            self.main_frame,
            text="Cerrar Sesión",
            command=self.logout
        )
        logout_button.pack(pady=20)
    
    def logout(self):
        """Cierra la sesión y regresa a la pantalla de login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que deseas cerrar sesión?"):
            self.root.destroy() 