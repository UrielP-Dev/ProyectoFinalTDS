import tkinter as tk
from controllers.shopping_list_controller import mostrar_lista_compras

def crear_ventana_lista_compras():
    ventana = tk.Toplevel()
    ventana.title("Lista de Compras")

    tk.Button(ventana, text="Generar Lista", command=lambda: mostrar_lista_compras(ventana)).pack()

    lista_texto = tk.Text(ventana, height=20, width=50)
    lista_texto.pack()
    return lista_texto
