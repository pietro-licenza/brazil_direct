import pygsheets
import pandas as pd
from google.cloud import bigquery
from google.cloud import bigquery_datatransfer
from google.oauth2 import service_account
from google.cloud import * 
import requests
from unidecode import unidecode as unidecode_func
import json


#*######################################################################
#*                          AUTENTICAÇÕES                              #
#*######################################################################

#! Autentica cliente no google sheets
def authenticate_gsheets(service_account_json, scopes):
    """Autentica com uma planilha google

    Args:
    service_account_json (json): json com os dados da conta de serviço gcp
    scopes (string): scopos usados na conexão com a API 
    """
    print("A função authenticate_gsheets foi chamada!")

    sheets_gcp_credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes = scopes)
    sheets_client = pygsheets.authorize(custom_credentials = sheets_gcp_credentials)

    return(sheets_client)
#end def

#*######################################################################
#*                        MERCADO LIVRE                                #
#*######################################################################

#######################################################################
#        INFORMAÇÕES DA PLANILHA E CONSULTA NO MERCADO LIVRE          #
#######################################################################

#! Função que recebe o range da planilha Buscador de Informações e transforma os código MLB em uma lista.
def get_active_products(wks_busca_info):

    print("Executando a função get_active_products")

    wks_busca_info = wks_busca_info

    #? Transformando o range do sheets em DataFrame
    df_active_products = wks_busca_info.get_as_df(has_header=True, start="B2", end="B31")

    #? Transforma o DataFrame em uma lista
    products_list = df_active_products['CÓDIGO MLB'].values.tolist()

    print("Função get_active_products executada com sucesso!")

    return(products_list)
#end def

#! Captura as informações dos produtos do Mercado Livre através do seu código e retorna informações necessárias
def get_ml_data(lista_anuncios):

  lista_dados_anuncios = []

  for anuncios in lista_anuncios:

    api_url = 'https://api.mercadolibre.com/items/%s' % anuncios
    api_url_description = 'https://api.mercadolibre.com/items/%s/description' % anuncios

    response = requests.get(api_url)  
    response_description = requests.get(api_url_description)

    lista_anuncio_individual = []
    if response.status_code == 200 and response_description.status_code == 200:
      product_data = response.json()

      #? Nome Produto
      description_data = response_description.json()
      produto = str(product_data.get('id'))
      lista_anuncio_individual.append(produto)

      #? Título
      titulo = str(product_data.get('title'))
      lista_anuncio_individual.append(titulo)

      #? Preço
      preco = str(product_data.get('price'))
      lista_anuncio_individual.append(preco)

      #? Marca
      brand_info = next((attr.get('value_name', 'N/A') for attr in product_data.get('attributes', []) if attr.get('id') == 'BRAND'), 'N/A')
      marca = next((attr.get('value_name', 'N/A') for attr in product_data.get('attributes', []) if attr.get('id') == 'BRAND'), 'N/A')
      lista_anuncio_individual.append(marca)

      #? Descrição
      descricao = str(description_data.get('plain_text'))
      lista_anuncio_individual.append(descricao)

      #? Categoria
      category_id = str(product_data.get('category_id', 'N/A'))
      lista_anuncio_individual.append(category_id)

      #? GTIN
      # Adicionar GTIN
      gtin_value = next((attr.get('value_name', 'N/A') for attr in product_data.get('attributes', []) if
                          attr.get('id') == 'GTIN'), 'N/A')
      lista_anuncio_individual.append(gtin_value)
    
      #? Imagens
      imagens_produto = product_data.get('pictures', [])[:4]
  

      for i, imagem in enumerate(imagens_produto, start=1):
          url = imagem.get('url', '')
          tamanho = imagem.get('size', '')

          # Verificação do tamanho
          if tamanho:
              largura, altura = map(int, tamanho.split('x'))
              if largura < 250 or altura < 250:
                  text_incorret_size = (f"Imagem fora do Padrão - Tamanho - {tamanho}")
                  lista_anuncio_individual.append(url)
                  lista_anuncio_individual.append(text_incorret_size)                  
              else:
                  text_correct_size = (f"Ok - {tamanho}")
                  lista_anuncio_individual.append(url)
                  lista_anuncio_individual.append(text_correct_size)                  

      #? Variações
      variations = product_data.get('variations', [])
      if variations:
          has_variations = 'Sim'
          variation_info = ""
          for variation in variations:
              attribute_combinations = variation.get('attribute_combinations', [])
              for attribute in attribute_combinations:
                  name = attribute.get('name', '')
                  value_name = attribute.get('value_name', '')
                  variation_info += f"'{name}':'{value_name}';"
          # Remove o último ponto-e-vírgula (;) se houver
          if variation_info.endswith(';'):
              variation_info = variation_info[:-1]
          lista_anuncio_individual.append(has_variations)
          lista_anuncio_individual.append(variation_info)

      else:
          lista_anuncio_individual.append('Não')
          lista_anuncio_individual.append('')

      lista_dados_anuncios.append(lista_anuncio_individual)

  return lista_dados_anuncios
