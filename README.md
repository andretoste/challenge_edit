# Startup Data Challenge - Insights Sustentáveis com Parquet

## Descrição do Projeto

Este projeto foi desenvolvido como parte do desafio final do bootcamp de DataOps. O objetivo foi criar uma solução que processasse dados de sensores ambientais (armazenados num arquivo Parquet), gerasse insights relevantes sobre sustentabilidade e os apresentasse de forma clara e útil para empresas.

## Arquivos do Projeto

*   `exploracao_dados.py`: Script Python para exploração inicial dos dados.
*   `analise_insights.py`: Script Python para análise e geração de insights.
*   `dashboard.py`: Script Python para criação do dashboard interativo usando Streamlit.
*   `dados_sensores_5000.parquet`: Arquivo Parquet com os dados (deve ser colocado na mesma pasta dos scripts).
*   `README.md`: Este arquivo.

## Como Executar o Projeto

1.  Certifique-se de ter o Python 3 instalado.

2.  Instale as bibliotecas necessárias: `pandas`, `streamlit` e `matplotlib` (caso não tenha instalado).
    ```bash
    pip install pandas streamlit matplotlib
    ```

3.  Mova o arquivo `dados_sensores_5000.parquet` para a mesma pasta dos scripts.

4.  Execute o dashboard interativo:
    ```bash
    streamlit run dashboard.py
    ```

5.  O dashboard será aberto no seu navegador.

## Funcionalidades

### Exploração de Dados: 
O arquivo `exploracao_dados.py` permite analisar a estrutura dos dados.

### Análise e Geração de Insights: 
O arquivo `analise_insights.py` calcula métricas de consumo de energia, água e emissões de CO2 por setor, identifica as empresas com maior consumo e analisa a correlação entre as métricas.

### Dashboard Interativo: 
O arquivo `dashboard.py` cria um painel interativo usando Streamlit, onde o usuário pode visualizar o consumo por setor, as empresas com maior consumo e a correlação entre as métricas. O dashboard possui um filtro por setor.

## Insights Principais

### O setor de Varejo se destaca como o maior consumidor de energia, água e emissor de CO2, seguido de perto por Indústria.

### As empresas com maiores consumos variam em cada métrica (energia, água e CO2).

### A correlação entre as métricas é baixa.

### Os insights e dados variam com o uso do filtro de setor.

## Próximos Passos

### Implementar outras visualizações de dados.

### Adicionar outras métricas úteis para análise.

### Criar sistema de alerta para as empresas que ultrapassem limites sustentáveis.

## Contato

### André Toste

### <andre.toste@gmail.com>

### [https://github.com/andretoste](https://github.com/andretoste)