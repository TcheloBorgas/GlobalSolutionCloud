import logging
from flask import Flask, Blueprint, jsonify, request
from API.services.openaq_service import get_openaq_data, get_countries

app = Flask(__name__)
api_bp = Blueprint('api', __name__)

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

# Registrar o blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
