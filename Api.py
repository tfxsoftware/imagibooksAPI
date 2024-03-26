
import ServiceImpl as services
import Models.QuizAwnser
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import json

app = Flask(__name__)
cred = credentials.Certificate("C:\\imagibooks-firebase-adminsdk-6tgdr-99184fb4fc.json")
firebase_app = initialize_app(cred)
db = firestore.client()

@app.route('/ai/recommend', methods=['GET'])
def recommend():
    return jsonify({"message": str(services.recommendAndImage(1))})

@app.route('/user/new', methods=['POST'])
def newUser():
    
    data = request.json
    json_data = json.dumps(data)
    return services.newUser(db, json_data)


if __name__ == '__main__':
    app.run(debug=True)