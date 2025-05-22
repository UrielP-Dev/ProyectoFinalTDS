import tkinter as tk
from tkinter import ttk, messagebox
import threading
from utils.styles import COLORS

class MealPlanGUI:
    def __init__(self, root, user_data, day, meal_type):
        self.root = root
        self.user_data = user_data
        self.day = day
        self.meal_type = meal_type
        self.controller = None
        self.current_meal_plan = None
        self.recipes = []
        self._loading_recipes = False
        self._loading_plan = False
        
        self.setup_window()
        self.create_widgets()
        
        # Inicializar el controlador y cargar datos de forma asíncrona
        self.initialize_async()
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title(f"NutriPlan - Planificar {self.meal_type} para {self.day}")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        self.root.config(bg=COLORS['fondo'])
        
        # Configurar fuentes
        self.title_font = ("Helvetica", 14, "bold")
        self.subtitle_font = ("Helvetica", 12, "bold")
        self.normal_font = ("Helvetica", 10)
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame, 
            text=f"Planificar {self.meal_type} para {self.day}",
            font=self.title_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro']
        ).pack(pady=(0, 20))
        
        # Plan actual
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
            text="Cargando plan...",
            font=self.normal_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro'],
            wraplength=500
        )
        self.current_plan_label.pack(pady=10)
        
        self.delete_button = tk.Button(
            current_plan_frame,
            text="Eliminar Plan",
            command=self.delete_meal_plan,
            bg=COLORS['rojo'],
            fg=COLORS['texto_claro'],
            padx=10,
            state='disabled'  # Deshabilitado hasta que se cargue el plan
        )
        self.delete_button.pack(pady=(0, 10))
        
        # Búsqueda de recetas
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
        
        self.search_button = tk.Button(
            search_frame,
            text="Buscar",
            command=lambda: self.on_search(None),
            bg=COLORS['morado'],
            fg=COLORS['texto_claro'],
            padx=10
        )
        self.search_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Lista de recetas con indicador de carga
        list_frame = tk.Frame(recipe_frame, bg=COLORS['blanco'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.recipe_listbox = tk.Listbox(
            list_frame,
            font=self.normal_font,
            selectmode=tk.SINGLE,
            height=8
        )
        self.recipe_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.recipe_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipe_listbox.config(yscrollcommand=scrollbar.set)
        
        # Indicador de carga para recetas
        self.recipe_loading_label = tk.Label(
            recipe_frame,
            text="Cargando recetas...",
            font=("Helvetica", 9),
            bg=COLORS['fondo'],
            fg=COLORS['azul']
        )
        self.recipe_loading_label.pack()
        
        # Botón para agregar receta al día actual
        self.add_button = tk.Button(
            recipe_frame,
            text=f"Agregar Receta a {self.day}",
            command=self.add_recipe_to_current_day,
            bg=COLORS['verde'],
            fg=COLORS['texto_claro'],
            padx=15,
            pady=5,
            font=self.normal_font,
            state='disabled'  # Deshabilitado hasta que se carguen las recetas
        )
        self.add_button.pack(pady=(5, 10))
        
        # Botón cancelar
        tk.Button(
            recipe_frame,
            text="Cancelar",
            command=self.root.destroy,
            bg=COLORS['gris'],
            fg=COLORS['texto_oscuro'],
            padx=10,
            font=self.normal_font
        ).pack()
    
    def initialize_async(self):
        """Inicializa el controlador y carga datos de forma asíncrona"""
        thread = threading.Thread(target=self._initialize_controller, daemon=True)
        thread.start()
    
    def _initialize_controller(self):
        """Inicializa el controlador en un hilo separado"""
        try:
            from controllers.meal_plan_controller import MealPlanController
            self.controller = MealPlanController(self.user_data, self.day, self.meal_type)
            self.controller.set_gui(self)
            
            # Cargar plan actual y recetas en paralelo
            self.load_current_meal_plan_async()
            self.load_recipes_async()
            
        except Exception as e:
            print(f"Error al inicializar controlador: {e}")
            self.root.after(0, lambda: self.current_plan_label.config(text="Error al cargar"))
    
    def load_current_meal_plan_async(self):
        """Carga el plan de comida actual de forma asíncrona"""
        if self._loading_plan:
            return
        
        self._loading_plan = True
        thread = threading.Thread(target=self._load_current_meal_plan, daemon=True)
        thread.start()
    
    def _load_current_meal_plan(self):
        """Carga el plan de comida actual en un hilo separado"""
        try:
            if self.controller:
                self.controller.load_current_meal_plan()
        except Exception as e:
            print(f"Error al cargar plan de comida: {e}")
            self.root.after(0, lambda: self.current_plan_label.config(text="Error al cargar plan"))
        finally:
            self._loading_plan = False
    
    def load_recipes_async(self, search_term=""):
        """Carga las recetas de forma asíncrona"""
        if self._loading_recipes:
            return
        
        self._loading_recipes = True
        self.root.after(0, lambda: self.recipe_loading_label.config(text="Cargando recetas..."))
        
        thread = threading.Thread(target=lambda: self._load_recipes(search_term), daemon=True)
        thread.start()
    
    def _load_recipes(self, search_term=""):
        """Carga las recetas en un hilo separado"""
        try:
            if self.controller:
                self.controller.search_recipes(search_term)
        except Exception as e:
            print(f"Error al cargar recetas: {e}")
            self.root.after(0, lambda: self.recipe_loading_label.config(text="Error al cargar recetas"))
        finally:
            self._loading_recipes = False
    
    def on_search(self, event):
        """Maneja el evento de búsqueda de forma asíncrona"""
        search_term = self.search_entry.get()
        self.load_recipes_async(search_term)
    
    def update_recipe_list(self, recipes):
        """Actualiza la lista de recetas (llamado desde el hilo principal)"""
        def update_ui():
            self.recipe_listbox.delete(0, tk.END)
            self.recipes = recipes
            for r in recipes:
                self.recipe_listbox.insert(tk.END, r.name)
            
            self.recipe_loading_label.config(text="")
            self.add_button.config(state='normal')
        
        self.root.after(0, update_ui)
    
    def set_current_meal_plan(self, meal_plan):
        """Muestra el plan de comida actual (llamado desde el hilo principal)"""
        def update_ui():
            self.current_meal_plan = meal_plan
            if meal_plan and meal_plan.recipe:
                self.current_plan_label.config(text=f"Receta actual: {meal_plan.recipe.name}")
                self.delete_button.config(state='normal')
            else:
                self.current_plan_label.config(text="No hay receta seleccionada para este día y comida")
                self.delete_button.config(state='disabled')
        
        self.root.after(0, update_ui)
    
    def add_recipe_to_current_day(self):
        """Agrega la receta seleccionada al día actual"""
        sel = self.recipe_listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona una receta primero.")
            return
        
        recipe = self.recipes[sel[0]]
        if messagebox.askyesno(
            "Confirmar", f"¿Agregar '{recipe.name}' al {self.meal_type} de {self.day}?"
        ):
            # Deshabilitar botón mientras se guarda
            self.add_button.config(state='disabled', text="Guardando...")
            
            # Ejecutar guardado en hilo separado
            thread = threading.Thread(
                target=lambda: self._save_meal_plan(recipe.recipe_id), 
                daemon=True
            )
            thread.start()
    
    def _save_meal_plan(self, recipe_id):
        """Guarda el plan de comida en un hilo separado"""
        try:
            if self.controller and self.controller.save_meal_plan(recipe_id):
                self.root.after(0, lambda: [
                    messagebox.showinfo("Éxito", "Receta agregada correctamente."),
                    self.load_current_meal_plan_async()
                ])
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo guardar la receta."))
        except Exception as e:
            print(f"Error al guardar plan de comida: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", "Error al guardar la receta."))
        finally:
            self.root.after(0, lambda: self.add_button.config(
                state='normal', 
                text=f"Agregar Receta a {self.day}"
            ))
    
    def delete_meal_plan(self):
        """Elimina el plan de comida actual"""
        if not self.current_meal_plan:
            messagebox.showerror("Error", "No hay plan para eliminar.")
            return
        
        if messagebox.askyesno("Eliminar", "¿Estás seguro?"):
            # Deshabilitar botón mientras se elimina
            self.delete_button.config(state='disabled', text="Eliminando...")
            
            # Ejecutar eliminación en hilo separado
            thread = threading.Thread(target=self._delete_meal_plan, daemon=True)
            thread.start()
    
    def _delete_meal_plan(self):
        """Elimina el plan de comida en un hilo separado"""
        try:
            if self.controller and self.controller.delete_meal_plan():
                self.root.after(0, lambda: [
                    messagebox.showinfo("Eliminado", "Plan eliminado correctamente."),
                    self.root.destroy()
                ])
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo eliminar el plan."))
        except Exception as e:
            print(f"Error al eliminar plan de comida: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", "Error al eliminar el plan."))
        finally:
            self.root.after(0, lambda: self.delete_button.config(state='normal', text="Eliminar Plan"))