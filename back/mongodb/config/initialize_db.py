from mongodb.config.connection_db import get_database
import os
import json

def initialize_collections():
    """
    Initialise les collections 'Users' et 'Weapons' 'Stock' si elles n'existent pas.
    """
    db = get_database()
    

    if db is not None:
        try:
            collections_to_create = ["Users", "Weapons", "Stock"]
            existing_collections = db.list_collection_names()

            if "Users" not in existing_collections:
                db.Users.create_index([("pseudo", 1)], unique=True)
                print("Index unique créé sur le champ 'pseudo' de la collection 'Users'.")
            else:
                print("La collection 'Users' existe déjà. Index non recréé.")

            for collection in collections_to_create:
                if collection not in existing_collections:
                    db.create_collection(collection)
                    print(f"Collection '{collection}' créée.")
                else:
                    print(f"Collection '{collection}' existe déjà.")

            # Insertion dans Stock si vide
            if "Stock" in collections_to_create:
                stock_count = db.Stock.count_documents({})
                if stock_count == 0:
                    stock_path = os.path.join("mongodb", "collections", "Stock.json")
                    with open(stock_path, "r", encoding="utf-8") as f:
                        stock_data = json.load(f)

                    # Ici plus besoin de reconstruire les documents, ils sont déjà prêts
                    result = db.Stock.insert_many(stock_data)
                    print(f"{len(result.inserted_ids)} documents insérés dans 'Stock'.")
                else:
                    print(f"'Stock' contient déjà {stock_count} documents. Aucune insertion faite.")


        except Exception as e:
            print(f"Erreur lors de l'initialisation des collections : {e}")



if __name__ == "__main__":
    initialize_collections()
