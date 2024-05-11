import firebase_admin
from firebase_admin import auth, firestore
from flask import jsonify
import json
import OpenChatGPTModel as ai

def recommendAndImage(quiz):
    return ai.generateRecommendation(quiz)

def newUser(db, data):
    user = json.loads(data)
    
   
    doc_ref = db.collection('users').add(user)
    user_id = doc_ref.id
    
    
    try:
        auth.create_user(uid=user_id)
        return jsonify({'message': 'Usuario criado com sucesso'}), 200
    except Exception as e:
        
        return jsonify({'error': str(e)}), 500
    
def getUserById(db, doc_id):
    try:
        doc_ref = db.collection('users').document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict(), 200
        else:
            return jsonify({'message': 'Usuario nao encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    