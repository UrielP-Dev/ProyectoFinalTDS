import tkinter as tk
from tkinter import messagebox
import threading
from utils.styles import COLORS
from ui.shopping_list_gui import ShoppingListGUI
from ui.recipe_gui import RecipeGUI


class WeeklyPlannerGUI:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.selected_recipe = None
        self.meal_cells = {}  # Diccionario para almacenar referencias a las celdas del calendario
        self._loading = False  # Flag para evitar múltiples cargas simultáneas

        self.root.title(f"NutriPlan - Planificador Semanal - Usuario: {user_data.username}")
        self.root.geometry("1200x800")

        self.main_frame = tk.Frame(self.root, bg=COLORS['fondo'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        top_panel = tk.Frame(self.main_frame, bg=COLORS['fondo'])
        top_panel.pack(fill=tk.X, pady=10)

        welcome_label = tk.Label(
            top_panel,
            text=f"Bienvenido(a) {user_data.fullname} al Planificador Semanal",
            font=("Helvetica", 14, "bold"),
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro']
        )
        welcome_label.pack(side=tk.LEFT, padx=20)

        # Botón para recargar el calendario con indicador de carga
        self.reload_button = tk.Button(
            top_panel,
            text="Recargar Planes",
            command=self.update_calendar_async,
            bg=COLORS['azul'],
            fg=COLORS['texto_claro'],
            padx=10
        )
        self.reload_button.pack(side=tk.RIGHT, padx=(0, 20))

        logout_button = tk.Button(
            top_panel,
            text="Cerrar Sesión",
            command=self.logout,
            bg=COLORS['rojo'],
            fg=COLORS['texto_claro'],
            padx=10
        )
        logout_button.pack(side=tk.RIGHT, padx=(0, 20))

        content_frame = tk.Frame(self.main_frame, bg=COLORS['fondo'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        left_panel = tk.Frame(content_frame, bg=COLORS['fondo'], width=250, padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel,
            text="Funciones",
            font=("Helvetica", 12, "bold"),
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro']
        ).pack(pady=(0, 10))

        self.create_function_button(left_panel, "Planificación Semanal",
                                    lambda: messagebox.showinfo("En desarrollo", "Módulo de Interfaz de Planificación Semanal en desarrollo."),
                                    COLORS['verde'])

        self.create_function_button(left_panel, "Gestión de Recetas",
                                    self.open_recipe_gui,
                                    COLORS['naranja'])

        self.create_function_button(left_panel, "Búsqueda de Recetas",
                                    self.open_search_gui,
                                    COLORS['morado'])

        self.create_function_button(left_panel, "Lista de Compras",
                                    self.open_shopping_list,
                                    COLORS['rojo'])

        right_panel = tk.Frame(content_frame, bg=COLORS['blanco'], padx=10, pady=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Título del calendario con indicador de carga
        title_frame = tk.Frame(right_panel, bg=COLORS['blanco'])
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.calendar_title = tk.Label(
            title_frame,
            text="Calendario Semanal de Comidas",
            font=("Helvetica", 12, "bold"),
            bg=COLORS['blanco'],
            fg=COLORS['texto_oscuro']
        )
        self.calendar_title.pack(side=tk.LEFT)
        
        # Indicador de carga
        self.loading_label = tk.Label(
            title_frame,
            text="",
            font=("Helvetica", 10),
            bg=COLORS['blanco'],
            fg=COLORS['azul']
        )
        self.loading_label.pack(side=tk.RIGHT)

        self.create_weekly_calendar(right_panel)
        # Cargar planes de comida existentes de forma asíncrona
        self.update_calendar_async()

    def create_function_button(self, parent, text, command, color):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=COLORS['texto_claro'],
            width=25,
            height=2,
            font=("Helvetica", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2
        )
        button.pack(pady=8, fill=tk.X)
        return button

    def create_weekly_calendar(self, parent):
        calendar_frame = tk.Frame(parent, bg=COLORS['blanco'])
        calendar_frame.pack(fill=tk.BOTH, expand=True)

        dias = ["", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        comidas = ["Desayuno", "Almuerzo", "Comida", "Merienda", "Cena"]

        for i, dia in enumerate(dias):
            label = tk.Label(
                calendar_frame,
                text=dia,
                font=("Helvetica", 10, "bold"),
                bg=COLORS['verde'] if i > 0 else COLORS['blanco'],
                fg=COLORS['texto_claro'] if i > 0 else COLORS['blanco'],
                padx=10,
                pady=5,
                borderwidth=1,
                relief=tk.RAISED if i > 0 else tk.FLAT,
                width=12
            )
            label.grid(row=0, column=i, sticky="nsew")

        for i, comida in enumerate(comidas):
            label = tk.Label(
                calendar_frame,
                text=comida,
                font=("Helvetica", 10, "bold"),
                bg=COLORS['morado'],
                fg=COLORS['texto_claro'],
                padx=5,
                pady=10,
                borderwidth=1,
                relief=tk.RAISED
            )
            label.grid(row=i+1, column=0, sticky="nsew")

            for j in range(1, 8):
                frame = tk.Frame(
                    calendar_frame,
                    bg=COLORS['blanco'],
                    borderwidth=1,
                    relief=tk.SUNKEN,
                    height=80
                )
                frame.grid(row=i+1, column=j, sticky="nsew", padx=1, pady=1)
                frame.grid_propagate(False)
                
                add_button = tk.Button(
                    frame,
                    text="+",
                    font=("Helvetica", 10),
                    bg=COLORS['blanco'],
                    command=lambda r=i+1, c=j: self.add_recipe(r, c)
                )
                add_button.pack(side=tk.BOTTOM, anchor="se", padx=2, pady=2)
                
                recipe_label = tk.Label(
                    frame,
                    text="",
                    bg=COLORS['blanco'],
                    wraplength=100,
                    justify=tk.CENTER
                )
                recipe_label.pack(expand=True)
                
                # Guardar referencia a la celda
                cell_key = (i, j-1)  # (tipo_comida_index, dia_index)
                self.meal_cells[cell_key] = recipe_label

        for i in range(len(comidas) + 1):
            calendar_frame.grid_rowconfigure(i, weight=1)
        for i in range(len(dias)):
            calendar_frame.grid_columnconfigure(i, weight=1)

    def add_recipe(self, row, col):
        """Abre la ventana de planificación de comidas de forma optimizada"""
        from ui.meal_plan_gui import MealPlanGUI
        
        meal_types = ["Desayuno", "Almuerzo", "Comida", "Merienda", "Cena"]
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        meal_type = meal_types[row - 1]
        day = days[col - 1]
        
        # Abrir ventana para añadir receta al día y comida seleccionados
        meal_plan_root = tk.Toplevel(self.root)
        meal_plan_gui = MealPlanGUI(meal_plan_root, self.user_data, day, meal_type)
        
        # Callback para actualizar el calendario cuando se cierre la ventana
        def on_window_close():
            self.update_calendar_async()
        
        meal_plan_root.protocol("WM_DELETE_WINDOW", lambda: [meal_plan_root.destroy(), on_window_close()])

    def open_shopping_list(self):
        shopping_root = tk.Toplevel(self.root)
        ShoppingListGUI(shopping_root, self.user_data)

    def open_recipe_gui(self):
        recipe_root = tk.Toplevel(self.root)
        RecipeGUI(recipe_root, self.user_data)
        
    def open_search_gui(self):
        from ui.search_gui import SearchGUI
        from controllers.search_controller import SearchController
        
        search_root = tk.Toplevel(self.root)
        search_gui = SearchGUI(search_root, self.on_recipe_selected)
        controller = SearchController(search_gui)
        search_gui.set_controller(controller)
    
    def on_recipe_selected(self, recipe):
        """Callback que se ejecuta cuando se selecciona una receta en la búsqueda"""
        # Guardar la receta seleccionada para usarla al añadir a una comida
        self.selected_recipe = recipe
        messagebox.showinfo("Receta Seleccionada", f"Receta '{recipe}' seleccionada. Ahora puedes añadirla a una comida del planificador.")
    
    def update_calendar_async(self):
        """Actualiza el calendario de forma asíncrona para no bloquear la UI"""
        if self._loading:
            return  # Evitar múltiples cargas simultáneas
        
        self._loading = True
        self.show_loading(True)
        
        # Ejecutar la carga en un hilo separado
        thread = threading.Thread(target=self._load_calendar_data, daemon=True)
        thread.start()
    
    def _load_calendar_data(self):
        """Carga los datos del calendario en un hilo separado"""
        try:
            from services.meal_plan_service import MealPlanService
            from services.recipe_service import RecipeService
            
            meal_plan_service = MealPlanService()
            recipe_service = RecipeService()
            meal_plans = meal_plan_service.get_meal_plans_by_user(self.user_data._id)
            
            # Procesar los datos de los planes de comida
            processed_data = {}
            meal_types = ["Desayuno", "Almuerzo", "Comida", "Merienda", "Cena"]
            days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            
            for meal_plan in meal_plans:
                try:
                    day_index = days.index(meal_plan.day)
                    meal_type_index = meal_types.index(meal_plan.meal_type)
                    cell_key = (meal_type_index, day_index)
                    
                    # Obtener la receta de meal_plan
                    recipe = None
                    if meal_plan.recipe:
                        recipe = meal_plan.recipe
                    # Si no hay receta en el plan, buscarla por ID
                    elif meal_plan.recipe_id:
                        recipe = recipe_service.get_recipe_by_id(meal_plan.recipe_id)
                    
                    if recipe and hasattr(recipe, 'name'):
                        processed_data[cell_key] = {
                            'text': recipe.name,
                            'bg': COLORS['verde_claro']
                        }
                    else:
                        processed_data[cell_key] = {
                            'text': "Sin nombre",
                            'bg': COLORS['gris_claro']
                        }
                        
                except (ValueError, IndexError, AttributeError) as e:
                    print(f"Error al procesar plan de comida: {e}")
            
            # Actualizar la UI en el hilo principal
            self.root.after(0, lambda: self._update_calendar_ui(processed_data))
            
        except Exception as e:
            print(f"Error al cargar datos del calendario: {e}")
            self.root.after(0, lambda: self.show_loading(False))
    
    def _update_calendar_ui(self, processed_data):
        """Actualiza la UI del calendario con los datos procesados"""
        try:
            # Limpiar todas las celdas
            for label in self.meal_cells.values():
                label.config(text="", bg=COLORS['blanco'])
            
            # Actualizar celdas con los datos procesados
            for cell_key, data in processed_data.items():
                if cell_key in self.meal_cells:
                    self.meal_cells[cell_key].config(
                        text=data['text'],
                        bg=data['bg']
                    )
        
        except Exception as e:
            print(f"Error al actualizar UI del calendario: {e}")
        
        finally:
            self.show_loading(False)
            self._loading = False
    
    def show_loading(self, loading):
        """Muestra u oculta el indicador de carga"""
        if loading:
            self.loading_label.config(text="Cargando...")
            self.reload_button.config(state='disabled', text="Cargando...")
        else:
            self.loading_label.config(text="")
            self.reload_button.config(state='normal', text="Recargar Planes")

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que deseas cerrar sesión?"):
            self.root.destroy()
