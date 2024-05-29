import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import ServiceImpl as services
import json 
from firebase_admin import firestore
from FirebaseConfig import get_firebase_app

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

firebase_app = get_firebase_app()
db = firestore.client()

@app.route('/ai/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        app.logger.info(f'Received data: {data}')
        userId = data["userId"]
        titulo_livro = data["titulo_livro"]
        recommendations = services.recommendBook(userId, titulo_livro, db)
        return jsonify(recommendations)
    except Exception as e:
        app.logger.error(f'Error during recommendation: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/user/new', methods=['POST'])
def newUser():
    try:
        data = request.json
        app.logger.info(f'Received data: {data}')  
        json_data = json.dumps(data)
        user_id = services.newUser(db, json_data)
        return jsonify({'userId': user_id}), 200
    except Exception as e:
        app.logger.error(f'Error creating new user: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/user/<string:userId>', methods=['GET'])
def getUserById(userId):
    try:
        return services.getUserById(db, userId)
    except Exception as e:
        app.logger.error(f'Error fetching user: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
