from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Charge les variables d'environnement depuis .env
load_dotenv(override=True)

# Récupère les variables d’environnement
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "cloudsoft_db")

def get_database():
    """
    Connecte à MongoDB et retourne l'objet de base de données.
    Utilise les variables d'environnement MONGO_URL et DB_NAME.
    """
    try:
        print(f"Tentative de connexion à MongoDB à l'URL : {MONGO_URL}")
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        
        # Force une tentative de connexion
        client.admin.command('ping')
        print("Connexion à MongoDB réussie.")
        
        db = client[DB_NAME]
        return db

    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB avec {MONGO_URL} : {e}")

        # Fallback vers localhost si le nom d'hôte 'mongo' échoue
        if "mongo" in MONGO_URL:
            try:
                print("Nouvelle tentative avec localhost:27017...")
                fallback_url = "mongodb://localhost:27017"
                client = MongoClient(fallback_url, serverSelectionTimeoutMS=5000)
                client.admin.command('ping')
                print("Connexion à MongoDB réussie en local.")
                return client[DB_NAME]
            except Exception as e2:
                print(f"Échec de la connexion locale également : {e2}")
        
        return None
