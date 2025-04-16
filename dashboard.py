import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import altair as alt

st.set_page_config(page_title="Dados Gerais", layout='wide')
st.title("Dados Gerais")

conn = sqlite3.connect("sales_database.db")
cursor = conn.cursor

df_sales = pd.read_sql_query("SELECT * FROM sales", conn)
df_products = pd.read_sql_query("SELECT * FROM products", conn)
df_clients = pd.read_sql_query("SELECT * FROM clients", conn)

df_best_products = pd.read_sql_query("SELECT p.name, p.cost, p.price, s.quantity FROM products as p INNER JOIN sales as s ON p.id = s.id_product", conn) 
df_best_products['profit'] = (df_best_products['price'] - df_best_products['cost']) * df_best_products['quantity']

col_1, col_2, col_3, col_4 = st.columns(4)

with col_1:
    st.metric("Total de Vendas", f"R${df_sales['total_value'].sum():.2f}")

with col_2:
    st.metric("Quantidade de Vendas", f"{df_sales.groupby('id').size().count()}")

with col_3:
    st.metric("Produtos Cadastrados", df_products.shape[0])

with col_4:
    st.metric("Clientes Cadastrados", df_clients.shape[0])


st.subheader("Faturamento por dia")
sales_by_day = df_sales.groupby(df_sales['date'])['total_value'].sum()
st.line_chart(sales_by_day)

sold_best = df_best_products.groupby('name')['quantity'].sum().sort_values(ascending=False)
best_profit = df_best_products.groupby('name')['profit'].sum().sort_values(ascending=False)

df_sold = sold_best.reset_index()
df_profit = best_profit.reset_index()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Produtos mais vendidos")
    chart1 = alt.Chart(df_sold).mark_bar().encode(
        x=alt.X('quantity:Q', title='Quantidade'),
        y=alt.Y('name:N', sort='-x', title='Produto'),
        tooltip=['name', 'quantity']
    ).properties(height=400)
    st.altair_chart(chart1, use_container_width=True)

with col2:
    st.subheader("Produtos mais lucrativos")
    chart2 = alt.Chart(df_profit).mark_bar(color='orange').encode(
        x=alt.X('profit:Q', title='Lucro'),
        y=alt.Y('name:N', sort='-x', title='Produto'),
        tooltip=['name', 'profit']
    ).properties(height=400)
    st.altair_chart(chart2, use_container_width=True)