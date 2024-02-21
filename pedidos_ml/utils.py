#Test cloud build 9

import pygsheets
from google.oauth2 import service_account
import pandas as pd
import numpy as np
from datetime import datetime,date
from auth import *
import re

############################################################
#                    AUTENTICAÇÕES                         #
############################################################

#! Autenticação - Google GCP
def authenticate_gsheets(service_account_json, sheet_scopes):
  """Autentica com uma planilha google
  
  Args:
    service_account_json (json): json com os dados da conta de serviço gcp
    scopes (string): scopos usados na conexão com a API
  """
  print("A função authenticate_gsheets foi chamada!")
  
  sheets_gcp_credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes = sheet_scopes)
  sheets_client = pygsheets.authorize(custom_credentials = sheets_gcp_credentials)

  return(sheets_client)
#end def 

############################################################
#           GERAL - FUNÇÕES NORMALIZADORAS                 #
############################################################

#! Formatar datas - Por enquanto apenas datas do Mercado Livre
def formatar_data(data_string):
#
#    #? Data do Mercado Livre vem da seguinte maneira: 19 de fevereiro de 2024 19:35 hs.
#
#    data_formatada = datetime.strptime(data_string, "%d de %B de %Y %H:%M hs.")
#    return data_formatada.strftime("%d/%m/%Y")
#
  # Expressão regular para extrair dia, mês, ano, hora e minuto da string de data
  pattern = r'(\d{1,2}) de (\w+) de (\d{4}) (\d{2}):(\d{2}) hs\.'
  match = re.match(pattern, data_string)
  
  if match:
      day = int(match.group(1))
      month_name = match.group(2)
      year = int(match.group(3))
      hour = int(match.group(4))
      minute = int(match.group(5))
      
      # Mapear o nome do mês para um número de mês
      months = {
          'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
          'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
          'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
      }
      month = months.get(month_name.lower())
      
      if month:
          # Construir e retornar a data formatada
          return "{:02d}/{:02d}/{:04d}".format(day, month, year)
  
  # Se a correspondência falhar, lançar uma exceção ou retornar a string original, dependendo do seu caso
  raise ValueError("Formato de data inválido: {}".format(data_string))
#end def

#! Colar valores finais na aba output
def paste_values(sheet_client, spreadsheet_id, wks, df_final):
    #* Converter DataFrame para lista de listas
    values_to_paste = df_final.values.tolist()

    #* Verificar se há valores para colar
    if values_to_paste:

      #* Obter a coluna 'A' como uma lista
      coluna_a = wks.get_col(1, include_tailing_empty=False)
  
      #* Encontrar a última linha preenchida na coluna 'A'
      ultima_linha = len(coluna_a) + 1
  
      #* Atualizar os valores começando na próxima linha após a última preenchida na coluna 'A'
      wks.update_values(crange=f'A{ultima_linha}', values=values_to_paste)
#end def

############################################################
#                 REGRAS MERCADO LIVRE                     #
############################################################


################
    # ESPECIFICAÇÕES DE NORMALIZAÇÃO DO DATAFRAME
################
    
#! Retorna uma lista com as colunas desejadas para o dataframe final
def colunas_desejadas_ml():
  colunas_desejadas             = ['N.º de venda', 'Data da venda', 'Status', 'Título do anúncio','Receita por produtos (BRL)', 'Total (BRL)', 'Forma de entrega']
  return colunas_desejadas
#end def

#! Captura lista com os status de cancelamento para serem removidos
def status_cancelados_ml():
  status_cancelado = ['Cancelada pelo comprador', 'Pacote cancelado pelo Mercado Livre', 'Venda cancelada. Não envie.', 'Cancelada', 'Você cancelou a venda']
  return status_cancelado
#end def

#! Captura os status de reembolso / devolução
def status_devolucao_ml():
  status_devolucao = ['Reclamação encerrada com reembolso para o comprador', 'Reclamação com devolução habilitada', 'Mediação finalizada com reembolso para o comprador', 'Devolução finalizada com reembolso para o comprador', 'Devolução para revisar', 'Devolvido no dia 19 de fevereiro', 'Mediação com devolução habilitada']
  return status_devolucao
#end def

#! Adicionando coluna Imposto
def coluna_imposto_ml(df):
  #* Definir a regra para calcular o imposto
  df['Imposto'] = np.where(df['Forma de entrega'] == 'Mercado Envios Flex', 0, 0.06)
  return df
#end def

