import tkinter as tk
from tkinter import ttk, messagebox
import sys
from controllers.recipe_controller import RecipeController
from utils.styles import COLORS


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
        style.configure("Custom.TLabelframe", background=BG_COLOR, foreground=COLORS['morado'], font=("Arial", 10, "bold"))
        style.configure("Treeview", background=COLORS['blanco'], foreground=TEXT_COLOR, fieldbackground=COLORS['blanco'], font=("Arial", 9))
        style.configure("Treeview.Heading", background=COLORS['morado'], foreground=BTN_TEXT, font=("Arial", 9, "bold"))
        style.configure("Treeview", rowheight=25)
        
        self.editing_recipe_id = None
        self.ingredientes = []
        self.controller = RecipeController(self)
        
        self.root.title(f"NutriPlan - 📖 Recetas - {user_data.username}")
        
        # Configuración de ventana compacta
        self.root.geometry("1000x600")
        self.root.minsize(1000, 600)
        self.root.maxsize(1000, 600)  # Fijar tamaño máximo
        self.root.resizable(False, False)  # No redimensionable
        self.root.config(bg=BG_COLOR)
        
        # Frame principal con padding mínimo
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar grid principal compacto
        main_frame.columnconfigure(0, weight=1, minsize=380)  # Panel izquierdo
        main_frame.columnconfigure(1, weight=1, minsize=600)  # Panel derecho
        main_frame.rowconfigure(0, weight=1)

        # Frame izquierdo: Formulario compacto
        form_frame = tk.LabelFrame(main_frame, text="Formulario de Recetas", bg=BG_COLOR, fg=TEXT_COLOR,
                       font=("Arial", 9, "bold"), padx=5, pady=5, labelanchor="n", relief=tk.GROOVE)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 3), pady=0)

        # Frame derecho: Lista de recetas
        list_frame = tk.LabelFrame(main_frame, text="Lista de Recetas", bg=BG_COLOR, fg=TEXT_COLOR,
                       font=("Arial", 9, "bold"), padx=5, pady=5, labelanchor="n", relief=tk.GROOVE)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(3, 0), pady=0)

        # --- Formulario compacto ---
        form_frame.columnconfigure(0, weight=1)
        
        row = 0
        
        # Nombre de la receta
        tk.Label(form_frame, text="Nombre:", bg=BG_COLOR, fg=TEXT_COLOR, 
                font=("Arial", 8, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 2))
        row += 1
        self.entry_nombre = tk.Entry(form_frame, bg=COLORS['blanco'], fg=TEXT_COLOR, 
                                   relief=tk.FLAT, highlightbackground=BORDER_COLOR, font=("Arial", 8))
        self.entry_nombre.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        row += 1

        # Descripción compacta
        tk.Label(form_frame, text="Descripción:", bg=BG_COLOR, fg=TEXT_COLOR, 
                font=("Arial", 8, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 2))
        row += 1
        self.entry_descripcion = tk.Text(form_frame, height=2, bg=COLORS['blanco'], fg=TEXT_COLOR, 
                                       relief=tk.FLAT, highlightbackground=BORDER_COLOR, font=("Arial", 8))
        self.entry_descripcion.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        row += 1

        # Sección ingredientes compacta
        tk.Label(form_frame, text="Ingredientes:", bg=BG_COLOR, fg=COLORS['morado'], 
                font=("Arial", 8, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 3))
        row += 1

        # Frame de ingredientes
        ing_frame = tk.Frame(form_frame, bg=BG_COLOR)
        ing_frame.grid(row=row, column=0, sticky="ew", pady=(0, 3))
        ing_frame.columnconfigure(0, weight=2)  # Nombre más ancho
        ing_frame.columnconfigure(1, weight=1)  # Cantidad
        ing_frame.columnconfigure(2, weight=1)  # Unidad
        
        #Labels correspondientes a los ingredientes
        tk.Label(ing_frame, text="Nombre", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 7, "bold"), justify="left").grid(row=0, column=0, sticky="w", padx=(0, 0))
        tk.Label(ing_frame, text="Cantidad", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 7, "bold"), justify="left").grid(row=0, column=1, sticky="w", padx=(0, 0))
        tk.Label(ing_frame, text="Unidad", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 7, "bold")).grid(row=0, column=2, sticky="w", padx=(0, 0))
        
        # Entradas de datos de los ingredientes
        self.entry_ingrediente = tk.Entry(ing_frame, bg=COLORS['blanco'], fg=TEXT_COLOR, 
                        relief=tk.FLAT, highlightbackground=BORDER_COLOR, font=("Arial", 8))
        self.entry_ingrediente.grid(row=1, column=0, sticky="ew", padx=(0, 2))
        self.entry_cantidad = tk.Entry(ing_frame, bg=COLORS['blanco'], fg=TEXT_COLOR, 
                         relief=tk.FLAT, highlightbackground=BORDER_COLOR, font=("Arial", 8))
        self.entry_cantidad.insert(0, "0")
        self.entry_cantidad.grid(row=1, column=1, sticky="ew", padx=2)
        self.combo_unidad = ttk.Combobox(ing_frame, values=["pz", "g", "kg", "ml", "l", "cda", "cdta"], 
                           font=("Arial", 8), state="readonly")
        self.combo_unidad.set("pz")
        self.combo_unidad.grid(row=1, column=2, sticky="ew", padx=(2, 0))
        row += 1
        
        # Botones de ingredientes compactos
        btn_ing_frame = tk.Frame(form_frame, bg=BG_COLOR)
        btn_ing_frame.grid(row=row, column=0, sticky="ew", pady=(0, 3))
        btn_ing_frame.columnconfigure(0, weight=1)
        btn_ing_frame.columnconfigure(1, weight=1)
        row += 1
        
        self.btn_agregar_ingrediente = tk.Button(
            btn_ing_frame, text="+ Agregar", bg=BTN_COLOR, fg=BTN_TEXT,
            activebackground=COLORS['verde'], activeforeground=BTN_TEXT,
            command=self.agregar_ingrediente, relief=tk.FLAT, font=("Arial", 7)
        )
        self.btn_agregar_ingrediente.grid(row=0, column=0, sticky="ew", padx=(0, 1))
        
        self.btn_eliminar_ingrediente = tk.Button(
            btn_ing_frame, text="- Eliminar", bg=COLORS['rojo'], fg=BTN_TEXT,
            activebackground=COLORS['naranja'], activeforeground=BTN_TEXT,
            command=self.eliminar_ingrediente, relief=tk.FLAT, font=("Arial", 7)
        )
        self.btn_eliminar_ingrediente.grid(row=0, column=1, sticky="ew", padx=(1, 0))

        # Lista de ingredientes compacta
        self.listbox_ingredientes = tk.Listbox(form_frame, height=5, bg=COLORS['blanco'], fg=TEXT_COLOR, 
                                             relief=tk.FLAT, highlightbackground=BORDER_COLOR, font=("Arial", 7))
        self.listbox_ingredientes.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        self.listbox_ingredientes.bind('<Double-1>', self.cargar_ingrediente_para_editar)
        row += 1

        # Instrucciones compactas
        tk.Label(form_frame, text="Instrucciones:", bg=BG_COLOR, fg=COLORS['morado'], 
                font=("Arial", 8, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 2))
        row += 1
        
        self.entry_instrucciones = tk.Text(form_frame, height=4, bg=COLORS['blanco'], fg=TEXT_COLOR, 
                                         relief=tk.FLAT, highlightbackground=BORDER_COLOR, font=("Arial", 8))
        self.entry_instrucciones.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        row += 1

        # Botones principales compactos
        btn_form_frame = tk.Frame(form_frame, bg=BG_COLOR)
        btn_form_frame.grid(row=row, column=0, sticky="ew")
        btn_form_frame.columnconfigure(0, weight=1)
        btn_form_frame.columnconfigure(1, weight=1)
        
        self.btn_limpiar = tk.Button(
            btn_form_frame, text="🧹 Limpiar", bg=COLORS['borde'], fg=TEXT_COLOR,
            command=self.limpiar_formulario, relief=tk.FLAT,
            activebackground=COLORS['borde'], activeforeground=TEXT_COLOR, font=("Arial", 8)
        )
        self.btn_limpiar.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        
        self.btn_guardar = tk.Button(
            btn_form_frame, text="💾 Guardar", bg=COLORS['verde'], fg=BTN_TEXT,
            command=self.guardar_receta, relief=tk.FLAT,
            activebackground=COLORS['verde'], activeforeground=BTN_TEXT, font=("Arial", 8, "bold")
        )
        self.btn_guardar.grid(row=0, column=1, sticky="ew", padx=(2, 0))

        # --- Panel derecho: Tabla optimizada ---
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Tabla más compacta
        self.tree = ttk.Treeview(
            list_frame, columns=("Nombre", "Descripcion"), show="headings",
            selectmode="browse", style="Treeview", height=20
        )
        self.tree.heading("Nombre", text="Receta")
        self.tree.heading("Descripcion", text="Descripción")
        self.tree.column("Nombre", width=180, anchor="w", minwidth=120)
        self.tree.column("Descripcion", width=320, anchor="w", minwidth=200)

        # Scrollbar vertical únicamente
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        scrollbar.grid(row=0, column=1, sticky="ns", pady=(0, 5))
        
        self.cargar_recetas_en_tabla()

        # Botones de tabla en una sola fila compacta
        btn_table_frame = tk.Frame(list_frame, bg=BG_COLOR)
        btn_table_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        # Configurar columnas para distribución uniforme
        for i in range(4):
            btn_table_frame.columnconfigure(i, weight=1)

        self.btn_ver = tk.Button(btn_table_frame, text="👁️ Ver", bg=COLORS['azul'], fg=BTN_TEXT, 
                               relief=tk.FLAT, activebackground=COLORS['azul'], activeforeground=BTN_TEXT, 
                               command=self.ver_receta, font=("Arial", 8))
        self.btn_ver.grid(row=0, column=0, sticky="ew", padx=(0, 1))
        
        self.btn_editar = tk.Button(btn_table_frame, text="✏️ Editar", command=self.cargar_receta_para_editar, 
                                  bg=COLORS['naranja'], fg=BTN_TEXT, relief=tk.FLAT, 
                                  activebackground=COLORS['naranja'], activeforeground=BTN_TEXT, font=("Arial", 8))
        self.btn_editar.grid(row=0, column=1, sticky="ew", padx=1)
        
        self.btn_eliminar = tk.Button(btn_table_frame, text="🗑️ Eliminar", command=self.eliminar_receta, 
                                    bg=COLORS['rojo'], fg=BTN_TEXT, relief=tk.FLAT, 
                                    activebackground=COLORS['rojo'], activeforeground=BTN_TEXT, font=("Arial", 8))
        self.btn_eliminar.grid(row=0, column=2, sticky="ew", padx=1)

        self.btn_agregar = tk.Button(btn_table_frame, text="➕ Nueva", bg=COLORS['verde'], fg=BTN_TEXT, 
                                   relief=tk.FLAT, activebackground=COLORS['verde'], activeforeground=BTN_TEXT, 
                                   command=self.activa_formulario, state="disabled", font=("Arial", 8, "bold"))
        self.btn_agregar.grid(row=0, column=3, sticky="ew", padx=(1, 0))

        # Cambiar protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
      
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
        # Eliminarlo de la lista para reemplazarlo
        self.listbox_ingredientes.delete(idx)
        del self.ingredientes[idx]
        
    def cargar_recetas_en_tabla(self):
        """Carga todas las recetas de la base de datos"""
        self.tree.delete(*self.tree.get_children())
        self.recetas = self.controller.get_all_recipes() or []
        for receta in self.recetas:
            # Truncar descripción para que quepa en la tabla
            desc_truncada = (receta.description[:80] + "...") if len(receta.description) > 80 else receta.description
            self.tree.insert("", tk.END, values=(receta.name, desc_truncada))
    
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
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        ingrediente = {"name": nombre, "quantity": cantidad_val, "unit": unidad}
        self.ingredientes.append(ingrediente)
        display = f"{cantidad} {unidad} {nombre}"
        self.listbox_ingredientes.insert(tk.END, display)
        
        # Limpiar campos
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
            self.controller.update_recipe(self.editing_recipe_id, nombre, descripcion, self.ingredientes, pasos)
            self.editing_recipe_id = None
        else:
            self.controller.register_recipe(nombre, descripcion, self.ingredientes, pasos)
            
        self.limpiar_formulario()
        self.cargar_recetas_en_tabla()
    
    def cargar_receta_para_editar(self):
        """Carga la receta seleccionada en el formulario para editarlo"""
        self.entry_nombre.config(state="normal")
        self.entry_descripcion.config(state="normal")
        self.entry_instrucciones.config(state="normal")
        self.listbox_ingredientes.config(state="normal")
        self.btn_agregar_ingrediente.config(state="normal")
        self.btn_eliminar_ingrediente.config(state="normal")
        self.btn_guardar.config(state="normal")
        self.btn_limpiar.config(state="normal")
        self.btn_agregar.config(state="disabled")

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
        
        # Cargar datos en formulario
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, receta.name)
        self.entry_descripcion.delete("1.0", tk.END)
        self.entry_descripcion.insert("1.0", receta.description)
        self.entry_instrucciones.delete("1.0", tk.END)
        self.entry_instrucciones.insert("1.0", "\n".join(receta.steps))
        
        # Cargar ingredientes
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
        
        # Cargar en modo lectura
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
        
        # Deshabilitar controles de edición
        self.btn_agregar_ingrediente.config(state="disabled")
        self.btn_eliminar_ingrediente.config(state="disabled")
        self.btn_guardar.config(state="disabled")
        self.btn_limpiar.config(state="disabled")
        self.btn_agregar.config(state="normal")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario y los pone en modo edición"""
        self.entry_nombre.config(state="normal")
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.config(state="normal")
        self.entry_descripcion.delete("1.0", tk.END)
        self.entry_ingrediente.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "0")
        self.combo_unidad.set("pz")
        self.listbox_ingredientes.config(state="normal")
        self.listbox_ingredientes.delete(0, tk.END)
        self.entry_instrucciones.config(state="normal")
        self.entry_instrucciones.delete("1.0", tk.END)
        self.ingredientes = []
        self.btn_agregar.config(state="disabled")
        self.btn_agregar_ingrediente.config(state="normal")
        self.btn_eliminar_ingrediente.config(state="normal")
        self.btn_guardar.config(state="normal")
        self.btn_limpiar.config(state="normal")
    
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
            self.editing_recipe_id = None
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
        
    def show_success(self, message):
        messagebox.showinfo("Éxito", message)
    
    def cerrar_ventana(self):
        """Cierra solo esta ventana sin afectar otras interfaces"""
        if messagebox.askokcancel("Cerrar", "¿Deseas cerrar el gestor de recetas?"):
            self.root.destroy()  # Solo destruye esta ventana
    
    # Método mantenido para compatibilidad
    def exit_window(self):
        self.cerrar_ventana()