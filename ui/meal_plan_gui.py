import tkinter as tk
from tkinter import ttk, messagebox
from utils.styles import COLORS

class MealPlanGUI:
    def __init__(self, root, user_data, day, meal_type):
        self.root = root
        self.user_data = user_data
        self.day = day
        self.meal_type = meal_type
        self.controller = None
        self.current_meal_plan = None
        
        self.setup_window()
        self.create_widgets()
        
        # Inicializar el controlador
        from controllers.meal_plan_controller import MealPlanController
        self.controller = MealPlanController(user_data, day, meal_type)
        self.controller.set_gui(self)
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title(f"NutriPlan - Planificar {self.meal_type} para {self.day}")
        self.root.geometry("600x650")  # Aumentamos el tamaño para los nuevos elementos
        self.root.resizable(False, False)
        self.root.config(bg=COLORS['fondo'])
        
        # Configurar fuentes
        self.title_font = ("Helvetica", 14, "bold")
        self.subtitle_font = ("Helvetica", 12, "bold")
        self.normal_font = ("Helvetica", 10)
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text=f"Planificar {self.meal_type} para {self.day}",
            font=self.title_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro']
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para el plan actual
        current_plan_frame = tk.LabelFrame(
            main_frame,
            text="Plan Actual",
            font=self.subtitle_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro'],
            padx=10,
            pady=10
        )
        current_plan_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.current_plan_label = tk.Label(
            current_plan_frame,
            text="No hay receta seleccionada para este día y comida",
            font=self.normal_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro'],
            wraplength=500
        )
        self.current_plan_label.pack(pady=10)
        
        delete_button = tk.Button(
            current_plan_frame,
            text="Eliminar Plan",
            command=self.delete_meal_plan,
            bg=COLORS['rojo'],
            fg=COLORS['texto_claro'],
            padx=10
        )
        delete_button.pack(pady=(0, 10))
        
        # Frame para búsqueda y selección de recetas
        recipe_frame = tk.LabelFrame(
            main_frame,
            text="Seleccionar Receta",
            font=self.subtitle_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro'],
            padx=10,
            pady=10
        )
        recipe_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo de búsqueda
        search_frame = tk.Frame(recipe_frame, bg=COLORS['fondo'])
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="Buscar:",
            font=self.normal_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_entry = tk.Entry(search_frame, width=30, font=self.normal_font)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        search_button = tk.Button(
            search_frame,
            text="Buscar",
            command=lambda: self.on_search(None),
            bg=COLORS['morado'],
            fg=COLORS['texto_claro'],
            padx=10
        )
        search_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Lista de recetas
        recipe_list_frame = tk.Frame(recipe_frame, bg=COLORS['blanco'])
        recipe_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.recipe_listbox = tk.Listbox(
            recipe_list_frame,
            font=self.normal_font,
            selectmode=tk.SINGLE,
            height=8
        )
        self.recipe_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(recipe_list_frame, orient=tk.VERTICAL, command=self.recipe_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipe_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botón para agregar receta al día actual
        add_recipe_button = tk.Button(
            recipe_frame,
            text=f"Agregar Receta a {self.day}",
            command=self.add_recipe_to_current_day,
            bg=COLORS['verde'],
            fg=COLORS['texto_claro'],
            padx=15,
            pady=5,
            font=self.normal_font
        )
        add_recipe_button.pack(pady=(5, 10))
        
        # Frame para planificación semanal
        weekly_frame = tk.LabelFrame(
            main_frame,
            text="Planificación Semanal",
            font=self.subtitle_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro'],
            padx=10,
            pady=10
        )
        weekly_frame.pack(fill=tk.X, pady=(10, 10))
        
        # Checkbuttons para los días de la semana
        days_frame = tk.Frame(weekly_frame, bg=COLORS['fondo'])
        days_frame.pack(fill=tk.X, pady=10)
        
        self.days_vars = {}
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        for day in days:
            var = tk.BooleanVar(value=(day == self.day))  # Seleccionar el día actual
            cb = tk.Checkbutton(
                days_frame,
                text=day,
                variable=var,
                onvalue=True,
                offvalue=False,
                bg=COLORS['fondo'],
                fg=COLORS['texto_oscuro'],
                selectcolor=COLORS['verde'],
                font=self.normal_font
            )
            cb.pack(side=tk.LEFT, padx=5)
            self.days_vars[day] = var
        
        # Botón para aplicar a todos los días seleccionados
        apply_button = tk.Button(
            weekly_frame,
            text="Aplicar a Días Seleccionados",
            command=self.save_weekly_plan,
            bg=COLORS['azul'],
            fg=COLORS['texto_claro'],
            padx=10,
            font=self.normal_font
        )
        apply_button.pack(pady=10)
        
        # Botones de acción principales
        button_frame = tk.Frame(main_frame, bg=COLORS['fondo'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            button_frame,
            text="Seleccionar Receta",
            command=self.save_meal_plan,
            bg=COLORS['verde'],
            fg=COLORS['texto_claro'],
            padx=10,
            font=self.normal_font
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="Cancelar",
            command=self.root.destroy,
            bg=COLORS['gris'],
            fg=COLORS['texto_oscuro'],
            padx=10,
            font=self.normal_font
        ).pack(side=tk.LEFT)
    
    def set_controller(self, controller):
        """Establece el controlador"""
        self.controller = controller
    
    def on_search(self, event):
        """Maneja el evento de búsqueda"""
        if self.controller:
            query = self.search_entry.get()
            self.controller.search_recipes(query)
    
    def update_recipe_list(self, recipes):
        """Actualiza la lista de recetas con los resultados de la búsqueda"""
        self.recipe_listbox.delete(0, tk.END)
        self.recipes = recipes
        
        for recipe in recipes:
            self.recipe_listbox.insert(tk.END, recipe.name)
    
    def set_current_meal_plan(self, meal_plan):
        """Muestra el plan de comida actual"""
        self.current_meal_plan = meal_plan
        if meal_plan and meal_plan.recipe:
            self.current_plan_label.config(
                text=f"Receta actual: {meal_plan.recipe.name}"
            )
        else:
            self.current_plan_label.config(
                text="No hay receta seleccionada para este día y comida"
            )
    
    def clear_current_meal_plan(self):
        """Limpia el plan de comida actual"""
        self.current_meal_plan = None
        self.current_plan_label.config(
            text="No hay receta seleccionada para este día y comida"
        )
    
    def add_recipe_to_current_day(self):
        """Agrega la receta seleccionada al día actual"""
        selection = self.recipe_listbox.curselection()
        
        if not selection:
            self.show_error("Por favor, selecciona una receta de la lista")
            return
        
        recipe = self.recipes[selection[0]]
        
        # Confirmar la acción
        if messagebox.askyesno(
            "Confirmar", 
            f"¿Deseas agregar '{recipe.name}' al {self.meal_type} del {self.day}?"
        ):
            if self.controller:
                if self.controller.save_meal_plan(recipe.recipe_id):
                    self.show_success(f"Receta '{recipe.name}' agregada exitosamente al {self.day}")
                    # Actualizar la visualización del plan actual
                    self.set_current_meal_plan_from_recipe(recipe)
                else:
                    self.show_error("Error al agregar la receta. Inténtalo de nuevo.")
    
    def set_current_meal_plan_from_recipe(self, recipe):
        """Actualiza la visualización del plan actual con la receta seleccionada"""
        self.current_plan_label.config(
            text=f"Receta actual: {recipe.name}"
        )
    
    def save_meal_plan(self):
        """Guarda el plan de comida seleccionado"""
        selection = self.recipe_listbox.curselection()
        
        if not selection:
            self.show_error("Por favor, selecciona una receta")
            return
        
        recipe = self.recipes[selection[0]]
        
        if self.controller:
            if self.controller.save_meal_plan(recipe.recipe_id):
                self.root.destroy()
    
    def save_weekly_plan(self):
        """Guarda el plan de comida para todos los días seleccionados"""
        selection = self.recipe_listbox.curselection()
        
        if not selection:
            self.show_error("Por favor, selecciona una receta")
            return
        
        recipe = self.recipes[selection[0]]
        
        # Obtener los días seleccionados
        selected_days = [day for day, var in self.days_vars.items() if var.get()]
        
        if not selected_days:
            self.show_error("Por favor, selecciona al menos un día de la semana")
            return
        
        if self.controller:
            success = True
            for day in selected_days:
                if not self.controller.save_meal_plan_for_day(recipe.recipe_id, day):
                    success = False
            
            if success:
                self.show_weekly_plan_success(selected_days)
                self.root.destroy()
    
    def delete_meal_plan(self):
        """Elimina el plan de comida actual"""
        if not self.current_meal_plan:
            self.show_error("No hay un plan de comida para eliminar")
            return
        
        if messagebox.askyesno("Eliminar Plan", "¿Estás seguro que deseas eliminar este plan de comida?"):
            if self.controller:
                if self.controller.delete_meal_plan():
                    self.root.destroy()
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        messagebox.showerror("Error", message)
    
    def show_success(self, message):
        """Muestra un mensaje de éxito"""
        messagebox.showinfo("Éxito", message)
        
    def show_weekly_plan_success(self, days):
        """Muestra un mensaje de éxito sobre el plan semanal"""
        days_str = ", ".join(days)
        messagebox.showinfo(
            "Plan Semanal", 
            f"La receta ha sido agregada al plan semanal para los días: {days_str}"
        )