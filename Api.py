import ServiceImpl as services
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import json

app = Flask(__name__)
cred = credentials.Certificate("C:\\imagibooks-firebase-adminsdk-6tgdr-20860514e5.json")
firebase_app = initialize_app(cred)
db = firestore.client()

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