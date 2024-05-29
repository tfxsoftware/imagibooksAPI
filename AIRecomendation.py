from flask import Blueprint, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import pandas as pd

DATASET_PATH = 'data.csv'

df = pd.read_csv(DATASET_PATH)

# Substituir os valores nulos por string vazia
df['title'] = df['title'].fillna('')

# Converter o título do livro para vetores de características
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(df['title'])

# Obter a similaridade entre os livros usando similaridade de cosseno
similarity = cosine_similarity(feature_vectors, feature_vectors)

def recommendBooks(titulo_livro):
    try:
        # Encontrar o livro mais próximo ao título fornecido
        close_matches = difflib.get_close_matches(titulo_livro, df['title'].tolist())
        if not close_matches:
            raise ValueError(f"No close matches found for the book title '{titulo_livro}'")
        
        livro_mais_proximo = close_matches[0]
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

        return recomendacoes
    except IndexError as e:
        print(f"IndexError: {e}")
        return []
    except Exception as e:
        print(f"Error in recommendBooks: {e}")
        raise

