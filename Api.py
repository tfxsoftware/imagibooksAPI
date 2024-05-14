from flask import Flask, jsonify, request
from flask_cors import CORS
import ServiceImpl as services
import json 
from firebase_admin import firestore
from FirebaseConfig import get_firebase_app

app = Flask(__name__)
CORS(app)  

firebase_app = get_firebase_app()
db = firestore.client()

@app.route('/ai/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        userId = data["userId"]
        titulo_livro = data["titulo_livro"]
        recommendations = services.recommendBook(userId, titulo_livro, db)
        return jsonify(recommendations)  
    except Exception as e:
        app.logger.error(f'Error during recommendation: {str(e)}')
        return jsonify({'error': str(e)}), 500


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
