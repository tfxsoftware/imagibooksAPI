import ServiceImpl as services
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import json
from AIRecomendation import rotas_blueprint
from AIRecomendation import rotas_blueprint
from FirebaseConfig import get_firebase_app

firebase_app = get_firebase_app()

app = Flask(__name__)

# Inicializar o SDK do Firebase
db = firestore.client()

# Registrar o Blueprint das rotas relacionadas à IA
app.register_blueprint(rotas_blueprint)

@app.route('/ai/recommend', methods=['POST'])
def recommend():
    data = request.json
    print(data)
    return jsonify(services.recommendAndImage(data))

@app.route('/user/new', methods=['POST'])
def newUser():
    data = request.json
    json_data = json.dumps(data)
    return services.newUser(db, json_data)


@app.route('/user/<string:userId>', methods=['GET'])
def getUserById(userId):
    return services.getUserById(db, userId)
    
if __name__ == '__main__':
    app.run(debug=True)