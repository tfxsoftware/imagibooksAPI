import ServiceImpl as services
from flask import Flask, jsonify, request
from firebase_admin import firestore
import json
from FirebaseConfig import get_firebase_app

firebase_app = get_firebase_app()

app = Flask(__name__)

# Inicializar o SDK do Firebase
db = firestore.client()

@app.route('/ai/recommend', methods=['POST'])
def recommend():
    data = request.json
    userId = data["userId"]
    livro = data["livro"]
    return (services.recommendBook(userId, livro, db))

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