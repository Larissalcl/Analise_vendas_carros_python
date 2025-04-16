# Objetivo: analisar as marcas de carros mais vendidos segundo preço e local.

# Passo 4: Análise das vendas
# Passo 5: Análise das causas das vendas

# Passo 1: Importar base de dados e ajustar a exibição
import pandas as pd

pd.set_option('display.width', None) #Ajustar a exibição para ocupar toda a largura disponível.
pd.set_option('display.max_columns', None) #Mostrar todas as colunas do DataFrame.

df_original = pd.read_csv('vendas_carros.csv', sep=';')
print(df_original.head())

# Passo 2: Visualizar os dados
df = df_original.drop(columns=['ID', 'NOME'])
print('\n Df sem dados desnecessários: \n', df.head())

# Passo 3: Corrigir as bases de dados
# Axis = 1-coluna, 0- linha e o inplace = executar o comando no proprio df

print(df.info())

linhas_com_nulos = df[df.isnull().any(axis=1)] #Verificar as linhas com qualquer valor nulo.
print('Linha com valores nulos: \n ', linhas_com_nulos)

indice_da_linha = 875
df.at[indice_da_linha, 'MARCA'] = 'Honda' #Atualizar dado da linha

df = df.dropna() #Excluir as linhas vazias

print(df.info())

df['PREÇO'] = df['PREÇO'].str.replace('.', '', regex=False) #Ajustar formato para float.
df['PREÇO'] = df['PREÇO'].str.replace(',', '', regex=False) # Substituir o ponto por uma string vazia.

df ['PREÇO'] = df ['PREÇO'].astype(float) #Ajustar formato para float.
df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%y', errors='coerce') #Ajustar formato para data
print(df.info())

print('Qtd registros atual:', df.shape[0]) #0 - linhas
df.drop_duplicates() #Remover linhas duplicadas.
print('Qtd de resgitros removendo as duplicadas:', len(df)) # len também mostra o número de linhas


df.to_csv('vendas_carros_tratado.csv', index=False)

# Passo 4: Análise das vendas
# quantas vendas por marcas / país

qte_por_marca_resumo = df.groupby('MARCA')['PAÍS'].count()
qte_por_marca = df.groupby('MARCA')['PAÍS'].value_counts()

print("\nContagem das marcas por país:\n", qte_por_marca)
print("\nNº de carros vendidos por marca:\n", qte_por_marca_resumo)

qte_por_marca_percentagem = (df["MARCA"].value_counts(normalize=True).map("{:.1%}".format))
print("\n Nº de carros vendidos por marca:\n", qte_por_marca_percentagem)

qte_por_pais_percentagem = (df["PAÍS"].value_counts(normalize=True).map("{:.1%}".format))
print("\n Nº de carros vendidos por país:\n", qte_por_pais_percentagem)

#Passo 5: Criar os gráficos (Análise da causa - como as colunas impactam nas vendas)

import plotly.express as px

for coluna in df.columns:
    grafico = px.histogram(df, x=coluna, color='MARCA')
    grafico.show()