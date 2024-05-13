from flask import Blueprint, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import pandas as pd
from firebase_admin import firestore
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
from FirebaseConfig import get_firebase_app
import time

firebase_app = get_firebase_app()

# Caminho para o conjunto de dados
DATASET_PATH = 'D:\ImagiBooks\BookRecomendationSystem\datasets\data.csv'

# Inicializar o cliente Firestore
db = firestore.client()

# Definir o Blueprint Flask para as rotas
rotas_blueprint = Blueprint('rotas', __name__)

# Carregar o conjunto de dados
df = pd.read_csv(DATASET_PATH)

# Substituir os valores nulos por string vazia
df['title'] = df['title'].fillna('')

# Converter o título do livro para vetores de características
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(df['title'])

# Obter a similaridade entre os livros usando similaridade de cosseno
similarity = cosine_similarity(feature_vectors, feature_vectors)

# Rota para lidar com a solicitação do frontend de recomendação de livros
@rotas_blueprint.route('/recomendar_livros', methods=['POST']) 
def recomendar_livros():
    # Obter os dados da solicitação JSON, incluindo o título do livro e o userId
    data = request.json
    titulo_livro = data['titulo_livro']
    userId = data['userId']
    
    # Encontrar o livro mais próximo ao título fornecido
    livro_mais_proximo = difflib.get_close_matches(titulo_livro, df['title'].tolist())[0]
    index_livro = df[df['title'] == livro_mais_proximo].index[0]

    # Calcular a similaridade entre os livros e classificar os mais similares
    similarity_score = list(enumerate(similarity[index_livro]))
    sorted_similar_books = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:5]

    # Coletar os títulos dos livros recomendados
    recomendacoes = []
    for book in sorted_similar_books:
        index = book[0]
        title_from_index = df.iloc[index]['title']
        recomendacoes.append(title_from_index)

    # Obter a hora atual
    timestamp = int(time.time())

    # Verificar se o documento do usuário já existe
    user_doc_ref = db.collection('users').document(userId)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
    # Atualizar o documento do usuário adicionando uma nova entrada ao array de recomendações
        user_data = user_doc.to_dict()
        if 'recomendacoes' not in user_data:
            user_data['recomendacoes'] = []
        user_data['recomendacoes'].append({
            'livros_recomendados': recomendacoes,
            'livro_inserido': titulo_livro,
            'timestamp': timestamp
        })
        user_doc_ref.update(user_data)
    else:
        # Criar um novo documento do usuário
        user_doc_ref.set({
            'recomendacoes': [{
                'livros_recomendados': recomendacoes,
                'livro_inserido': titulo_livro,
                'timestamp': timestamp
            }]
        })

    # Retornar as recomendações para o frontend
    return jsonify({'recomendacoes': recomendacoes})