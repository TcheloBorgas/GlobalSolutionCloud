import requests
import logging

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
