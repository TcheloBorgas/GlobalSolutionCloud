from flask import Flask, jsonify, request
import requests
import logging

app = Flask(__name__)

# Configuração do logger
logging.basicConfig(level=logging.INFO)

# Função para obter dados da OpenAQ API
def get_openaq_data(country="US"):
    url = f"https://api.openaq.org/v1/measurements?country={country}&limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve um erro na resposta
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter dados da OpenAQ: {e}")
        return {"error": str(e)}

# Função para obter a lista de países disponíveis na OpenAQ API
def get_countries():
    url = "https://api.openaq.org/v1/countries"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve um erro na resposta
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter lista de países da OpenAQ: {e}")
        return {"error": str(e)}

@app.route('/api/openaq', methods=['GET'])
def openaq_data():
    country = request.args.get('country', 'US')
    logging.info(f"Obtendo dados para o país: {country}")
    data = get_openaq_data(country)
    return jsonify(data)

@app.route('/api/countries', methods=['GET'])
def countries():
    logging.info("Obtendo lista de países")
    data = get_countries()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
