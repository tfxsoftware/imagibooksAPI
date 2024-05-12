from firebase_admin import credentials, initialize_app

# Caminho para o arquivo de credenciais do Firebase
CREDENTIALS_PATH = 'C:/Users/maria/OneDrive/Área de Trabalho/Faculdade/BACKPI5/imagibooks-firebase-adminsdk-6tgdr-6efb6d72dd.json'

# Variável global para armazenar o aplicativo Firebase
firebase_app = None

def get_firebase_app():
    global firebase_app
    if firebase_app is None:
        # Caminho para o arquivo de credenciais do Firebase
        CREDENTIALS_PATH = 'C:/Users/maria/OneDrive/Área de Trabalho/Faculdade/BACKPI5/imagibooks-firebase-adminsdk-6tgdr-6efb6d72dd.json'
        
        # Inicializar o aplicativo Firebase
        cred = credentials.Certificate(CREDENTIALS_PATH)
        firebase_app = initialize_app(cred)
    return firebase_app