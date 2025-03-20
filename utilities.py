import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
import sqlite3


class Database():
    def __init__(self):
        self._open_conn()
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
    CREATE TABLE IF NOT EXISTS sales
    (
        id INTEGER PRIMARY KEY NOT NULL,
        id_client TEXT NOT NULL,
        id_product TEXT NOT NULL,
        date TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_value REAL NOT NULL,
        FOREIGN KEY (id_client) REFERENCES clients(id),
        FOREIGN KEY (id_product) REFERENCES products(id)
    )
    """)
        
    
    def add(self, reference_list, table_name):
        
        match table_name:
            case 'products':
                sql=("""INSERT INTO products (id, name, cost, price)
                        VALUES (?, ?, ?, ?)""")
                self.cursor.execute(sql, reference_list)
            
            case 'clients':
                sql=("""INSERT INTO clients (id, name, cep, phone)
                        VALUES (?, ?, ?, ?)""")
                self.cursor.execute(sql, reference_list)

            case 'sales':
                sql=("""INSERT INTO sales (id, id_client, id_product, date, quantity, total_value)
                        VALUES (?, ?, ?, DATE('now'), ?, ?)""")
                self.cursor.execute(sql, reference_list)
                    
        self.conn.commit()
    
    def remove(self, reference_list, table_name):

        match table_name:
            case 'products':
                self.cursor.execute("""DELETE FROM products
                                        WHERE id = ?""", reference_list[0],)

            case 'clients':
                self.cursor.execute("""DELETE FROM clients
                                        WHERE id = ?""", reference_list[0],)
                    
            case 'sales':
                self.cursor.execute("""DELETE FROM sales
                                        WHERE id = ?""", reference_list[0],)
        
                    
    def fetcher(self, table_name):
        self.cursor.execute(f"""SELECT * FROM {table_name}""")
        data = self.cursor.fetchall()
        return data
    
    def _open_conn(self):
        self.conn = sqlite3.connect("control.db")

    def _close_conn(self):
        self.conn.close()

db = Database()

def frame_complete(notebook, table_reference, action=type(str), *args):

    """Used for completion of frame pattern, placing a notebook with a page and entries.
       All data inputed on entries are registeres in a SQLite data base"""

    frame = ttk.Frame(notebook)

    notebook.add(frame, text= action)

    entries = []

    for v in range(len(args)):
        label = ttk.Label(frame, text= args[v], font=("Helvetica",10), padding=10)
        label.grid(row=v,column=0, sticky="w")

        entry = ttk.Entry(frame, width=30)
        entry.grid(row=v, column=2, sticky="ew")

        entries.append(entry)
    
    
    def getter():
        values = [entry.get() for entry in entries]

        def validate_list(reference_list, index, data_type):
            for item in reference_list:
                if type(reference_list[index]) != data_type:
                    try:
                        if isinstance(item[index], str) and ',' in item[index]:
                            item[index] = item[index].replace(',', '.')
                        elif isinstance(item[index], int):
                            item[index] = float(item[index])
                    except:
                        for entry in entries:
                            entry.delete(index, tk.END)
                else:
                    pass

        if len(values) < len(args):
            for entry in entries:
                entry.delete(0, tk.END)
        else:
            # Cadastrar no banco de dados
            if action == "Cadastrar":

                match table_reference:
                    case 'products':
                        validate_list(values,2, float)
                        validate_list(values,3, float)
                        db.add(values, table_reference)

                match table_reference:
                    case 'clients':
                        validate_list(values,2, float)
                        validate_list(values,3, float)
                        db.add(values, table_reference)

                match table_reference:
                    case 'sales':
                        validate_list(values,4, int)
                        validate_list(values,5, float)
                        db.add(values, table_reference)

            # Descadastrar do banco de dados-------------------------------------------------------------------------
            else:
                for element in values:
                    if values[0] == element[0]:
                        db.remove([values], table_reference)

                    else:
                        pass

            for entry in entries:
                entry.delete(0, tk.END)
    
    action_btn = ttk.Button(frame, text="Concluir", command=getter)
    action_btn.grid(row=len(args), column=2, sticky="e")

def table_complete(frame, table_reference):

    """Creates a tableview with data fetched from SQLite data base."""

    match table_reference:
        case 'products':
            data = db.fetcher('products')
            table = Tableview(master= frame,
                                coldata = ('ID', 'Nome', 'Custo', 'Valor'),
                                rowdata = data,
                                paginated = True,
                                pagesize= 10,
                                searchable=True)
            table.grid()
            table.load_table_data()
            table.autofit_columns()
            table.autoalign_columns()
        
        case 'clients':
            data = db.fetcher('clients')
            table = Tableview(master= frame,
                                coldata = ('ID', 'Nome', 'CEP', 'Telefone'),
                                rowdata = data,
                                paginated = True,
                                pagesize= 10,
                                searchable=True)
            table.grid()
            table.load_table_data()
            table.autofit_columns()
            table.autoalign_columns()
        
        case 'sales':
            data = db.fetcher('sales')
            table = Tableview(master= frame,
                                coldata = ('ID', 'Data', 'Quantidade', 'Valor Total'),
                                rowdata = data,
                                paginated = True,
                                pagesize= 10,
                                searchable=True)
            table.grid()
            table.load_table_data()
            table.autofit_columns()
            table.autoalign_columns()
    
    return table