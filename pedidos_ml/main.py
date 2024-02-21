from flask import Flask, request, render_template
from datetime import datetime, timezone, timedelta
import requests
from time import sleep
from configs import *
from utils import *
import locale
from auth import *

app = Flask(__name__)
@app.route("/")
def pedidos_ml():
    try:
        
        #? Configurações de planilha e horários

        #* Definir localização para português
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        #* ID da planilha do BD
        spreadsheet_id = '1yAbwVoG3H1F70UTVSqMVLfmAjWEL0f7viqfqZfZAsys'

        #? Autenticando no Google Sheets
        sheet_client                  = authenticate_gsheets(service_account_json=service_account_json, sheet_scopes=sheets_scopes)

        #? Configurações das abas da planilha
        #* Pegando as configurações de taxonomia da planilha da mídia correspondente
        sheet                         = sheet_client.open_by_key(spreadsheet_id)    
        #* Capturando aba Planilha Vendas Mercado Livre - COLE AQUI
        wks_ml_vendas                 = sheet.worksheet_by_title(title="Planilha Vendas Mercado Livre - COLE AQUI")
        #* Capturando aba Planilha ML - Enviados
        wks_ml_enviados               = sheet.worksheet_by_title(title="ML - Enviados")
        #* Capturando aba Planilha ML - Cancelados
        wks_ml_cancelados             = sheet.worksheet_by_title(title="ML - Cancelados")
        #* Capturando aba Planilha ML - Cancelados
        wks_ml_reembolso              = sheet.worksheet_by_title(title="ML - Devolução / Reembolso")
        #* Gera um dataframe com a planilha de vendas do ML
        sheet_df                      = wks_ml_vendas.get_as_df(has_header=True, start="A6", end="AK1000")

        print("Rodou tudo até a linha 39")

        #? Executando funções para capturar as regras de negócio
        #* Captura a lista de colunas desejadas
        colunas_desejadas = colunas_desejadas_ml()
        #* Captura a lista de status cancelados para remover
        status_a_remover = status_cancelados_ml()
        #* Captura a lista de status de reembolso e devolução
        status_devolucao = status_devolucao_ml()

        print("Rodou tudo até a linha 47")

        #? Criando dataframe de cancelados
        cancelados_ml = df_cancelados_ml(df=sheet_df, colunas_desejadas=colunas_desejadas, status_cancelado=status_a_remover)
        df_cancelados_final = cria_df_cancelados_ml(cancelados_ml)

        #? Criando dataframe de reembolso / devolução
        reembolso_ml = df_reembolso_ml(df=sheet_df, colunas_desejadas=colunas_desejadas, status_devolucao_ml=status_devolucao)
        df_reembolso_final = cria_df_reembolso_ml(reembolso_ml)

        #? Criando dataframe de enviados
        enviados_ml = df_enviados_ml(df = sheet_df, colunas_desejadas=colunas_desejadas, status_cancelado=status_a_remover, status_devolucao=status_devolucao)
        df_final_enviados_ml = cria_df_enviados_ml(enviados_ml)

        #? Criando dataframes dos dados já existentes na planilha de enviados / cancelados e reembolso / devolução
        df_desejado_cancelados = captura_df_desejado(tipo="Cancelados", sheet=sheet)
        df_desejado_reembolso  = captura_df_desejado(tipo="Reembolso", sheet=sheet)
        df_desejado_enviados   = captura_df_desejado(tipo="Enviados", sheet=sheet)

        print("Rodou tudo até a linha 68")

        #? Checagem de duplicidade para enviados, cancelados e reembolso / devolução
        check_duplicidades_cancelados = check_duplicidade(df_cancelados_final, df_desejado_cancelados)
        check_duplicidades_reembolso  = check_duplicidade(df_reembolso_final, df_desejado_reembolso)
        check_duplicidades_enviados   = check_duplicidade(df_final_enviados_ml, df_desejado_enviados)

        print("Rodou tudo até a linha 75")

        #? Cola os novos valores que não constam na planilha de enviados, cancelados e reembolso/devolução
        paste_values(sheet_client, spreadsheet_id, wks_ml_cancelados, check_duplicidades_cancelados)
        print("Rodou tudo até a linha 80")
        colar_reembolso = paste_values(sheet_client, spreadsheet_id, wks_ml_reembolso, check_duplicidades_reembolso)
        colar_enviados = paste_values(sheet_client, spreadsheet_id, wks_ml_enviados, check_duplicidades_enviados)

        print("Rodou tudo até o final")

        return "Operação Concluída Com Sucesso!"

    except Exception as e:
        return "Operação Cancelada!"
        print('Houve algum erro ao processar os dados. Verifique a exception do Python:')
        print(f"Exception: {e}") 

if __name__ == '__main__':
    app.run(debug=True)