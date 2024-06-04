from flask import Flask
from API.routes.analise import analysis_bp
from API.routes.api import api_bp

app = Flask(__name__)
app.register_blueprint(analysis_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)