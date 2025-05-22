import tkinter as tk
from tkinter import ttk, messagebox
from utils.styles import COLORS
from services.weekly_plan_service import WeeklyPlanService
from services.recipe_service import RecipeService

class WeeklyPlanView:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.weekly_plan_service = WeeklyPlanService()
        self.recipe_service = RecipeService()
        
        self.setup_window()
        self.create_widgets()
        
        # Inicializar el controlador
        from controllers.weekly_plan_controller import WeeklyPlanController
        self.controller = WeeklyPlanController(self, user_data)
        
        self.load_weekly_plan()
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("NutriPlan - Plan Semanal")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.config(bg=COLORS['fondo'])
        
        # Configurar fuentes
        self.title_font = ("Helvetica", 16, "bold")
        self.day_font = ("Helvetica", 14, "bold")
        self.meal_font = ("Helvetica", 12, "bold")
        self.recipe_font = ("Helvetica", 11)
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Plan Semanal de Alimentación",
            font=self.title_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro']
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para el plan semanal
        self.week_frame = tk.Frame(main_frame, bg=COLORS['fondo'])
        self.week_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones de acción
        button_frame = tk.Frame(main_frame, bg=COLORS['fondo'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="Cerrar",
            command=self.root.destroy,
            bg=COLORS['gris'],
            fg=COLORS['texto_oscuro'],
            padx=15,
            pady=5,
            font=self.recipe_font
        ).pack(side=tk.RIGHT)
    
    def load_weekly_plan(self):
        """Carga y muestra el plan semanal del usuario"""
        # Limpiar el frame actual
        for widget in self.week_frame.winfo_children():
            widget.destroy()
        
        # Obtener el plan semanal
        weekly_plan = self.weekly_plan_service.get_user_plan(self.user_data.id)
        
        if not weekly_plan or not weekly_plan.recipes:
            no_plan_label = tk.Label(
                self.week_frame,
                text="No tienes un plan semanal configurado",
                font=self.day_font,
                bg=COLORS['fondo'],
                fg=COLORS['texto_oscuro']
            )
            no_plan_label.pack(pady=100)
            return
        
        # Obtener todas las recetas del plan
        recipe_ids = weekly_plan.recipes
        recipes = {}
        for recipe_id in recipe_ids:
            recipe = self.recipe_service.get_recipe_by_id(recipe_id)
            if recipe:
                recipes[recipe_id] = recipe
        
        # Días de la semana
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        # Tipos de comida
        meal_types = ["Desayuno", "Almuerzo", "Cena", "Snack"]
        
        # Crear una tabla para mostrar el plan
        for i, day in enumerate(days):
            # Frame para el día
            day_frame = tk.LabelFrame(
                self.week_frame,
                text=day,
                font=self.day_font,
                bg=COLORS['fondo'],
                fg=COLORS['texto_oscuro'],
                padx=10,
                pady=10
            )
            day_frame.grid(row=i, column=0, sticky="we", padx=5, pady=5)
            
            # Configurar el peso de las columnas
            self.week_frame.columnconfigure(0, weight=1)
            
            # Mostrar comidas para este día
            meal_frame = tk.Frame(day_frame, bg=COLORS['fondo'])
            meal_frame.pack(fill=tk.X)
            
            # Buscar planes para este día
            for j, meal_type in enumerate(meal_types):
                meal_label = tk.Label(
                    meal_frame,
                    text=f"{meal_type}:",
                    font=self.meal_font,
                    bg=COLORS['fondo'],
                    fg=COLORS['texto_oscuro'],
                    width=10,
                    anchor="w"
                )
                meal_label.grid(row=0, column=j*2, sticky="w", padx=(0 if j == 0 else 10, 5))
                
                # Buscar plan para este día y tipo de comida
                meal_plan = self.user_data.meal_plans.get(f"{day}_{meal_type}")
                
                if meal_plan and meal_plan.recipe_id in recipes:
                    recipe = recipes[meal_plan.recipe_id]
                    recipe_label = tk.Label(
                        meal_frame,
                        text=recipe.name,
                        font=self.recipe_font,
                        bg=COLORS['blanco'],
                        fg=COLORS['texto_oscuro'],
                        padx=5,
                        pady=3,
                        relief=tk.RIDGE
                    )
                else:
                    recipe_label = tk.Label(
                        meal_frame,
                        text="No planificado",
                        font=self.recipe_font,
                        bg=COLORS['gris_claro'],
                        fg=COLORS['texto_oscuro'],
                        padx=5,
                        pady=3,
                        relief=tk.RIDGE
                    )
                
                recipe_label.grid(row=0, column=j*2+1, sticky="w")
                
                # Configurar el peso de las columnas
                meal_frame.columnconfigure(j*2+1, weight=1)
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        messagebox.showerror("Error", message)
    
    def show_success(self, message):
        """Muestra un mensaje de éxito"""
        messagebox.showinfo("Éxito", message) 