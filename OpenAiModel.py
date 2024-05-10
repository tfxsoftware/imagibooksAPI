from openai import OpenAI
client = OpenAI(api_key="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")

def generateRecommendation(quiz):
    tipo = quiz["tipo"]
    genero = quiz["genero"]
    books = quiz["livros"]

    role = f"Voce é um vendedor de livros, mas faz recomedações de livros que existem no mundo real, sua resposta deve começar com o nome do livro, seguido por um ponto e então a explicação do por que ele seria interessante pra mim"
    prompt = f"Me recomende um livro do gênero {genero} em um mundo de {tipo}, outros livors que eu li {books[0]}, {books[1]} e {books[2]}"


    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": role},
        {"role": "user", "content": prompt}
    ]
    )
    return {"livro": completion.choices[0].message.content.split(",")[0], "text": completion.choices[0].message.content}

