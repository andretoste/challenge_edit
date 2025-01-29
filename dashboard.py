# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_chat import message

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

# Função para obter resposta do chatbot
def chatbot_response(df, question):
    question = question.lower()
    if "setor que mais consome energia" in question:
        consumo = consumo_por_setor(df)
        max_consumo = consumo['energia_kwh'].idxmax()
        return f"O setor que mais consome energia é o **{max_consumo}**."
    elif "empresa que mais consome água" in question:
        top_agua = df.nlargest(1,'agua_m3')
        empresa = top_agua['empresa'].iloc[0]
        return f"A empresa que mais consome água é a **{empresa}**"
    elif "média de emissões de co2" in question:
       media_co2 = df['co2_emissoes'].mean()
       return f"A média de emissões de CO2 é de **{media_co2:.2f}**."
    elif "consumo de energia do setor" in question:
      setores = list(df['setor'].unique())
      for setor in setores:
        if setor in question:
           consumo = consumo_por_setor(df)
           consumo_setor = consumo.loc[setor,'energia_kwh']
           return f"O setor **{setor}** tem um consumo de energia de **{consumo_setor:.2f}**."
      return "Não entendi a sua pergunta. Tente algo como 'Qual o setor que mais consome energia?'"
    else:
        return "Não entendi a sua pergunta. Tente algo como 'Qual o setor que mais consome energia?'"


# Configurar a página
st.set_page_config(page_title="Dashboard Sustentabilidade", layout="wide")

# Título do Dashboard
st.title("Dashboard de Sustentabilidade")

# Carregar os dados
df = carregar_dados()
if df is None:
    st.stop()

# Barra Lateral
st.sidebar.header("Controles")

# Filtro de Setor
todos_setores = ['Todos'] + list(df['setor'].unique())
filtro_setor = st.sidebar.selectbox("Filtrar por setor", options=todos_setores)

# Chatbot
st.sidebar.header("Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message_chat in st.session_state.messages:
    with st.sidebar.chat_message(message_chat["role"]):
        st.markdown(message_chat["content"])

if prompt := st.sidebar.chat_input("Faça sua pergunta"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.sidebar.chat_message("user"):
      st.markdown(prompt)
  response = chatbot_response(df,prompt)
  st.session_state.messages.append({"role": "assistant", "content": response})
  with st.sidebar.chat_message("assistant"):
      st.markdown(response)


# Slider de Empresas
n_top = st.slider("Top empresas", min_value=1, max_value=10, value=5)

# Layout Principal
col1, col2 = st.columns([1,2])

with col1:
    # Medidor de Consumo Total
    st.header("Consumo Total de Energia")
    total_consumo = df['energia_kwh'].sum()
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_consumo,
        title = {'text': "Total de Energia (kWh)"},
        gauge = {'axis': {'range': [None, total_consumo*1.1]},
                'bar': {'color': "green"},
                'steps' : [
                    {'range': [0, total_consumo*0.5], 'color': "red"},
                    {'range': [total_consumo*0.5, total_consumo*0.75], 'color': "yellow"},
                    {'range': [total_consumo*0.75, total_consumo*1.1], 'color': "green"}
                    ]}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)


with col2:
    # 1. Gráfico de barras
    st.header("Consumo por Setor (Gráfico de barras)")
    consumo_setor = consumo_por_setor(df, filtro_setor if filtro_setor != 'Todos' else None).reset_index()
    fig_bar = px.bar(consumo_setor, x='setor', y=['energia_kwh', 'agua_m3', 'co2_emissoes'], barmode='group')
    st.plotly_chart(fig_bar, use_container_width=True)


# 2. Empresas com maior consumo
st.header("Empresas com maior consumo")
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