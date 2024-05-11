from flask import Blueprint, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import pandas as pd

# Definir o Blueprint Flask para as rotas
rotas_blueprint = Blueprint('rotas', __name__)

# Carregar o conjunto de dados
df = pd.read_csv('C:/Users/maria/OneDrive/Área de Trabalho/Faculdade/IA/BookRecomendationSystem/BookRecomendationSystem/datasets/data.csv')

# Substituir os valores nulos por string vazia
df['title'] = df['title'].fillna('')

# Converter o título do livro para vetores de características
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(df['title'])

# Obter a similaridade entre os livros usando similaridade de cosseno
similarity = cosine_similarity(feature_vectors, feature_vectors)

# Rota para lidar com a solicitação do frontend
@rotas_blueprint.route('/recomendar_livros', methods=['POST']) 
def recomendar_livros():
   
    titulo_livro = request.json['titulo_livro']
    livro_mais_proximo = difflib.get_close_matches(titulo_livro, df['title'].tolist())[0]
    index_livro = df[df['title'] == livro_mais_proximo].index[0]

   
    similarity_score = list(enumerate(similarity[index_livro]))
    sorted_similar_books = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:5]

    recomendacoes = []
    for book in sorted_similar_books:
        index = book[0]
        title_from_index = df.iloc[index]['title']
        recomendacoes.append(title_from_index)

    # Retornar as recomendações para o frontend
    return jsonify({'recomendacoes': recomendacoes})
