from utilities import *

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