from flask import Flask, request
import requests
import streamlit as st
import base64

dados = {
    "Temperatura da Água (°C)": [16.46, 18.50, 24.51, 17.20, 23.39, 10.78, 25.66, 12.48, 27.90, 14.11, 19.30, 21.12, 26.49, 13.55, 22.88, 11.67, 20.03, 29.55, 15.67, 28.23],
    "Salinidade (ppt)": [35.77, 33.55, 36.41, 37.62, 38.73, 34.66, 39.54, 31.22, 33.91, 34.78, 32.15, 36.50, 38.88, 32.73, 34.96, 35.12, 37.11, 31.93, 33.64, 39.10],
    "Profundidade (m)": [75.64, 59.24, 11.89, 22.95, 44.22, 91.77, 48.19, 10.53, 19.61, 87.31, 73.23, 53.45, 26.14, 45.72, 34.88, 60.41, 18.56, 14.22, 74.81, 32.35],
    "pH": [8.09, 7.96, 8.34, 7.69, 7.88, 8.10, 8.23, 7.75, 8.45, 8.00, 7.94, 8.11, 8.29, 7.76, 8.12, 7.81, 8.04, 8.40, 7.89, 8.37],
    "Presença de Espécie Marinha": [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
}


quantidade_presenca_marinha = dados["Presença de Espécie Marinha"].count(1)




# URL da API Flask (altere conforme necessário)
API_URL = "http://localhost:5000"

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Converter a imagem para base64
encoded_image = img_to_base64(r'..\template\fundo.jpg')  # Ajuste o caminho conforme necessário

def add_bg_from_local():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

# Chama a função para adicionar a imagem de fundo
add_bg_from_local()

st.title("Análise de Dados Marinhos")

if st.button("Realizar Análise Completa"):
    response = requests.get(f"{API_URL}/analise")
    analise = response.json()
    st.write("Médias Calculadas:", analise["Médias"])
    st.write(f'Número de Detecções da Espécie: {quantidade_presenca_marinha}')
    st.write("Detalhes dos Registros com Presença da Espécie:")
    st.write(f'Detalhes Presença: ')
    for registro in analise["Detalhes Presença"]:
        st.write(registro)




import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
import deepl

# Configurar a chave de autenticação da API DeepL
auth_key = "023f48c8-7767-4df8-b643-d77f0cf35c19:fx"  # Substitua pela sua chave
translator = deepl.Translator(auth_key)

st.title("Monitoramento de Poluição Marinha")

# Função para obter dados da OpenAQ API
def get_openaq_data(country):
    url = f"http://localhost:5000/api/openaq?country={country}"  # URL da API Flask
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve um erro na resposta
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Função para obter a lista de países disponíveis na OpenAQ API
def get_countries():
    url = "http://localhost:5000/api/countries"  # URL da API Flask
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve um erro na resposta
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Função para traduzir texto usando DeepL
def translate_text(text, target_lang="PT-BR"):
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text

# Função para formatar dados da OpenAQ
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
            if not df.empty:
                locations = df['Location'].unique()
                location = st.selectbox("Selecione uma localização", locations)

                location_data = df[df['Location'] == location]

                if not location_data.empty:
                    st.dataframe(location_data[['Location', 'Parameter', 'Value', 'Unit', 'Description']])

                    # Exibir mapa com a localização selecionada
                    map_center = [location_data['Latitude'].mean(), location_data['Longitude'].mean()]
                    m = folium.Map(location=map_center, zoom_start=10)

                    for _, row in location_data.iterrows():
                        folium.Marker(
                            location=[row['Latitude'], row['Longitude']],
                            popup=row['Description']
                        ).add_to(m)

                    folium_static(m)
                else:
                    st.write("Nenhum dado disponível para a localização selecionada")
            else:
                st.write("Nenhum dado disponível")
