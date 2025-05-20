import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import altair as alt
import datetime

st.set_page_config(page_title="Dados Gerais", layout='wide')
st.title("Dados de Vendas")
st.divider()

@st.cache_data
def get_df():
    conn = sqlite3.connect("sales_database.db")
    cursor = conn.cursor

    sales = pd.read_sql_query("SELECT * FROM sales", conn)
    sales['date'] = pd.to_datetime(sales['date'], format= '%Y-%m-%d')
    sales['month'] = sales['date'].dt.month
    sales['date'] = sales['date'].dt.date
    products = pd.read_sql_query("SELECT * FROM products", conn)
    clients = pd.read_sql_query("SELECT * FROM clients", conn)
    best_products = pd.read_sql_query("SELECT p.name, p.cost, p.price, s.quantity, s.date, s.total_value FROM products as p INNER JOIN sales as s ON p.id = s.id_product", conn) 
    best_products['date'] = pd.to_datetime(best_products['date']).dt.date
    best_products['profit'] = (best_products['price'] - best_products['cost']) * best_products['quantity']

    conn.close()
    return sales, products, clients, best_products


df_sales, df_products, df_clients, df_best_products = get_df()

st.sidebar.subheader('Filtro de dados')

date_range = st.sidebar.slider('Filtro de dados',
                               label_visibility= 'hidden',
                               min_value=df_sales['date'].min(),
                               max_value=df_sales['date'].max(),
                               value=(df_sales['date'].min(), df_sales['date'].max()),
                               format='DD/MM/YYYY')


df_filter_sales = df_sales[(df_sales['date'] >= date_range[0]) & (df_sales['date'] <= date_range[1])]
df_filter_best_products = df_best_products[(df_best_products['date'] >= date_range[0]) & (df_best_products['date'] <= date_range[1])]

total_revenue = df_filter_sales['total_value'].sum()
amount_sales = df_filter_sales.groupby('id')['quantity'].sum().sum()
avg_ticket = total_revenue/amount_sales
avg_profit = df_filter_best_products['profit'].mean()

col_1, col_2, col_3, col_4 = st.columns(4)

with col_1:
    st.markdown('#### Faturamento Total')
    st.markdown(f'##### R$ {total_revenue:.2f}')

with col_2:
    st.markdown('#### Total de vendas')
    st.markdown(f'##### {amount_sales}')

with col_3:
    st.markdown('#### Ticket Médio')
    st.markdown(f'##### R$ {avg_ticket:.2f}')

with col_4:
    st.markdown('#### Lucro Médio')
    st.markdown(f'##### R$ {avg_profit:.2f}')

st.divider()

sales_data = df_filter_sales.groupby('date')['total_value'].sum().reset_index()

st.subheader('Faturamento por dia :chart:')
st.line_chart(sales_data, x='date', y='total_value',x_label='Data', y_label='Faturamento (R$)')

st.divider()

st.subheader('Faturamento médio por mês')

sales_data = df_filter_sales.groupby('month')['total_value'].mean().reset_index()
st.bar_chart(sales_data, x='month', y='total_value', x_label= 'Mês', y_label='Faturamento Médio (R$)')