from connection_db import get_database

def test_database():
    db = get_database()
    if db is not None: 
        try:
            collections = db.list_collection_names()
            print(f"Collections disponibles : {collections}")
            
            if "Weapons" in collections:
                weapons = list(db.Weapons.find())
                print(f"Nombre de documents dans 'Weapons' : {len(weapons)}")
            else:
                print("'Weapons' collection non trouvée.")
            
            if "Users" in collections:
                users = list(db.Users.find())
                print(f"Nombre de documents dans 'Users' : {len(users)}")
            else:
                print("'Users' collection non trouvée.")
                
        except Exception as e:
            print(f"Erreur lors du test de la base de données : {e}")
    else:
        print("Connexion à la base de données échouée.")

if __name__ == "__main__":
    test_database()
