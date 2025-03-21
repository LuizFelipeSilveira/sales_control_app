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
    

    def add(self):
        pass
    

    def remove(self):
        pass


    def fetch(self):
        pass


    def _open_conn(self):
        self.conn = sqlite3.connect("sales_force.db")
    

    def _close_conn(self):
        self.conn.close()


class App():
    def __init__(self):
        self.root = ttk.Window(themename="solar")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

        self.entries = list()

        db = Database()

    def send_to_db(self):
        values = [entry.get() for entry in self.entries]

    
    def add_frame(self, frame, widgets=None):
        
        if frame == 'root':
            frame = ttk.Frame(self.root)
        else:
            frame = ttk.Frame(frame)
        
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
                                                              'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self.send_to_db}})
                
                frame_remove = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                                  'entry_1':{'row':0, 'column':1},
                                                                  'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e'}})
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
                                                              'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self.send_to_db}})
                
                frame_remove = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                                  'entry_1':{'row':0, 'column':1},
                                                                  'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e'}})
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
                                                              'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e', 'command':self.send_to_db}})
                
                frame_remove = self.add_frame(notebook, widgets={'label_1':{'text':'Id', 'row':0, 'column':0},
                                                                  'entry_1':{'row':0, 'column':1},
                                                                  'button':{'text':'Enviar', 'row':4, 'column':1, 'sticky':'e'}})
                notebook.add(frame_add, text='Cadastrar')
                notebook.add(frame_remove, text='Descadastrar')


    def _add_label(self, frame, parameters=dict()):
        label = ttk.Label(frame, text=parameters['text'], font=('Helvetica', 10))
        label.grid(row=parameters['row'], column=parameters['column'], padx=10)


    def _add_button(self, frame, parameters=dict()):
        button = ttk.Button(frame, text=parameters['text'], padding=8)
        button.grid(row=parameters['row'], column=parameters['column'], padx=5, pady=5, sticky=parameters['sticky'])
    

    def _add_entry(self, frame, parameters=dict()):
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=parameters['row'], column=parameters['column'], padx=5, pady=5)
        
        self.entries.append(entry)
        

    
    def _add_table(self, frame, parameters=dict()):
        table = Tableview(master=frame,
                          coldata=parameters['coldata'],
                          rowdata=parameters['rowdata'],
                          paginated=parameters['paginated'],
                          pagesize=parameters['pagesize'],
                          searchable=parameters['searchable'])
    

    def run(self):
        self.root.mainloop()



#--------------------------------------------------------------------------------------------------------------


app = App()

app.add_frame(frame='root', widgets={'label':{'text':'Controle',
                                              'font':('Helvetica', 16),
                                              'row':0,
                                              'column':0,
                                              'columnspan':2}})
                                              


left_frame = app.add_label_frame(frame='root', row=1, column=0, padding=10, padx=10, pady=10, sticky="nsew", bootstyle="primary", text="Produtos")
app.add_notebook(left_frame, 'products')

center_frame = app.add_label_frame(frame='root', row=1, column=1, padding=10, padx=10, pady=10, sticky="nsew", bootstyle="primary", text="Clientes")
app.add_notebook(center_frame, 'clients')

right_frame = app.add_label_frame(frame='root', row=1, column=2, padding=10, padx=10, pady=10, sticky="nsew", bootstyle="primary", text="Vendas")
app.add_notebook(right_frame, 'sales')

app.run()