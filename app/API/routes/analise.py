from flask import Blueprint, jsonify
from API.data.data import dados

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analise', methods=['GET'])
def get_analise():
    medias = {
        'Temperatura média': sum(dados['Temperatura da Água (°C)']) / len(dados['Temperatura da Água (°C)']),
        'Salinidade média': sum(dados['Salinidade (ppt)']) / len(dados['Salinidade (ppt)']),
        'Profundidade média': sum(dados['Profundidade (m)']) / len(dados['Profundidade (m)']),
        'pH médio': sum(dados['pH']) / len(dados['pH']),
        'Contagem de Presença de Espécie Marinha': sum(dados['Presença de Espécie Marinha'])
    }
    return jsonify(medias)
