import firebase_admin
from firebase_admin import credentials, firestore
import AIModel as ai
from flask import jsonify
import json

def recommendAndImage(quiz):
    ai.generateRecommendation(quiz)
    return ai.generateRecommendation(quiz)

def newUser(db, data):
        user = json.loads(data)
        
        doc_ref = db.collection('users').add(user)
        return jsonify({'message': 'Data added to Firestore'}), 200

    