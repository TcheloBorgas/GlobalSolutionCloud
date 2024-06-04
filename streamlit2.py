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
