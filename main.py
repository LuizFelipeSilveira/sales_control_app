import tkinter as tk
import ttkbootstrap as ttk
from utilities import *


# Main Structure 

root = ttk.Window(themename="solar")

top_frame = ttk.Frame(root, padding=5)
top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

left_frame = ttk.LabelFrame(root, padding=10, text="Produtos", bootstyle= "primary")
left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

center_frame = ttk.LabelFrame(root, padding=10, text="Clientes", bootstyle= "primary")
center_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

right_frame = ttk.LabelFrame(root, padding=10, text="Vendas", bootstyle= "primary")
right_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=3)
root.rowconfigure(1, weight=1)

# Widgets Placement

# Top Frame
label_t = ttk.Label(top_frame, text=f"Controle{110*' '}", font=("Helvetica", 20))
label_t.grid(row=0, column=1)

btn_stl = ttk.Button(top_frame, text="Dashboard")
btn_stl.grid(row=0, column=3, sticky="e")

# Left Frame
notebook_l = ttk.Notebook(left_frame)
notebook_l.grid()

frame_complete(notebook_l, products, 'Cadastrar','ID', 'Nome', 'Custo', 'Valor')
frame_complete(notebook_l, products, 'Descadastrar', 'ID')

# Center Frame
notebook_c = ttk.Notebook(center_frame)
notebook_c.grid()

frame_complete(notebook_c, clients, 'Cadastrar','ID', 'Nome', 'CEP', 'Telefone')
frame_complete(notebook_c, clients, 'Descadastrar', 'ID')

# Right Frame
notebook_r = ttk.Notebook(right_frame)
notebook_r.grid()

frame_complete(notebook_r, sells, 'Cadastrar','ID', 'Cliente', 'Produto', 'Quantidade')
frame_complete(notebook_r, sells, 'Descadastrar', 'ID')

# Run App
root.mainloop()

print(products)
print(clients)
print(sells)