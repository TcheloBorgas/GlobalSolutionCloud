import requests
import logging
import pandas as pd

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