#! Ajustando dados da coluna Receita por produtos (BRL)
#! Substituir os valores em branco por NaN, remove as linhas nulas, troca virgula por ponto e converte em Float
def ajuste_coluna_receita_ml(df):
  #* Corrigir valores em branco na coluna 'Receita por produtos (BRL)'
  df['Receita por produtos (BRL)'] = df['Receita por produtos (BRL)'].replace('', np.nan)

  #* Remover linhas com valores em branco na coluna 'Receita por produtos (BRL)'
  df = df.dropna(subset=['Receita por produtos (BRL)'])

  #* Substituir vírgulas por pontos na coluna 'Receita por produtos (BRL)'
  df['Receita por produtos (BRL)'] = df['Receita por produtos (BRL)'].str.replace(',', '.')

  #* Converter a coluna 'Receita por produtos (BRL)' para float
  df['Receita por produtos (BRL)'] = df['Receita por produtos (BRL)'].astype(float)

  return df
#end def

#! Ajustando dados da coluna Total (BRL)
#! Substitui ponto por virgula e converte em float
def ajuste_coluna_total_ml(df):
  #* Converter a nova coluna 'Total (BRL)' em float
  df['Total (BRL)'] = df['Total (BRL)'].str.replace(',', '.')
  df['Total (BRL)'] = df['Total (BRL)'].astype(float)

  return df

#! Cria a coluna Valor do Imposto multiplicando a receita pelo % do imposto
def coluna_valor_imposto_ml(df):
  #* Calcular a nova coluna 'Valor do Imposto' multiplicando a receita pelo % do imposto
  df['Valor do Imposto'] = np.where(df['Imposto'] == 0, 0, df['Receita por produtos (BRL)'] * df['Imposto'])
  df['Valor do Imposto'] = df['Valor do Imposto'].round(2)
  return df

################
    # MONTAGEM DO DATAFRAME DE PEDIDOS ENVIADOS
################

#! Recebe as informações e gera o dataframe de pedidos enviados
def df_enviados_ml(df, colunas_desejadas, status_cancelado, status_devolucao):
  
  #* Faz uma cópia do DataFrame e aplica a função para corrigir a data
  new_df                        = df[colunas_desejadas].copy()
  new_df['Data da venda']       = new_df['Data da venda'].apply(formatar_data)

  #* Removendo colunas duplicadas (Status)
  new_df = new_df.loc[:, ~new_df.columns.duplicated()]

  #* Remove os status de cancelamento
  new_df = new_df.loc[~new_df['Status'].isin(status_cancelado)]

  #* Remove os status de Reembolso
  new_df = new_df.loc[~new_df['Status'].isin(status_devolucao)]

  #* Alterando nomenclatura das devolução para Reembolso / Devolução
  #new_df['Status'] = new_df['Status'].replace(status_devolucao, 'Reembolso / Devolução')

  #* Criando a coluna de imposto
  new_df = coluna_imposto_ml(new_df)

  #* Ajustando coluna Receita por Produtos (BRL)
  new_df = ajuste_coluna_receita_ml(new_df)

  #* Ajustando coluna Receita por Total (BRL)
  new_df = ajuste_coluna_total_ml(new_df)

  #* Criando a coluna do Valor do Imposto
  new_df = coluna_valor_imposto_ml(new_df)

  return new_df
#end def

#! Cria o dataframe final do MercadoLivre de pedidos enviados para colar no sheets
def cria_df_enviados_ml(df):
  #* Cria matriz das colunas do dataframe final
  df_final = pd.DataFrame({
      'Data': df['Data da venda'],
      'Número da Venda': "'" + df['N.º de venda'].astype(str),
      'Item (nome)': df['Título do anúncio'],
      'MarketPlace': 'Mercado Livre',
      'Status': df['Status'],
      'Valor Nota (Total)': df['Receita por produtos (BRL)'],
      'Repasse': df['Total (BRL)'],
      'Imposto': df['Imposto'],
      'Valor do Imposto': df['Valor do Imposto'],
  })

  #* Remove linhas em branco
  df_final = df_final.fillna(0)

  #* Ordenar por data
  df_final = df_final.sort_values(by='Data', ascending=True)

  return df_final
#end def

################
    # MONTAGEM DO DATAFRAME DE PEDIDOS CANCELADOS
################

