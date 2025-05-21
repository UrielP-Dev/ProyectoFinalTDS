import tkinter as tk

from tkinter import ttk, messagebox
# Implementación prueba Sandy
from ui.shopping_list_gui import ShoppingListGUI


class WeeklyPlannerGUI:
    
    # Implementación prueba Sandy
    def open_shopping_list(self):
        """Abre la ventana de lista de compras"""
        shopping_root = tk.Toplevel(self.root)
        ShoppingListGUI(shopping_root, self.user_data)
    
    
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        
        
        self.root.title(f"NutriPlan - Planificador Semanal - Usuario: {user_data.username}")
        self.root.geometry("1000x600")
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        welcome_label = tk.Label(
            self.main_frame, 
            text=f"Bienvenido(a) {user_data.fullname} al Planificador Semanal",
            font=("Helvetica", 14, "bold")
        )
        welcome_label.pack(pady=20)
        
        tk.Label(
            self.main_frame,
            text="La interfaz del planificador semanal está en desarrollo...",
            font=("Helvetica", 12)
        ).pack(pady=10)

        # Botón para ir a la sección de recetas
        recipe_button = tk.Button(
            self.main_frame,
            text="Ir a Recetas",
            command=lambda: self.open_recipe_gui()  # Aquí se debería abrir la ventana de recetas
        )
        recipe_button.pack(pady=20)

        # Botón para cerrar sesión
        logout_button = tk.Button(
            self.main_frame,
            text="Cerrar Sesión",
            command=self.logout
        )
        logout_button.pack(pady=20)


        buttons_frame = tk.Frame(self.main_frame)
        buttons_frame.pack(pady=30)

        tk.Button(
            buttons_frame,
            text="Planificación Semanal (Uriel)",
            width=30,
            command=lambda: messagebox.showinfo("En desarrollo", "Módulo de Interfaz de Planificación Semanal en desarrollo.")
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            buttons_frame,
            text="Gestión de Recetas (Edgar)",
            width=30,
            command=lambda: messagebox.showinfo("En desarrollo", "Módulo de Gestión de Recetas en desarrollo.")
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            buttons_frame,
            text="Búsqueda y Selección de Recetas (Fer)",
            width=30,
            command=lambda: messagebox.showinfo("En desarrollo", "Módulo de Búsqueda y Selección de Recetas en desarrollo.")
        ).grid(row=1, column=0, padx=10, pady=5)
        
        """ IMPLEMENTACIÓN SANDY
        tk.Button(
            buttons_frame,
            text="Generación de Lista de Compras (Sandra)",
            width=30,
            command=lambda: messagebox.showinfo("En desarrollo", "Módulo de Generación de Lista de Compras en desarrollo.")
        ).grid(row=1, column=1, padx=10, pady=5)
        """
        tk.Button(
            buttons_frame,
            text="Generación de Lista de Compras (Sandra)",
            width=30,
            command=self.open_shopping_list
        ).grid(row=1, column=1, padx=10, pady=5)


    def logout(self):
        """Cierra la sesión y regresa a la pantalla de login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que deseas cerrar sesión?"):
            self.root.destroy()

