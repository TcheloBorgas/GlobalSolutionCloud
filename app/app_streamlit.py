import streamlit as st
import sys
import os
import importlib.util
import requests
import logging
import deepl
import pandas as pd

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # Importar utils.utils.openaq usando importlib
# spec = importlib.util.spec_from_file_location("utils.utils.openaq", os.path.join(os.path.dirname(__file__), 'utils', 'utils', 'openaq.py'))
# openaq = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(openaq)

# get_countries = openaq.get_countries
# get_openaq_data = openaq.get_openaq_data
# format_openaq_data = openaq.format_openaq_data

from utils.utils.data import dados, quantidade_presenca_marinha, get_analise
from utils.utils.image import add_bg_from_local
from utils.utils.deep_translate import translate_text




add_bg_from_local()


def get_openaq_data(country="US"):
    url = f"https://api.openaq.org/v1/measurements?country={country}&limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve um erro na resposta
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter dados da OpenAQ: {e}")
        return {"error": str(e)}

def get_countries():
    url = "https://api.openaq.org/v1/countries"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve um erro na resposta
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter lista de países da OpenAQ: {e}")
        return {"error": str(e)}

def format_openaq_data(data):
    if "results" in data:
        formatted_data = [
            {
                "Latitude": item["coordinates"]["latitude"],
                "Longitude": item["coordinates"]["longitude"],
                "Location": item["location"],
                "Parameter": item["parameter"],
                "Value": item["value"],
                "Unit": item["unit"],
                "Description": translate_text(f"Measurement of {item['parameter']} at {item['location']}, {item.get('city', 'Unknown City')}, {item['country']} on {item['date']['local']}")
            }
            for item in data["results"]
        ]
        df = pd.DataFrame(formatted_data)
        df = df[['Latitude', 'Longitude', 'Location', 'Parameter', 'Value', 'Unit', 'Description']]  # Reordenar colunas
        return df
    else:
        return pd.DataFrame()

# Configurar a chave de autenticação da API DeepL
auth_key = "023f48c8-7767-4df8-b643-d77f0cf35c19:fx"  # Substitua pela sua chave
translator = deepl.Translator(auth_key)

def translate_text(text, target_lang="PT-BR"):
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text




st.title("Análise de Dados Marinhos")

if st.button("Realizar Análise Completa"):
    analise = get_analise()
    st.write("Médias Calculadas:", analise["Médias"])
    st.write(f'Número de Detecções da Espécie: {quantidade_presenca_marinha}')
    st.write("Detalhes dos Registros com Presença da Espécie:")
    st.write(f'Detalhes Presença: ')
    for registro in analise["Detalhes Presença"]:
        st.write(registro)

st.title("Monitoramento de Poluição Marinha")

# Obter lista de países
countries_data = get_countries()
if "error" in countries_data:
    st.error(countries_data["error"])
else:
    countries = [country['code'] for country in countries_data['results']]
    if countries:
        country = st.selectbox("Selecione um país", countries)

        # Obter dados da API para o país selecionado
        data = get_openaq_data(country)
        
        if "error" in data:
            st.error(data["error"])
        else:
            df = format_openaq_data(data)
            if not df.empty():
                locations = df['Location'].unique()
                if locations:
                    location = st.selectbox("Selecione uma localização", locations)
                    location_data = df[df['Location'] == location]
                    if not location_data.empty():
                        st.map(location_data[['Latitude', 'Longitude']])
                        st.write(location_data)
                    else:
                        st.write("Nenhum dado disponível para a localização selecionada")
                else:
                    st.write("Nenhum dado disponível")
            else:
                st.write("Nenhum dado disponível")
