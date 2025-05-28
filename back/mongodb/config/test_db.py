from mongodb.config.connection_db import get_database

def test_database():
    db = get_database()
    if db is not None: 
        try:

            # db.Weapons.delete_many({})
            # print("Tous les documents de la collection 'Weapons' ont été supprimés.")
            collections = db.list_collection_names()
            print(f"Collections disponibles : {collections}")
            
            if "Weapons" in collections:
                weapons = list(db.Weapons.find())
                print(f"Nombre de documents dans 'Weapons' : {len(weapons)}")
                for i, w in enumerate(weapons, start=1):
                    weapon_info = w.get("weapon", {})
                    name = weapon_info.get("name", "Nom inconnu")
                    brand = weapon_info.get("brand", "Marque inconnue")
                    model = weapon_info.get("model", "Modèle inconnu")
                    image_path = weapon_info.get("image_path", "Pas d'image")
                    print(f"  {i}. {name} - {brand} - {model} | Image: {image_path}")
            else:
                print("Collection 'Weapons' non trouvée.")

            if "Users" in collections:
                users = list(db.Users.find())
                print(f"Nombre de documents dans 'Users' : {len(users)}")
                for i, u in enumerate(users, start=1):
                    pseudo = u.get("pseudo", "Pseudo inconnu")
                    password = u.get("password", "Mot de passe manquant")
                    print(f"  {i}. Pseudo : {pseudo} | Password : {password}")
            else:
                print("'Users' collection non trouvée.")
                
        except Exception as e:
            print(f"Erreur lors du test de la base de données : {e}")
    else:
        print("Connexion à la base de données échouée.")


if __name__ == "__main__":
    test_database()
