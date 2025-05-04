from mongodb.config.connection_db import get_database

def initialize_collections():
    db = get_database()
    if db is not None:
        try:
            collections_to_create = ["Users", "Weapons"]

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

        except Exception as e:
            print(f"Erreur lors de l'initialisation des collections : {e}")


if __name__ == "__main__":
    initialize_collections()
