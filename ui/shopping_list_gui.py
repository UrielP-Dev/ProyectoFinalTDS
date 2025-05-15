import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import font, messagebox
from controllers.shopping_list_controller import ShoppingListController
from utils.styles import COLORS

class ShoppingListGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.controller = ShoppingListController()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("NutriPlan - Generador de Lista de Compras")
        self.root.geometry("800x550")
        self.root.resizable(False, False)
        self.root.config(bg=COLORS['fondo'])

        self.title_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)

        self.main_frame = tk.Frame(self.root, bg=COLORS['fondo'], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_widgets(self):
        # Título
        title_frame = tk.Frame(self.main_frame, bg=COLORS['fondo'])
        title_frame.pack(pady=10)

        tk.Label(title_frame, text="Generador de Lista de Compras", font=self.title_font,
                 bg=COLORS['fondo'], fg=COLORS['morado']).pack()

        # Contenedor principal
        generator_frame = tk.Frame(self.main_frame, bg=COLORS['blanco'], padx=20, pady=20, relief=tk.RIDGE, bd=1)
        generator_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Botón para generar lista
        generate_button = tk.Button(generator_frame, text="Generar Lista", font=self.normal_font,
                                    bg=COLORS['verde'], fg=COLORS['texto_claro'],
                                    activebackground=COLORS['verde'], activeforeground=COLORS['texto_claro'],
                                    relief=tk.FLAT, padx=15, pady=8, command=self.generate_list)
        generate_button.pack(pady=(0, 10))

        # Área de resultados
        tk.Label(generator_frame, text="Lista de compras generada:", font=self.subtitle_font,
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(anchor=tk.W, pady=(0, 5))

        self.results_text = tk.Text(generator_frame, height=15, font=self.normal_font, wrap=tk.WORD,
                                    bg=COLORS['fondo'], fg=COLORS['texto_oscuro'], relief=tk.SOLID, bd=1)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Botón para exportar CSV
        export_button = tk.Button(generator_frame, text="Descargar CSV", font=self.normal_font,
                                  bg=COLORS['morado'], fg=COLORS['texto_claro'],
                                  activebackground=COLORS['morado'], activeforeground=COLORS['texto_claro'],
                                  relief=tk.FLAT, padx=15, pady=8, command=self.export_to_csv)
        export_button.pack(pady=10)

    def generate_list(self):
        try:
            ingredients = self.controller.generate_shopping_list()
            if not ingredients:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "No se encontraron ingredientes.")
                self.current_ingredients = []
            else:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "\n".join(sorted(ingredients)))
                self.current_ingredients = ingredients
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_csv(self):
        if not hasattr(self, 'current_ingredients') or not self.current_ingredients:
            messagebox.showwarning("Nada para exportar", "Primero genera una lista de compras.")
            return

        try:
            with open("lista_compras.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Ingrediente"])
                for item in sorted(self.current_ingredients):
                    writer.writerow([item])
            messagebox.showinfo("Exportación exitosa", "La lista se guardó como 'lista_compras.csv'.")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingListGeneratorGUI(root)
    root.mainloop()
