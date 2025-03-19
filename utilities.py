import tkinter as tk
import ttkbootstrap as ttk
import sqlite3

products=[]
clients=[]
sells=[]

class Database():
    def __init__(self):
        self.conn = sqlite3.connect("db")
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS products
    (
        id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        cost REAL NOT NULL,
        price REAL NOT NULL
    )
    """)
        
        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients
    (
        id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        cep INTEGER NOT NULL,
        phone TEXT NOT NULL
    )
    """)
        
        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS sells
    (
        id INTEGER PRIMARY KEY NOT NULL,
        id_client TEXT NOT NULL,
        id_product TEXT NOT NULL,
        quantity INTEGER NOT NULL
        total_value REAL NOT NULL
        FOREING KEY (id_cliente) REFERENCES clients(id)
        FOREING KEY (id_product) REFERENCES products(id)
    )
    """)
    
    def add(self, reference_list, table_name):

        match table_name:
            case 'products':
                for element in table_name:
                    for value in element:
                        self.cursor.execute(f"""INSERT INTO products (id, name, cost, value)
                                            VALUES ({value[0]}, {value[1]}, {value[2]}, {value[3]})""")
            
            case 'clients':
                for element in table_name:
                    for value in element:
                        self.cursor.execute(f"""INSERT INTO clients (id, name, cep, phone)
                                            VALUES ({value[0]}, {value[1]}, {value[2]}, {value[3]})""")

            case 'sells':
                for element in table_name:
                    for value in element:
                        self.cursor.execute(f"""INSERT INTO sells (id, quantity, total_value)
                                            VALUES ({value[0]}, {value[1]}, {value[2]}, {value[3]})""")


        

def frame_complete(notebook, lista=type(list), tipo=type(str), *args):
    "Used for completion of frame pattern."

    frame = ttk.Frame(notebook)

    notebook.add(frame, text= tipo)

    entries = []

    for v in range(len(args)):
        label = ttk.Label(frame, text= args[v], font=("Helvetica",10), padding=10)
        label.grid(row=v,column=0, sticky="w")

        entry = ttk.Entry(frame, width=30)
        entry.grid(row=v, column=2, sticky="ew")

        entries.append(entry)

    def getter():
        values = [entry.get() for entry in entries]
        if tipo == "Cadastrar":
            lista.append(values)
        else:
            for k,v in enumerate(lista):
                if values[0] == v[0]:
                    lista.pop(k)

        for entry in entries:
            entry.delete(0, tk.END)
    
    action_btn = ttk.Button(frame, text="Concluir", command=getter)
    action_btn.grid(row=len(args), column=2, sticky="e")