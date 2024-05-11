from flask import Flask
from AI import rotas_blueprint

app = Flask(__name__)

# Registrar o Blueprint das rotas
app.register_blueprint(rotas_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
