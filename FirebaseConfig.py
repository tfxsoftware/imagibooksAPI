from firebase_admin import credentials, initialize_app

# Caminho para o arquivo de credenciais do Firebase
CREDENTIALS_PATH = 'imagibooks-firebase-adminsdk-6tgdr-99184fb4fc.json'
firebase_app = None

def get_firebase_app():
    global firebase_app
    if firebase_app is None:
        cred = credentials.Certificate(CREDENTIALS_PATH)
        firebase_app = initialize_app(cred)
    return firebase_app