#end def

#! Colar valores finais na aba output
def paste_values(wks_output, df):
    wks_output.update_values('C3', df)
#end def

#! Consulta a planilha de buscador de informações com as infos preenchidas
#! Faz o tratamento para separar altura, largura, comprimento e peso e cria um dataframe
def get_products_df(wks_busca_info):
    products_df                                                 = wks_busca_info.get_as_df(has_header=True, start="C2", end="T31")
    products_df['Título']                                       = products_df['Título'].apply(lambda x: unidecode_func(x))
    products_df['Descrição']                                    = products_df['Descrição'].apply(lambda x: unidecode_func(x))
    products_df[['Altura', 'Largura', 'Comprimento', 'Peso']]   = products_df['Dimensões'].str.lower().str.extract(r'(\d+)x(\d+)x(\d+) cm - ([\d,.]+) kg')
    products_df['Peso']                                         = products_df['Peso'].str.replace(',', '.', regex=True)
    products_df[['Altura', 'Largura', 'Comprimento', 'Peso']]   = products_df[['Altura', 'Largura', 'Comprimento', 'Peso']].apply(pd.to_numeric, errors='coerce')
    products_df['Variações']                                    = products_df['Variações'].str.replace("'", '')

    final_products_df = products_df

    return(final_products_df)
#end def

#*######################################################################
#*                              TINY                                   #
#*######################################################################


#######################################################################
#             GERAR JSON COM INFORMAÇÕES DOS PRODUTOS                 #
#######################################################################

#! Cria o formato json necessário para cadastrar o produto no Tiny ERP
def criar_json_produto(sequencia, row):
    # Verifica se o produto tem variação
    if row.get('Tem Variação', '').lower() == 'não':
        classe_produto = "S"  # Define classe_produto como "S" se o produto não tem variação
        var_dict = {}  # Define um dicionário vazio para as variações
    elif 'Variações' in row and row['Variações'] != 'Não':
        var_dict = {}
        variacoes = row['Variações'].split(';')
        for var in variacoes:
            key, value = var.split(':')
            var_dict[key.strip()] = value.strip()
        classe_produto = "V"  # Define classe_produto como "V" se houver variações
    else:
        var_dict = {}
        classe_produto = "S"  # Define classe_produto como "S" se não houver variações

    # Dados do produto
    produto = {
        "sequencia": sequencia,
        "nome": row['Título'],
        "codigo": row['CÓDIGO Produto'],
        "gtin": row['Gtin / EAN'],
        "unidade": "UN",
        "preco": float(row['Preço']),
        "peso_liquido": float(row['Peso']),  # Peso Líquido em CM
        "peso_bruto": float(row['Peso']),  # Peso Bruto em CM
        "altura_embalagem": float(row['Altura']),  # Altura em CM
        "largura_embalagem": float(row['Largura']),  # Largura em CM
        "comprimento_embalagem": float(row['Comprimento']),  # Comprimento em CM
        "origem": "0",
        "situacao": "A",
        "tipo": "P",
        "estoque_atual": 100,
        "estoque_minimo": 100,
        "dias_preparacao": 3,
        "categoria": row['Categoria ML'],
        "descricao_complementar": row['Descrição'],
        "marca": row['Marca'],
        "garantia": "3",
        "imagens_externas": [
            {"imagem_externa": {"url": row['Url Capa']}},
            {"imagem_externa": {"url": row['Url2']}},
            {"imagem_externa": {"url": row['Url3']}},
            {"imagem_externa": {"url": row['Url4']}},
        ],
        "classe_produto": classe_produto,  # Adiciona a classe do produto
    }

    # Adiciona as variações somente se houver variações
    if var_dict:
        produto["variacoes"] = [
            {
                "variacao": {
                    "codigo": f"{row['CÓDIGO Produto']}-1",
                    "preco": str(float(row['Preço'])),
                    "estoque_atual": 100,
                    "grade": var_dict  # Adiciona as variações ao produto
                }
            }
        ]

    return {"produto": produto}

