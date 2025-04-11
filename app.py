import datetime
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
        cep TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)
        
        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales
    (
        id INTEGER NOT NULL,
        id_client TEXT NOT NULL,
        id_product TEXT NOT NULL,
        date TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_value REAL NOT NULL,
        FOREIGN KEY (id_client) REFERENCES clients(id),
        FOREIGN KEY (id_product) REFERENCES products(id)
    )
    """)


    def add(self, reference_list, table):

        match table:
            case 'products':
                try:
                    sql=("""INSERT INTO products (id, name, cost, price)
                            VALUES (?, ?, ?, ?)""")
                    self.cursor.execute(sql, reference_list) 
                except:
                    pass              

            case 'clients':
                try:
                    sql=("""INSERT INTO clients (id, name, cep, phone)
                        VALUES (?, ?, ?, ?)""")
                    self.cursor.execute(sql, reference_list)  
                except:
                    pass

            case 'sales':

                try:
                    sql=("""INSERT INTO sales (id, id_client, id_product, date, quantity, total_value)
                        VALUES (?, ?, ?, ?, ?, ?)""")
                    self.cursor.execute(sql, reference_list) 
                except:
                    pass

        self.conn.commit()           
    

    def remove(self, reference_value, table):
        match table:
            case 'products':
                try:
                    sql = ("""DELETE FROM products WHERE id = ?""")
                    self.cursor.execute(sql, reference_value)
                except:
                    pass
            case 'clients':
                try:
                    sql = ("""DELETE FROM clients WHERE id = ?""")
                    self.cursor.execute(sql, reference_value)
                except:
                    pass
            case 'sales':
                try:
                    sql = ("""DELETE FROM sales WHERE id = ?""")
                    self.cursor.execute(sql, reference_value)
                except:
                    pass
        self.conn.commit()


    def fetch(self, table):
        self.cursor.execute(f"""SELECT * FROM {table}""")
        data = self.cursor.fetchall()
        return data


    def _open_conn(self):
        self.conn = sqlite3.connect("sales_database.db")
    

    def _close_conn(self):
        self.conn.close()


class App():
    def __init__(self):
        self.root = ttk.Window(themename="solar")
        self.root.title('Sales Control')

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

        self.entries = list()

        self.db = Database()

    def _send_to_db(self):
        values = [entry.get() for entry in self.entries]
        values = self._validate_values(values)

        if values[0] != '' and values[1] != '' and values[2] != '' and values[3] != '':
            self.db.add(values[0:4],'products')
            for i in range(4):
                self.entries[i].delete(0, tk.END)
            
            data = self.db.fetch('products')
            self._add_table(left_frame, parameters={'coldata':['ID', 'Nome', 'Custo', 'Valor'],
                                                    'rowdata':data})
        
        elif values[4] != '':
            self.db.remove(values[4], 'products')
            self.entries[4].delete(0, tk.END)
            data = self.db.fetch('products')
            self._add_table(left_frame, parameters={'coldata':['ID', 'Nome', 'Custo', 'Valor'],
                                                    'rowdata':data})
        

        elif values[5] != '' and values[6] != '' and values[7] != '' and values[8] != '':
            self.db.add(values[5:9],'clients')
            for i in range(5,9):
                self.entries[i].delete(0, tk.END)
            data = self.db.fetch('clients')
            self._add_table(center_frame, parameters={'coldata':['ID', 'Nome', 'CEP', 'Telefone'],
                                                    'rowdata':data})
        
        elif values[9] != '':
            self.db.remove(values[9], 'clients')
            self.entries[9].delete(0, tk.END)
            data = self.db.fetch('clients')
            self._add_table(center_frame, parameters={'coldata':['ID', 'Nome', 'CEP', 'Telefone'],
                                                    'rowdata':data})
        
        elif values[10] != '' and values[11] != '' and values[12] != '' and values[13] != '':          
            id_product = values[12]

            sql = """SELECT price FROM products WHERE id = ?"""

            self.db.cursor.execute(sql, (id_product,))

            price_product = self.db.cursor.fetchone()
            price_product = price_product[0]
            total = price_product * values[13]
            values.insert(14, total)
            values.insert(13, datetime.date.today())

            self.db.add(values[10:16],'sales')
            
            for i in range(10,14):
                self.entries[i].delete(0, tk.END)
            
            data = self.db.fetch('sales')
            self._add_table(right_frame, parameters={'coldata':['ID', 'ID Cliente', 'ID Produto', 'Data', 'Quantidade', 'Valor Total'],
                                                    'rowdata':data})

        elif values[14] != '':
            self.db.remove(values[14], 'sales')
            self.entries[14].delete(0, tk.END)
            data = self.db.fetch('sales')
            self._add_table(right_frame, parameters={'coldata':['ID', 'ID Cliente', 'ID Produto', 'Data', 'Quantidade', 'Valor Total'],
                                                    'rowdata':data})
            
    
    def add_frame(self, frame, widgets=None):
        
        if frame == 'root':
            frame = ttk.Frame(self.root)
            frame.grid(row=0, column=0, columnspan=3)
        else:
            frame = ttk.Frame(frame)
            frame.grid(row=0, column=0, columnspan=3)
        
        if widgets:
            for key, value in widgets.items():
                if key.startswith('label'):
                    self._add_label(frame, value)

                elif key.startswith('entry'):
                    self._add_entry(frame, value)

                elif key.startswith('button'):
                    self._add_button(frame, value)
                
                elif key.startswith('entry'):
                    self._add_entry(frame, value)
        return frame
                
    
    def add_label_frame(self, frame, row=0, column=0, padding=None, text=str, bootstyle=None, sticky=None, padx=None, pady=None, widgets=None):
        
        if frame == 'root':
            frame = ttk.LabelFrame(self.root, padding=padding, text=text, bootstyle=bootstyle)
            frame.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        else:
            frame = ttk.LabelFrame(frame, padding=padding, text=text, bootstyle=bootstyle)
            frame.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        
        if widgets:
            for key, value in widgets.items():
                if key.startswith('label'):
                    self._add_label(frame, value)

                elif key.startswith('entry'):
                    self._add_entry(frame, value)

                elif key.startswith('button'):
                    self._add_button(frame, value)
                
                elif key.startswith('entry'):
                    self._add_entry(frame, value)
                
                elif key.startswith('table'):
                    self._add_table(frame, value)
        return frame


    def add_notebook(self, frame, table):
        notebook = ttk.Notebook(frame)
        notebook.grid(row=0, column=0, sticky='nsew')

        match table:
            case 'products':
                frame_add = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                              'entry_1':{'row':0, 'column':1},
                                                              'label_2':{'text':'Nome', 'row':1, 'column':0},
                                                              'entry_2':{'row':1, 'column':1},
                                                              'label_3':{'text':'Custo', 'row':2, 'column':0},
                                                              'entry_3':{'row':2, 'column':1},
                                                              'label_4':{'text':'Valor', 'row':3, 'column':0},
                                                              'entry_4':{'row':3, 'column':1},
                                                              'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self._send_to_db}})
                
                frame_remove = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                                  'entry_1':{'row':0, 'column':1},
                                                                  'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self._send_to_db}})
                notebook.add(frame_add, text='Cadastrar')
                notebook.add(frame_remove, text='Descadastrar')

            case 'clients':
                frame_add = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                              'entry_1':{'row':0, 'column':1},
                                                              'label_2':{'text':'Nome', 'row':1, 'column':0},
                                                              'entry_2':{'row':1, 'column':1},
                                                              'label_3':{'text':'CEP', 'row':2, 'column':0},
                                                              'entry_3':{'row':2, 'column':1},
                                                              'label_4':{'text':'Telefone', 'row':3, 'column':0},
                                                              'entry_4':{'row':3, 'column':1},                                                             
                                                              'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self._send_to_db}})
                
                frame_remove = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                                  'entry_1':{'row':0, 'column':1},
                                                                  'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self._send_to_db}})
                notebook.add(frame_add, text='Cadastrar')
                notebook.add(frame_remove, text='Descadastrar')

            case 'sales':
                frame_add = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                              'entry_1':{'row':0, 'column':1},
                                                              'label_2':{'text':'Id Cliente', 'row':1, 'column':0},
                                                              'entry_2':{'row':1, 'column':1},
                                                              'label_3':{'text':'Id Produto', 'row':2, 'column':0},
                                                              'entry_3':{'row':2, 'column':1},
                                                              'label_4':{'text':'Quantidade', 'row':3, 'column':0},
                                                              'entry_4':{'row':3, 'column':1},
                                                              'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self._send_to_db}})
                
                frame_remove = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                                  'entry_1':{'row':0, 'column':1},
                                                                  'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self._send_to_db}})
                notebook.add(frame_add, text='Cadastrar')
                notebook.add(frame_remove, text='Descadastrar')


    def _add_label(self, frame, parameters=dict()):
        label = ttk.Label(frame, text=parameters['text'], font=('Helvetica', 10))
        label.grid(row=parameters['row'], column=parameters['column'], padx=10)


    def _add_button(self, frame, parameters=dict()):
        button = ttk.Button(frame, text=parameters['text'], padding=8, command=parameters['command'])
        button.grid(row=parameters['row'], column=parameters['column'], padx=5, pady=5, sticky=parameters['sticky'])
    

    def _add_entry(self, frame, parameters=dict()):
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=parameters['row'], column=parameters['column'], padx=5, pady=5)
        
        self.entries.append(entry)
        

    
    def _add_table(self, frame, parameters=dict()):
        table = Tableview(master=frame,
                          coldata=parameters['coldata'],
                          rowdata=parameters['rowdata'],
                          paginated=True,
                          pagesize=10,
                          searchable=True,
                          autoalign=True,
                          autofit=True)
        table.grid(row=1, column=0)
    

    def _validate_values(self, reference_list):
            for i in range(len(reference_list)):
                if i == 0 or i == 1 or i == 4 or i == 5 or i == 6 or i == 9 or i == 10 or i == 10 or i == 11 or i == 12 or i == 14:
                    reference_list[i] = reference_list[i].upper()

                elif i == 2 or i == 3:
                    if ',' in reference_list[i]:
                        reference_list[i] = reference_list[i].replace(',','.')
                    try:
                        reference_list[i] = float(reference_list[i])
                    except:
                        reference_list[i] = ''

                elif i == 13:
                    try:
                        reference_list[i] = int(reference_list[i])
                    except:
                        reference_list[i] = ''
            return reference_list


    def run(self):
        self.root.mainloop()
        self.db._close_conn()


app = App()

app.add_frame(frame='root', widgets={'button_1':{'text':'Dashboard', 'row':0, 'column':0, 'sticky':'e', 'command':None}})
                                              

data = app.db.fetch('products')
left_frame = app.add_label_frame(frame='root', row=1, column=0, padding=10, padx=10, pady=10, sticky="nsew", bootstyle="primary", text="Produtos",widgets={'table':{'coldata':['ID', 'Nome', 'Custo', 'Valor'],
                                                                                                                                                                    'rowdata':data}})                                                      
app.add_notebook(left_frame, 'products')

data = app.db.fetch('clients')
center_frame = app.add_label_frame(frame='root', row=1, column=1, padding=10, padx=10, pady=10, sticky="nsew", bootstyle="primary", text="Clientes",widgets={'table':{'coldata':['ID', 'Nome', 'CEP', 'Telefone'],
                                                                                                                                                                      'rowdata':data}})
app.add_notebook(center_frame, 'clients')

data = app.db.fetch('sales')
right_frame = app.add_label_frame(frame='root', row=1, column=2, padding=10, padx=10, pady=10, sticky="nsew", bootstyle="primary", text="Vendas",widgets={'table':{'coldata':['ID', 'ID Cliente', 'ID Produto', 'Data', 'Quantidade', 'Valor Total'],
                                                                                                                                                                   'rowdata':data}})
app.add_notebook(right_frame, 'sales')

app.run()