from flask import Flask, jsonify, request
import requests
import logging


app = Flask(__name__)

# Dados
dados = {
    "Temperatura da Água (°C)": [16.46, 18.50, 24.51, 17.20, 23.39, 10.78, 25.66, 12.48, 27.90, 14.11, 19.30, 21.12, 26.49, 13.55, 22.88, 11.67, 20.03, 29.55, 15.67, 28.23],
    "Salinidade (ppt)": [35.77, 33.55, 36.41, 37.62, 38.73, 34.66, 39.54, 31.22, 33.91, 34.78, 32.15, 36.50, 38.88, 32.73, 34.96, 35.12, 37.11, 31.93, 33.64, 39.10],
    "Profundidade (m)": [75.64, 59.24, 11.89, 22.95, 44.22, 91.77, 48.19, 10.53, 19.61, 87.31, 73.23, 53.45, 26.14, 45.72, 34.88, 60.41, 18.56, 14.22, 74.81, 32.35],
    "pH": [8.09, 7.96, 8.34, 7.69, 7.88, 8.10, 8.23, 7.75, 8.45, 8.00, 7.94, 8.11, 8.29, 7.76, 8.12, 7.81, 8.04, 8.40, 7.89, 8.37],
    "Presença de Espécie Marinha": [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
}




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



# Endpoint para obter as médias e contagem de presença de espécie
@app.route('/analise', methods=['GET'])
def get_analise():
    medias = {
        'Temperatura média': sum(dados["Temperatura da Água (°C)"]) / len(dados["Temperatura da Água (°C)"]),
        'Salinidade média': sum(dados["Salinidade (ppt)"]) / len(dados["Salinidade (ppt)"]),
        'Profundidade média': sum(dados["Profundidade (m)"]) / len(dados["Profundidade (m)"]),
        'pH médio': sum(dados["pH"]) / len(dados["pH"])
    }
    presenca = sum(dados["Presença de Espécie Marinha"])
    especie_presenca = []
    for i, presenca in enumerate(dados["Presença de Espécie Marinha"]):
        if presenca == 1:
            registro = {
                "Temperatura": dados["Temperatura da Água (°C)"][i],
                "Salinidade": dados["Salinidade (ppt)"][i],
                "Profundidade": dados["Profundidade (m)"][i],
                "pH": dados["pH"][i],
                "Acima/Baixo da Média": {
                    "Temperatura": "acima" if dados["Temperatura da Água (°C)"][i] > medias['Temperatura média'] else "abaixo",
                    "Salinidade": "acima" if dados["Salinidade (ppt)"][i] > medias['Salinidade média'] else "abaixo",
                    "Profundidade": "acima" if dados["Profundidade (m)"][i] > medias['Profundidade média'] else "abaixo",
                    "pH": "acima" if dados["pH"][i] > medias['pH médio'] else "abaixo"
                }
            }
            especie_presenca.append(registro)
    return jsonify({"Médias": medias, "Presença": presenca, "Detalhes Presença": especie_presenca})

if __name__ == '__main__':
    app.run(debug=True)


