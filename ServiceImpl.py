import time
import firebase_admin
from firebase_admin import auth, firestore
from flask import jsonify
import json
import OpenAiModel
import AIRecomendation

def recommendBook(userId, book, db):
    books = AIRecomendation.recommendBooks(book)
    saveRecommendations(userId, books, book, db)
    text = OpenAiModel.generateExplanation(books, book)
    # Retornar um dicionário Python simples, não um objeto jsonify
    return {"livros": books, "texto": str(text)}


def newUser(db, data):
    try:
        user = json.loads(data)
        _, doc_ref = db.collection('users').add(user)
        doc_id = doc_ref.id

        # Criação do usuário no Firebase Auth
        auth.create_user(uid=doc_id, email=user.get('email'), password=user.get('senha'))
        
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
    
def saveRecommendations(userId, books, book, db):
    user_doc_ref = db.collection('users').document(userId)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
    # Atualizar o documento do usuário adicionando uma nova entrada ao array de recomendações
        user_data = user_doc.to_dict()
        if 'recomendacoes' not in user_data:
            user_data['recomendacoes'] = []
        user_data['recomendacoes'].append({
            'livros_recomendados': books,
            'livro_inserido': book,
            'timestamp': int(time.time())
        })
        user_doc_ref.update(user_data)
    else:
        # Criar um novo documento do usuário
        user_doc_ref.set({
            'recomendacoes': [{
                'livros_recomendados': books,
                'livro_inserido': book,
                'timestamp': int(time.time())
            }]
        })
    