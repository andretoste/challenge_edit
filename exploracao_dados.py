# exploracao_dados.py

import pandas as pd

# 1. Caminho para o seu arquivo Parquet
caminho_arquivo = 'dados_sensores_5000.parquet' # Caminho relativo

# 2. Carregar o arquivo Parquet
try:
    df = pd.read_parquet(caminho_arquivo)
    print("Arquivo Parquet carregado com sucesso!")
except FileNotFoundError:
    print("Erro: Arquivo Parquet não encontrado. Verifique o caminho.")
    exit()

# 3. Explorar a estrutura do DataFrame

print("\n--- Informações Gerais ---")
print(f"Número de linhas: {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")

print("\n--- Tipos de Dados ---")
print(df.dtypes)

print("\n--- Estatísticas Descritivas ---")
print(df.describe())

print("\n--- Primeiras Linhas ---")
print(df.head())

print("\n--- Informações Nulas ---")
print(df.isnull().sum())

# Opcional: Limpeza e tratamento inicial (adicionar conforme necessário)
# Exemplo: df = df.fillna(0) # Substituir valores nulos por 0