# analise_insights.py

import pandas as pd
import matplotlib.pyplot as plt # Biblioteca para criar gráficos

# 1. Caminho para o seu arquivo Parquet
caminho_arquivo = 'dados_sensores_5000.parquet' # Ajustar se necessário

# 2. Carregar o arquivo Parquet
try:
    df = pd.read_parquet(caminho_arquivo)
    print("Arquivo Parquet carregado com sucesso!\n")
except FileNotFoundError:
    print("Erro: Arquivo Parquet não encontrado. Verifique o caminho.")
    exit()


# 3. Cálculo do consumo por setor
print("--- Consumo por setor ---")
consumo_por_setor = df.groupby('setor')[['energia_kwh', 'agua_m3', 'co2_emissoes']].sum()
print(consumo_por_setor)
print("\n")

# 4. Identificação de empresas com consumo excessivo
print("--- Empresas com maior consumo ---")
top_empresas_energia = df.nlargest(5, 'energia_kwh')
top_empresas_agua = df.nlargest(5, 'agua_m3')
top_empresas_co2 = df.nlargest(5, 'co2_emissoes')

print("\nTop 5 empresas com maior consumo de energia:\n", top_empresas_energia[['empresa','energia_kwh']])
print("\nTop 5 empresas com maior consumo de agua:\n", top_empresas_agua[['empresa','agua_m3']])
print("\nTop 5 empresas com maior emissão de CO2:\n", top_empresas_co2[['empresa','co2_emissoes']])
print("\n")

# 5. Comparação entre setores (criação de gráficos)
# Se quiseres usar gráficos comente as seguintes linhas:
consumo_por_setor.plot(kind='bar', figsize=(10, 6))
plt.title('Consumo por Setor')
plt.xlabel('Setor')
plt.ylabel('Consumo')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 6. Identificação de padrões (Exemplo: correlação entre métricas)
correlacao = df[['energia_kwh', 'agua_m3', 'co2_emissoes']].corr()
print("--- Correlação entre métricas ---")
print(correlacao)
print("\n")