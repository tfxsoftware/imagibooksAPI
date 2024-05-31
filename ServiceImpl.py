import time
import firebase_admin
from firebase_admin import auth, firestore
from flask import jsonify, request
import json
import OpenAiModel
import AIRecomendation
import logging

def recommendBook(userId, book, db):
    books = AIRecomendation.recommendBooks(book)
    saveRecommendations(userId, books, book, db)
    text = OpenAiModel.generateExplanation(books, book)
    return {"livros": books, "texto": str(text)}

def saveRecommendations(userId, books, book, db):
    user_doc_ref = db.collection('users').document(userId)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
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
        user_doc_ref.set({
            'recomendacoes': [{
                'livros_recomendados': books,
                'livro_inserido': book,
                'timestamp': int(time.time())
            }]
        })

def newUser(db, data):
    try:
        user = data
        email = user.get('email')
        senha = user.get('senha')
        
        # Adiciona o usuário ao Firestore
        _, doc_ref = db.collection('users').add(user)
        doc_id = doc_ref.id
        
        # Adiciona o usuário ao Firebase Authentication
        auth.create_user(uid=doc_id, email=email, password=senha)
        
        logging.info(f"User created with ID: {doc_id}")
        return doc_id
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise e

def getUserById(db, doc_id):
    try:
        user_doc_ref = db.collection('users').document(doc_id)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()

            # Obter checklist do Firestore
            checklist_ref = db.collection('checklist').document(doc_id)
            checklist_doc = checklist_ref.get()
            if checklist_doc.exists:
                user_data['checklist'] = checklist_doc.to_dict()
            else:
                user_data['checklist'] = {}

            return jsonify(user_data), 200
        else:
            return jsonify({'message': 'Usuario nao encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def saveRecommendations(userId, books, book, db):
    user_doc_ref = db.collection('users').document(userId)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        if 'recomendacoes' not in user_data:
            user_data['recomendacoes'] = []
        user_data['recomendacoes'].append({
            'livros_recomendados': books,
            'livro_inserido': book,
            'timestamp': int(time.time())
        })
        user_doc_ref.update(user_data)
        logging.info(f"Recomendações salvas para o usuário {userId}: {user_data['recomendacoes']}")
    else:
        user_doc_ref.set({
            'recomendacoes': [{
                'livros_recomendados': books,
                'livro_inserido': book,
                'timestamp': int(time.time())
            }]
        })
        logging.info(f"Novo documento de usuário criado para {userId} com recomendações: {books}")

def saveChecklist(userId, checklist, db):
    checklist_ref = db.collection('checklist').document(userId)
    checklist_ref.set({
        'checklist': checklist,
        'timestamp': int(time.time())
    })
    logging.info(f"Checklist salvo para o usuário {userId}: {checklist}")

