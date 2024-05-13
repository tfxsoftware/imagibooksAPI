from openai import OpenAI

client = OpenAI()

def generateExplanation(books, book):
    
    role = ""
    prompt = f"me diga oque os {books[0]}, {books[1]}, {books[2]}, {books[3]} e {books[4]} tem em comum e porque eu iria gostar de ler eles"


    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[ 
        {"role": "user", "content": prompt}
    ]
    )
    return {completion.choices[0].message.content}

