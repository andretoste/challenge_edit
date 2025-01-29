# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar os dados
def carregar_dados():
    try:
        df = pd.read_parquet('dados_sensores_5000.parquet')  # Ajustar se necessário
        return df
    except FileNotFoundError:
        st.error("Arquivo Parquet não encontrado. Verifique o caminho.")
        return None

# Função para calcular o consumo por setor
def consumo_por_setor(df, filtro_setor=None):
    if filtro_setor:
        df_filtrado = df[df['setor'] == filtro_setor]
    else:
        df_filtrado = df
    return df_filtrado.groupby('setor')[['energia_kwh', 'agua_m3', 'co2_emissoes']].sum()

# Função para identificar empresas com maior consumo
def top_empresas(df, n=5, filtro_setor=None):
    if filtro_setor:
        df = df[df['setor'] == filtro_setor]
    top_empresas_energia = df.nlargest(n, 'energia_kwh')
    top_empresas_agua = df.nlargest(n, 'agua_m3')
    top_empresas_co2 = df.nlargest(n, 'co2_emissoes')
    return top_empresas_energia, top_empresas_agua, top_empresas_co2

# Configurar a página
st.set_page_config(page_title="Dashboard Sustentabilidade", layout="wide")

# Título do Dashboard
st.title("Dashboard de Sustentabilidade")

# Carregar os dados
df = carregar_dados()
if df is None:
    st.stop()

# Filtro de Setor
st.sidebar.header("Filtros")
todos_setores = ['Todos'] + list(df['setor'].unique())
filtro_setor = st.sidebar.selectbox("Setor:", options=todos_setores)

# 1. Consumo por setor
st.header("Consumo por Setor")
col1, col2 = st.columns(2)
with col1:
  consumo = consumo_por_setor(df, filtro_setor if filtro_setor != 'Todos' else None)
  st.dataframe(consumo)

with col2:
  fig, ax = plt.subplots()
  consumo.plot(kind='bar', ax=ax, figsize=(8,5))
  st.pyplot(fig)

# 2. Empresas com maior consumo
st.header("Empresas com maior consumo")
n_top = st.slider("Número de Empresas", min_value=1, max_value=10, value=5)
top_energia, top_agua, top_co2 = top_empresas(df, n_top, filtro_setor if filtro_setor != 'Todos' else None)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Energia")
    st.dataframe(top_energia[['empresa','energia_kwh']])
with col2:
    st.subheader("Água")
    st.dataframe(top_agua[['empresa','agua_m3']])
with col3:
    st.subheader("CO2")
    st.dataframe(top_co2[['empresa','co2_emissoes']])

# 3. Correlação entre métricas
st.header("Correlação entre Métricas")
if filtro_setor != 'Todos':
  df_filtrado = df[df['setor'] == filtro_setor]
  correlacao = df_filtrado[['energia_kwh', 'agua_m3', 'co2_emissoes']].corr()
else:
    correlacao = df[['energia_kwh', 'agua_m3', 'co2_emissoes']].corr()
st.dataframe(correlacao)