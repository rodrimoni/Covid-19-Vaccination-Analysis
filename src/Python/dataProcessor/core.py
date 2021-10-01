import pandas as pd
from geobr import read_municipality
import os

basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
dataPath = os.path.join(basePath, 'data')

# Ler dados de cidades do Rio Grande do Sul

def getCityVaccineData():
    rs = pd.read_csv(os.path.join(dataPath, 'municipios_rs.csv'))
    rs['code_muni'] = rs['code_muni'].astype(str)
    rs = rs.drop(columns = ['code_state', 'code_region', 'abbrev_state', 'name_state', 'name_region', 'name_muni', 'Unnamed: 0'])
    rs['code_muni'] = rs['code_muni'].str.slice(0, 6)
    print(rs.iloc[0])

    # Processar os dados de vacinação do RS
    dados_vac = pd.read_csv(os.path.join(dataPath, 'imune/aplicacao_vacina_municipios.csv'))
    dados_vac['codigo_municipio'] = dados_vac['codigo_municipio'].astype(str)

    # Join dos bancos de vacinação
    print(dados_vac.iloc[0])
    dados_vac = pd.merge(dados_vac, rs, left_on='codigo_municipio', right_on='code_muni')
    dados_vac = dados_vac.drop(columns = 'code_muni')
    print(dados_vac.iloc[0])

    return dados_vac

