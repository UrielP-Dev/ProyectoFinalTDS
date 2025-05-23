import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.shopping_list_service import generate_shopping_list
from utils.styles import COLORS
import csv
import utils.session as session

class ShoppingListGUI:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.items = [] 

        print(f"ID de usuario en shopping_list_gui: {user_data._id}, tipo: {type(user_data._id)}")
        
        session.user_id = str(user_data._id)  

        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title(f"Lista de Compras - {self.user_data.fullname}")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.config(bg=COLORS['fondo'])

        self.title_font = ("Helvetica", 16, "bold")
        self.subtitle_font = ("Helvetica", 12, "bold")
        self.normal_font = ("Helvetica", 10)

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        # Título morado
        welcome_label = tk.Label(
            self.main_frame,
            text=f"Lista de Compras para {self.user_data.fullname}",
            font=self.title_font,
            fg=COLORS['morado'],
            bg=COLORS['fondo']
        )
        welcome_label.pack(pady=10)

        # Subtítulo
        info_label = tk.Label(
            self.main_frame,
            text="A continuación se muestra la lista consolidada de ingredientes basada en tu planificación semanal:",
            font=self.normal_font,
            bg=COLORS['fondo'],
            fg=COLORS['texto_oscuro']
        )
        info_label.pack(pady=5)


        # Botones superiores
        button_frame = tk.Frame(self.main_frame, bg=COLORS['fondo'])
        button_frame.pack(pady=10)

        generate_btn = tk.Button(
            button_frame,
            text="Generar Lista",
            command=self.load_shopping_list,
            bg=COLORS['verde'],
            fg=COLORS['texto_claro'],
            font=self.normal_font,
            padx=15,
            pady=5
        )
        generate_btn.grid(row=0, column=0, padx=10)

        export_btn = tk.Button(
            button_frame,
            text="Descargar CSV",
            command=self.export_csv,
            bg=COLORS['morado'],
            fg=COLORS['texto_claro'],
            font=self.normal_font,
            padx=15,
            pady=5
        )
        export_btn.grid(row=0, column=1, padx=10)

        # Tabla
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("Ingrediente", "Cantidad", "Unidad"),
            show="headings",
            height=15
        )
        self.tree.heading("Ingrediente", text="Ingrediente")
        self.tree.heading("Cantidad", text="Cantidad Total")
        self.tree.heading("Unidad", text="Unidad")

        self.tree.column("Ingrediente", anchor=tk.CENTER, width=300)
        self.tree.column("Cantidad", anchor=tk.CENTER, width=150)
        self.tree.column("Unidad", anchor=tk.CENTER, width=150)
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        # Botón cerrar
        close_btn = tk.Button(
            self.main_frame,
            text="Cerrar",
            command=self.root.destroy,
            bg=COLORS['gris'],
            fg=COLORS['texto_oscuro'],
            font=self.normal_font,
            padx=10,
            pady=5
        )
        close_btn.pack(pady=10)

    def load_shopping_list(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Volver a verificar el ID actual
            print(f"ID de sesión al generar lista: {session.user_id}")
            
            # 🔧 Usa datos reales o simulados
            self.items = generate_shopping_list(session.user_id)
            print(f"Usuario: {self.user_data}")
            print(f"Elementos obtenidos: {self.items}")  # Para depuración

            if not self.items:
                messagebox.showinfo("Sin recetas", "Aún no tienes recetas en tu planificación semanal.")
                return

            for item in self.items:
                self.tree.insert("", tk.END, values=(item["name"], item["quantity"], item["unit"]))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la lista: {e}")

    def export_csv(self):
        if not self.items:
            messagebox.showinfo("Sin datos", "Primero genera la lista de compras.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Guardar como"
        )
        if filepath:
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Ingrediente", "Cantidad Total", "Unidad"])
                    for item in self.items:
                        writer.writerow([item["name"], item["quantity"], item["unit"]])
                messagebox.showinfo("Éxito", f"Lista exportada correctamente a:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
