import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.shopping_list_service import generate_shopping_list
import csv

class ShoppingListGUI:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.items = []  # ← Aquí almacenaremos los ingredientes para exportar

        self.root.title(f"Lista de Compras - {user_data.fullname}")
        self.root.geometry("900x600")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Etiquetas de bienvenida y explicación
        welcome_label = tk.Label(
            self.main_frame,
            text=f"Lista de Compras para {user_data.fullname}",
            font=("Helvetica", 16, "bold")
        )
        welcome_label.pack(pady=10)

        info_label = tk.Label(
            self.main_frame,
            text="A continuación se muestra la lista consolidada de ingredientes basada en tu planificación semanal:",
            font=("Helvetica", 12)
        )
        info_label.pack(pady=5)

        # 🟡 Frame con botones
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)

        generate_btn = tk.Button(button_frame, text="Generar Lista", command=self.load_shopping_list)
        generate_btn.grid(row=0, column=0, padx=10)

        export_btn = tk.Button(button_frame, text="Descargar CSV", command=self.export_csv)
        export_btn.grid(row=0, column=1, padx=10)

        # 🟢 Tabla de ingredientes
        self.tree = ttk.Treeview(self.main_frame, columns=("Ingrediente", "Cantidad", "Unidad"), show="headings")
        self.tree.heading("Ingrediente", text="Ingrediente")
        self.tree.heading("Cantidad", text="Cantidad Total")
        self.tree.heading("Unidad", text="Unidad")

        self.tree.column("Ingrediente", anchor=tk.CENTER, width=200)
        self.tree.column("Cantidad", anchor=tk.CENTER, width=120)
        self.tree.column("Unidad", anchor=tk.CENTER, width=120)

        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        # 🔴 Botón para cerrar
        close_btn = tk.Button(self.main_frame, text="Cerrar", command=self.root.destroy)
        close_btn.pack(pady=10)

        # Cargar datos al iniciar
        #self.load_shopping_list()

    def load_shopping_list(self):
        """Carga y muestra la lista de compras"""
        try:
            # Limpiar la tabla antes de recargar
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 🔧 Usa datos reales o simulados
            self.items = generate_shopping_list(str(self.user_data._id))

            if not self.items:
                messagebox.showinfo("Sin recetas", "Aún no tienes recetas en tu planificación semanal.")
                return

            # Insertar en la tabla
            for item in self.items:
                self.tree.insert("", tk.END, values=(item["name"], item["quantity"], item["unit"]))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la lista: {e}")

    def export_csv(self):
        """Exporta la lista a un archivo CSV"""
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
