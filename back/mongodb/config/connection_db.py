from pymongo import MongoClient
from dotenv import load_dotenv
import os

def reload_env():
    load_dotenv(override=True)  

reload_env()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

def get_database():
    """
    Connecte à MongoDB et retourne l'objet de base de données.
    """

    try:
        print("Tentative de connexion à MongoDB...")
        client = MongoClient(MONGO_URL)
        print("Client MongoDB créé avec succès.")

        db = client[DB_NAME]
        print(db)
        print(f"Connexion à la base de données '{DB_NAME}' réussie.")
        return db
    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB : {e}")
        return None


