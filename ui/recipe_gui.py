import tkinter as tk
from tkinter import ttk, messagebox
import sys
from controllers.recipe_controller import RecipeController
from utils.styles import COLORS
import select
from pip._vendor.rich.jupyter import display


class RecipeGUI:

    def __init__(self, root, user_data):
        
        self.root = root
        self.user_data = user_data
        
        BG_COLOR = COLORS['fondo']
        TEXT_COLOR = COLORS['texto_oscuro']
        BTN_COLOR = COLORS['morado']
        BTN_TEXT = COLORS['texto_claro']
        FRAME_COLOR = COLORS['blanco']
        BORDER_COLOR = COLORS['borde']
        
        style = ttk.Style()
        style.configure("Custom.TLabelframe", background=BG_COLOR, foreground=COLORS['morado'], font=("Arial", 12, "bold"))
        style.configure("Treeview", background=COLORS['blanco'], foreground=TEXT_COLOR, fieldbackground=COLORS['blanco'], font=("Arial", 10))
        style.configure("Treeview.Heading", background=COLORS['morado'], foreground=BTN_TEXT, font=("Arial", 11, "bold"))
        style.configure("Treeview", rowheight=32)
        
        self.editing_recipe_id = None
        self.ingredientes = []
        self.controller = RecipeController(self)
        
        self.root.title(f"NutriPlan - 📖 Gestor de Recetas de Cocina - Usuario: {user_data.username}")
        self.root.geometry("2900x1080")
        self.root.resizable(False, False)
        self.root.config(bg=BG_COLOR)
        
        # Usar un frame principal para contener los dos paneles
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)

        # Frame izquierdo: Formulario de recetas
        form_frame = tk.LabelFrame(main_frame, text="Añadir y Editar Recetas", bg=BG_COLOR, fg=TEXT_COLOR,
                       font=("Arial", 11, "bold"), padx=15, pady=15, labelanchor="n", relief=tk.GROOVE)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)

        # Frame derecho: Lista de recetas
        list_frame = tk.LabelFrame(main_frame, text="Lista de Recetas", bg=BG_COLOR, fg=TEXT_COLOR,
                       font=("Arial", 11, "bold"), padx=15, pady=15, labelanchor="n", relief=tk.GROOVE)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=0)

        # Configurar el grid para que ambos paneles se expandan
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)

        # --- Formulario de recetas ---
        # Nombre de la receta
        tk.Label(form_frame, text="Nombre de la receta:", bg=FRAME_COLOR, fg=TEXT_COLOR, anchor="w").grid(row=0, column=0, sticky="w")
        self.entry_nombre = tk.Entry(form_frame, width=40, bg=COLORS['blanco'], fg=TEXT_COLOR, relief=tk.FLAT, highlightbackground=BORDER_COLOR)
        self.entry_nombre.grid(row=0, column=1, sticky="ew", padx=5, pady=5, columnspan=5)

        # Descripción
        tk.Label(form_frame, text="Descripción:", bg=FRAME_COLOR, fg=TEXT_COLOR, anchor="w").grid(row=1, column=0, sticky="nw")
        self.entry_descripcion = tk.Text(form_frame, width=50, height=2, bg=COLORS['blanco'], fg=TEXT_COLOR, relief=tk.FLAT, highlightbackground=BORDER_COLOR)
        self.entry_descripcion.grid(row=1, column=1, sticky="ew", padx=5, pady=5, columnspan=5)

        # Separador
        ttk.Separator(form_frame, orient="horizontal").grid(row=2, column=0, columnspan=6, sticky="ew", pady=10)

        # Lista de ingredientes
        tk.Label(form_frame, text="Lista de ingredientes:", bg=FRAME_COLOR, fg=COLORS['morado'], anchor="w", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", columnspan=6, pady=(10, 0))

        # Nombre
        tk.Label(form_frame, text="Nombre:", bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=4, column=0, sticky="w", padx=(0, 2), pady=(5, 0))
        self.entry_ingrediente = tk.Entry(form_frame, width=35, bg=COLORS['blanco'], fg=TEXT_COLOR, relief=tk.FLAT, highlightbackground=BORDER_COLOR)
        self.entry_ingrediente.grid(row=4, column=1, sticky="w", padx=(0, 10), pady=(5, 0))

        # Cantidad
        tk.Label(form_frame, text="Cantidad:", bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=4, column=2, sticky="w", padx=(0, 2), pady=(5, 0))
        self.entry_cantidad = tk.Entry(form_frame, width=10, bg=COLORS['blanco'], fg=TEXT_COLOR, relief=tk.FLAT, highlightbackground=BORDER_COLOR)
        self.entry_cantidad.insert(0, "0")
        self.entry_cantidad.grid(row=4, column=3, sticky="w", padx=(0, 10), pady=(5, 0))

        # Unidad
        tk.Label(form_frame, text="Unidad:", bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=4, column=4, sticky="w", padx=(0, 2), pady=(5, 0))
        self.combo_unidad = ttk.Combobox(form_frame, values=["pz", "g", "kg", "ml", "l", "cda", "cdta"], width=7)
        self.combo_unidad.set("pz")
        self.combo_unidad.grid(row=4, column=5, sticky="w", pady=(5, 0))
        
        # Botón agregar ingrediente
        self.btn_agregar_ingrediente = tk.Button(
            form_frame,
            text="➕ Agregar Ingrediente",
            bg=BTN_COLOR,
            fg=BTN_TEXT,
            activebackground=COLORS['verde'],
            activeforeground=BTN_TEXT,
            command=self.agregar_ingrediente,
            relief=tk.FLAT
        )
        self.btn_agregar_ingrediente.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        # Lista de ingredientes agregados
        self.listbox_ingredientes = tk.Listbox(form_frame, height=5, width=50, bg=COLORS['blanco'], fg=TEXT_COLOR, relief=tk.FLAT, highlightbackground=BORDER_COLOR)
        self.listbox_ingredientes.grid(row=6, column=0, columnspan=6, sticky="ew", pady=5)
        scrollbar_ingredientes = tk.Scrollbar(form_frame, command=self.listbox_ingredientes.yview)
        scrollbar_ingredientes.grid(row=6, column=6, sticky="ns")
        self.listbox_ingredientes.config(yscrollcommand=scrollbar_ingredientes.set)
        
        self.btn_eliminar_ingrediente = tk.Button(
            form_frame,
            text="🗑️ Eliminar Ingrediente",
            bg=COLORS['rojo'],
            fg=BTN_TEXT,
            activebackground=COLORS['naranja'],
            activeforeground=BTN_TEXT,
            command=self.eliminar_ingrediente,
            relief=tk.FLAT
        )
        self.btn_eliminar_ingrediente.grid(row=5, column=2, columnspan=2, sticky="w", pady=5)

        self.listbox_ingredientes.bind('<Double-1>', self.cargar_ingrediente_para_editar)
        
        # Separador
        ttk.Separator(form_frame, orient="horizontal").grid(row=7, column=0, columnspan=7, sticky="ew", pady=10)

        # Instrucciones de preparación
        tk.Label(form_frame, text="Instrucciones de preparación:", bg=FRAME_COLOR, fg=COLORS['morado'], anchor="w", font=("Arial", 10, "bold")).grid(row=8, column=0, sticky="nw", columnspan=7)
        self.entry_instrucciones = tk.Text(form_frame, width=50, height=5, bg=COLORS['blanco'], fg=TEXT_COLOR, relief=tk.FLAT, highlightbackground=BORDER_COLOR)
        self.entry_instrucciones.grid(row=9, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        instrucciones_scroll = tk.Scrollbar(form_frame, command=self.entry_instrucciones.yview)
        instrucciones_scroll.grid(row=9, column=6, sticky="ns")
        self.entry_instrucciones['yscrollcommand'] = instrucciones_scroll.set

        # Botones Guardar y Limpiar
        self.btn_guardar = tk.Button(
            form_frame,
            text="💾 Guardar Receta",
            bg=COLORS['verde'],
            fg=BTN_TEXT,
            width=15,
            command=self.guardar_receta,
            relief=tk.FLAT,
            activebackground=COLORS['verde'],
            activeforeground=BTN_TEXT
        )
        self.btn_guardar.grid(row=10, column=4, sticky="e", pady=10, padx=5)
        
        self.btn_limpiar = tk.Button(
            form_frame,
            text="🧹 Limpiar",
            bg=COLORS['borde'],
            fg=TEXT_COLOR,
            width=10,
            command=self.limpiar_formulario,
            relief=tk.FLAT,
            activebackground=COLORS['borde'],
            activeforeground=TEXT_COLOR
        )
        self.btn_limpiar.grid(row=10, column=5, sticky="w", pady=10, padx=5)

        # Ajustar columnas del formulario
        for i in range(6):
            form_frame.columnconfigure(i, weight=1)

        # Tabla de recetas con scrollbars
        tree_frame = tk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Nombre", "Descripcion"),
            show="headings",
            selectmode="browse",
            height=18,
            style="Treeview"
        )
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripcion", text="Descripción")
        self.tree.column("Nombre", width=300, anchor="w")
        self.tree.column("Descripcion", width=600, anchor="w")

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        self.cargar_recetas_en_tabla()

        # Frame para los botones Editar y Eliminar
        btn_frame = tk.Frame(list_frame, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, padx=10, pady=(5, 10), anchor="e")

        self.btn_agregar = tk.Button(btn_frame, text="➕ Agregar", width=12, bg=COLORS['verde'], fg=BTN_TEXT, relief=tk.FLAT, activebackground=COLORS['verde'], activeforeground=BTN_TEXT, command=self.activa_formulario, state="disabled")
        self.btn_agregar.pack(side=tk.RIGHT, padx=5)
        self.btn_ver = tk.Button(btn_frame, text="👁️ Ver Receta", width=12, bg=COLORS['azul'], fg=BTN_TEXT, relief=tk.FLAT, activebackground=COLORS['azul'], activeforeground=BTN_TEXT, command=self.ver_receta)
        self.btn_ver.pack(side=tk.RIGHT, padx=5)
        self.btn_editar = tk.Button(btn_frame, text="✏️ Editar", width=12, command=self.cargar_receta_para_editar, bg=COLORS['naranja'], fg=BTN_TEXT, relief=tk.FLAT, activebackground=COLORS['naranja'], activeforeground=BTN_TEXT)
        self.btn_editar.pack(side=tk.RIGHT, padx=5)
        self.btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar", width=12, command=self.eliminar_receta, bg=COLORS['rojo'], fg=BTN_TEXT, relief=tk.FLAT, activebackground=COLORS['rojo'], activeforeground=BTN_TEXT)
        self.btn_eliminar.pack(side=tk.RIGHT, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_window)
      
    def activa_formulario(self):
        self.entry_nombre.config(state="normal")
        self.entry_descripcion.config(state="normal")
        self.entry_instrucciones.config(state="normal")
        self.listbox_ingredientes.config(state="normal")
        self.btn_agregar_ingrediente.config(state="normal")
        self.btn_eliminar_ingrediente.config(state="normal")
        self.btn_guardar.config(state="normal")
        self.btn_limpiar.config(state="normal")
        self.btn_agregar.config(state="disabled")
        self.limpiar_formulario()
    
    def eliminar_ingrediente(self):
        """Elimina el ingrediente seleccionado del listbox y de la lista interna"""
        seleccion = self.listbox_ingredientes.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un ingrediente para eliminar")
            return
        idx = seleccion[0]
        self.listbox_ingredientes.delete(idx)
        del self.ingredientes[idx]  
      
    def cargar_ingrediente_para_editar(self, event=None):
        """Carga el ingrediente seleccionado en los campos de entrada"""
        seleccion = self.listbox_ingredientes.curselection()
        if not seleccion:
            return
        idx = seleccion[0]
        ing = self.ingredientes[idx]
        self.entry_ingrediente.delete(0, tk.END)
        self.entry_ingrediente.insert(0, ing["name"])
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, str(ing["quantity"]))
        self.combo_unidad.set(ing["unit"])
        # Opcional: eliminarlo de la lista para que al agregarlo se reemplace
        self.listbox_ingredientes.delete(idx)
        del self.ingredientes[idx]
        
    def cargar_recetas_en_tabla(self):
        """Carga todas las recetas de la base de datos"""
        self.tree.delete(*self.tree.get_children())
        self.recetas = self.controller.get_all_recipes() or []
        for receta in self.recetas:
            self.tree.insert(
                "", tk.END,
                values=(receta.name, receta.description)
            )
    
    def agregar_ingrediente(self):
        """Agrega el ingrediente a la lista"""
        nombre = self.entry_ingrediente.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        unidad = self.combo_unidad.get().strip()
        
        if not nombre or not cantidad or not unidad:
            messagebox.showerror("Error", "Completa todos los campos del ingrediente")
            return
        try:
            cantidad_val = float(cantidad)
        except ValueError:
            messagebox.showerror("Error")
            return
        
        ingrediente = {
            "name": nombre,
            "quantity": cantidad_val,
            "unit": unidad
        }
        
        self.ingredientes.append(ingrediente)
        display = f"{cantidad} {unidad} {nombre}"
        self.listbox_ingredientes.insert(tk.END, display)
        
        self.entry_ingrediente.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "0")
        self.combo_unidad.set("pz")
        
    def guardar_receta(self):
        """Guardar la receta o la actualiza"""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get("1.0", tk.END).strip()
        instrucciones_str = self.entry_instrucciones.get("1.0", tk.END).strip()
        
        if not nombre or not descripcion or not instrucciones_str or not self.ingredientes:
            messagebox.showerror("Error", "Favor de completar todos los campos")
            return
        pasos = [line.strip() for line in instrucciones_str.split('\n') if line.strip()]
        if self.editing_recipe_id:
            # Actualiza una receta existente
            self.controller.update_recipe(
                self.editing_recipe_id,
                nombre,
                descripcion,
                self.ingredientes,
                pasos
            )
            self.editing_recipe_id = None
        else:
            # Guardar una nueva receta
            self.controller.register_recipe(nombre, descripcion, self.ingredientes, pasos)
        self.limpiar_formulario()
        self.cargar_recetas_en_tabla()
    
    def cargar_receta_para_editar(self):
        """Carga la receta seleccionada en el formulario para editarlo"""
        selected = self.tree.selection()
        if not selected:
            self.show_error("Selecciona una receta para editar")
            return
        item = self.tree.item(selected)
        nombre_receta = item['values'][0]
        receta = self.controller.get_recipe_by_name(nombre_receta)
        if not receta:
            self.show_error("No se pudo cargar la receta")
            return
        
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, receta.name)
        self.entry_descripcion.delete("1.0", tk.END)
        self.entry_descripcion.insert("1.0", receta.description)
        self.entry_instrucciones.delete("1.0", tk.END)
        self.entry_instrucciones.insert("1.0", "\n".join(receta.steps))
        self.listbox_ingredientes.delete(0, tk.END)
        self.ingredientes = []
        for ing in receta.ingredients:
            self.ingredientes.append(ing)
            display = f"{ing['quantity']} {ing['unit']} {ing['name']}"
            self.listbox_ingredientes.insert(tk.END, display)
        self.editing_recipe_id = receta.recipe_id
        self.btn_agregar.config(state="disabled")

    def ver_receta(self):
        """Carga la receta seleccionada en el formulario en modo de lectura"""
        selected = self.tree.selection()
        if not selected:
            self.show_error("Selecciona una receta para visualizar")
            return
        item = self.tree.item(selected)
        nombre_receta = item['values'][0]
        receta = self.controller.get_recipe_by_name(nombre_receta)
        if not receta:
            self.show_error("No se pudo cargar la receta")
            return
        
        # Cargar datos en los campos
        self.entry_nombre.config(state="normal")
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, receta.name)
        self.entry_nombre.config(state="readonly")

        self.entry_descripcion.config(state="normal")
        self.entry_descripcion.delete("1.0", tk.END)
        self.entry_descripcion.insert("1.0", receta.description)
        self.entry_descripcion.config(state="disabled")

        self.entry_instrucciones.config(state="normal")
        self.entry_instrucciones.delete("1.0", tk.END)
        self.entry_instrucciones.insert("1.0", "\n".join(receta.steps))
        self.entry_instrucciones.config(state="disabled")
        
        self.listbox_ingredientes.delete(0, tk.END)
        for ing in receta.ingredients:
            display = f"{ing['quantity']} {ing['unit']} {ing['name']}"
            self.listbox_ingredientes.insert(tk.END, display)
        self.listbox_ingredientes.config(state="disabled")
        
        # Bloquear botones del formulario
        self.btn_agregar_ingrediente.config(state="disabled")
        self.btn_eliminar_ingrediente.config(state="disabled")
        self.btn_guardar.config(state="disabled")
        self.btn_limpiar.config(state="disabled")
        self.btn_agregar.config(state="normal")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete("1.0", tk.END)
        self.entry_ingrediente.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "0")
        self.combo_unidad.set("pz")
        self.listbox_ingredientes.delete(0, tk.END)
        self.entry_instrucciones.delete("1.0", tk.END)
        self.ingredientes = []
        self.btn_agregar.config(state="disabled")
        
    def eliminar_receta(self):
        """Elimina la receta"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una receta para eliminar")
            return
        idx = self.tree.index(seleccion[0])
        receta = self.recetas[idx]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar la receta '{receta.name}'?")    
        if confirm:
            self.controller.delete_recipe(receta.recipe_id)
            self.tree.delete(seleccion[0])
            del self.recetas[idx]
            self.limpiar_formulario()
        
    def show_error(self, message):
        messagebox.showerror("Error", message)
        
    def show_success(self, message):
        messagebox.showinfo("Exito", message)
    
    def exit_window(self):
        self.root.destroy()
        sys.exit(0)