#! Recebe as informações e cria o dataframe de pedidos cancelados
def df_cancelados_ml(df, colunas_desejadas, status_cancelado):

  #* Faz uma cópia do DataFrame e aplica a função para corrigir a data
  new_df                        = df[colunas_desejadas].copy()
  new_df['Data da venda']       = new_df['Data da venda'].apply(formatar_data)

  #* Removendo colunas duplicadas (Status)
  new_df = new_df.loc[:, ~new_df.columns.duplicated()]

  #* Remove os status de cancelamento
  new_df = new_df.loc[new_df['Status'].isin(status_cancelado)]

  return new_df
#end def

#! Cria o dataframe final do mercadolivre para pedidos cancelados
def cria_df_cancelados_ml(df):
  #* Cria matriz das colunas do dataframe final
  df_final = pd.DataFrame({
      'Data': df['Data da venda'],
      'Número da Venda': "'" + df['N.º de venda'].astype(str),
      'Item (nome)': df['Título do anúncio'],
      'MarketPlace': 'Mercado Livre',
      'Status': df['Status'],
  })

  return df_final
#end def

################
    # MONTAGEM DO DATAFRAME DE PEDIDOS COM DEVOLUÇÃO / REEMBOLSO
################

#! Recebe as informações e cria o dataframe de pedidos com devolução / reembolso
def df_reembolso_ml(df, colunas_desejadas, status_devolucao_ml):

  #* Faz uma cópia do DataFrame e aplica a função para corrigir a data
  new_df                        = df[colunas_desejadas].copy()
  new_df['Data da venda']       = new_df['Data da venda'].apply(formatar_data)

  #* Removendo colunas duplicadas (Status)
  new_df = new_df.loc[:, ~new_df.columns.duplicated()]

  #* Remove os status de cancelamento
  new_df = new_df.loc[new_df['Status'].isin(status_devolucao_ml)]

  return new_df
#end def

#! Cria o dataframe final do mercadolivre para pedidos com devolução / reembolso
def cria_df_reembolso_ml(df):
  #* Cria matriz das colunas do dataframe final
  df_final = pd.DataFrame({
      'Data': df['Data da venda'],
      'Número da Venda': "'" + df['N.º de venda'].astype(str),
      'Item (nome)': df['Título do anúncio'],
      'MarketPlace': 'Mercado Livre',
      'Status': df['Status'],
  })

  return df_final
#end def

################
    # VERIFICAÇÃO E REMOÇÃO DAS LINHAS JÁ EXISTENTES
################

#! Captura, de acordo com parametro, o dataframe desejado (enviados, cancelados, reembolso)
def captura_df_desejado(tipo, sheet):
  if str(tipo) == "Enviados":
    wks         = sheet.worksheet_by_title(title="ML - Enviados")
    sheet_df    = wks.get_as_df(has_header=True, start="A1", end="K1000")

    return sheet_df
  
  elif str(tipo) == "Cancelados":
    wks         = sheet.worksheet_by_title(title="ML - Cancelados")
    sheet_df    = wks.get_as_df(has_header=True, start="A1", end="E1000")
    return sheet_df

  elif str(tipo) == "Reembolso":
    wks         = sheet.worksheet_by_title(title="ML - Devolução / Reembolso")
    sheet_df    = wks.get_as_df(has_header=True, start="A1", end="E1000")
    return sheet_df

#! Função que checa se os dados da planilha do ML existem na planilha de Enviados, Cancelados ou Reembolso, e exlcui os que já existem, mantendo apenas os novos a serem colados
def check_duplicidade(df_completo, df_existente):
  # Converter coluna 'Número da Venda' para string
  df_completo['Número da Venda'] = df_completo['Número da Venda'].astype(str)
  df_existente['Número da Venda'] = df_existente['Número da Venda'].astype(str)
  
  # Remover espaços em branco extras
  df_completo['Número da Venda'] = df_completo['Número da Venda'].str.strip()
  df_existente['Número da Venda'] = df_existente['Número da Venda'].str.strip()
  
  # Remover "'" inicial da coluna "Número da Venda"
  df_completo['Número da Venda'] = df_completo['Número da Venda'].str.lstrip("'")

  # Verificar os números de venda que já existem no dataframe existente
  numeros_venda_existente = set(df_existente['Número da Venda'])
  
  # Mantém apenas as linhas do dataframe completo que não estão no dataframe existente
  df_novos = df_completo[~df_completo['Número da Venda'].isin(numeros_venda_existente)]

  # Adiciona "'" antes de cada número de venda no dataframe novos
  df_novos['Número da Venda'] = df_novos['Número da Venda'].apply(lambda x: "'" + str(x))
  
  return df_novos