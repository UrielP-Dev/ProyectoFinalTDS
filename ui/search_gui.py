# gui/search_gui.py
import tkinter as tk
from tkinter import messagebox, font
from controllers.search_controller import SearchController
from utils.styles import COLORS

class SearchGUI:
    def __init__(self, root, on_select_callback):
        self.root = root
        self.on_select_callback = on_select_callback
        self.setup_window()
        self.controller = None  # Inicializamos como None
        self.create_search_widgets()

    def setup_window(self):
        """Configura las propiedades generales de la ventana"""
        self.root.title("NutriPlan - Búsqueda de Recetas")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.config(bg=COLORS['fondo'])

        # Configura fuentes
        self.title_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)

        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_search_widgets(self):
        """Crea los widgets de la ventana de búsqueda"""
        # Título
        title_frame = tk.Frame(self.main_frame, bg=COLORS['fondo'])
        title_frame.pack(pady=20)

        tk.Label(title_frame, text="NutriPlan", font=self.title_font, 
                 bg=COLORS['fondo'], fg=COLORS['morado']).pack()

        # Subtítulo
        tk.Label(self.main_frame, text="Búsqueda de Recetas", font=self.subtitle_font, 
                 bg=COLORS['fondo'], fg=COLORS['texto_oscuro']).pack(pady=(0, 20))

        # Marco central
        search_frame = tk.Frame(self.main_frame, bg=COLORS['blanco'], padx=30, pady=30, 
                                relief=tk.RIDGE, bd=1)
        search_frame.pack(fill=tk.BOTH, expand=True, padx=50)

        # Campo de búsqueda
        frame_busqueda = tk.Frame(search_frame, bg=COLORS['blanco'])
        frame_busqueda.pack(fill=tk.X, pady=(0, 20))

        tk.Label(frame_busqueda, text="Buscar:", anchor=tk.W, font=self.normal_font,
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(side=tk.LEFT)
        self.entry_busqueda = tk.Entry(frame_busqueda, font=self.normal_font)
        self.entry_busqueda.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.entry_busqueda.bind("<KeyRelease>", self.on_search)

        # Lista de recetas
        self.listbox_recetas = tk.Listbox(search_frame, height=10, 
                                          font=self.normal_font)
        self.listbox_recetas.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Botón de selección
        select_button = tk.Button(search_frame, text="Seleccionar Receta", font=self.normal_font,
                                  bg=COLORS['verde'], fg=COLORS['texto_claro'],
                                  activebackground=COLORS['verde'], activeforeground=COLORS['texto_claro'],
                                  relief=tk.FLAT, padx=20, pady=8, command=self.select_recipe)
        select_button.pack()

        # Lista para almacenar recetas
        self.recipes = []

    def set_controller(self, controller: SearchController):
        self.controller = controller  # Asignamos el controller aquí
        # Cargar todas las recetas al inicio
        self.controller.search_recipes("")

    def update_recipe_list(self, recipes):
        self.recipes = recipes
        self.listbox_recetas.delete(0, tk.END)
        for recipe in recipes:
            self.listbox_recetas.insert(tk.END, str(recipe))

    def on_search(self, event):
        if self.controller:  # Verificamos que el controller esté inicializado
            query = self.entry_busqueda.get()
            self.controller.search_recipes(query)

    def select_recipe(self):
        selection = self.listbox_recetas.curselection()
        if selection and self.controller:
            index = selection[0]
            recipe = self.recipes[index]
            self.on_select_callback(recipe)
            self.root.destroy()
        else:
            self.show_error("Por favor, selecciona una receta")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def on_recipe_selected(self, recipe):
        pass