#! Recebe o DataFrame final com as informações, aplica a regra lógica da função criar_json_produto para cada produto, aumentando sua sequência de acordo com a quantidade de produtos e retorna um json com todos os produtos que serão cadastrados
def criar_json_produtos(df_produtos_final):
    produtos = []

    for i, row in df_produtos_final.iterrows():
        produto_info = criar_json_produto(i + 1, row)
        produtos.append(produto_info)

    return {"produtos": produtos}
#end def 

#######################################################################
#                     BUSCA CATEGORIAS TINY                           #
#######################################################################

#! Captura todas as categorias e seus IDs para poder cruzar com mercado livre
def obter_arvore_categorias(token):
    url = "https://api.tiny.com.br/api2/produtos.categorias.arvore.php"
    parametros = {"token": token}
    resposta = requests.get(url, params=parametros)
    data = resposta.json()

    if 'retorno' in data:
        categorias = []

        def processar_categoria(categoria):
            categorias.append((categoria['id'], categoria['descricao']))
            if 'nodes' in categoria:
                for subcategoria in categoria['nodes']:
                    processar_categoria(subcategoria)

        for categoria in data['retorno']:
            processar_categoria(categoria)

        return categorias
    else:
        print("Erro desconhecido ao obter categorias.")

#######################################################################
#             CONEXÃO / CRIAÇÃO DO PRODUTOS NO TINY                   #
#######################################################################

def connect_and_create_tiny(produto_info):
    url = 'https://api.tiny.com.br/api2/produto.incluir.php'
    api_key = 'c2eaa98ba9636cc53ae517020b0f0394b397cbbb'

    # Dados do produto
    produto_info = produto_info

    #! Função 1 - Conexão com a API para gerar a variável Data

    #* Parte 1 - Conexão com a API através do token
    # Construa os dados para a solicitação POST
    data = {
        'token': api_key,
        'formato': 'JSON',
        'produto': json.dumps(produto_info),
    }

    # Faça a solicitação POST
    response = requests.post(url, data=data)


    #* Parte 2 - Verifica status da conexão e cria o produto
    # Manipule a resposta
    if response.status_code == 200:
        resultado = response.json()
        
        if resultado['retorno']['status_processamento'] == 3 and resultado['retorno']['status'] == "OK":
            registros = resultado['retorno']['registros']
            
            if registros:
                print("Produto criado com sucesso!")
                
                for registro in registros:
                    print(f"ID do produto criado: {registro['registro']['id']}")
            else:
                print("Nenhum registro retornado. Possível falha na criação do produto.")
                print(resultado)
        else:
            print(f"Erro na solicitação. Código de erro: {resultado['retorno']['status_processamento']}")
            print(resultado['retorno']['registros'])
    else:
        print(f"Erro na solicitação. Código de status: {response.status_code}")
        print(response.text)
#end def

#*######################################################################
#*                    TRATAMENTO DE DADOS                              #
#*######################################################################

def get_df_categories():
    file = "Categorias ML-Tiny.xlsx"
    df = pd.read_excel(file)
    return(df)
#end def

#! Função para aplicar as regras e mapear as categorias
def mapeamento_categoria(products_df, category_mapping_df):
    # Merge dos dataframes com base na coluna "Categoria ML"
    merged_df = pd.merge(products_df, category_mapping_df, on='Categoria ML', how='left')
    
    # Renomear a coluna resultante
    merged_df = merged_df.rename(columns={'ID Categoria Tiny': 'Categoria'})
    merged_df['Categoria ML'] = merged_df['Categoria']
    merged_df['Categoria ML'] = merged_df['Categoria ML'].fillna(0)
    
    return merged_df
#end def