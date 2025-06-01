from mongodb.config.connection_db import get_database

def test_database():
    db = get_database()
    if db is not None: 
        try:
            # Script de reset de Weapons et Stock
            # db.Weapons.delete_many({})
            # db.Stock.delete_many({})
            # print("Tous les documents de la collection 'Weapons' et 'Stock' ont été supprimés.")

            
            collections = db.list_collection_names()
            print(f"Collections disponibles : {collections}")
            
            if "Weapons" in collections:
                weapons = list(db.Weapons.find())
                print(f"Nombre de documents dans 'Weapons' : {len(weapons)}")
                for i, w in enumerate(weapons, start=1):
                    weapon_info = w.get("weapon", {})
                    name = weapon_info.get("name", "Nom inconnu")

                    print(f"  {i}. {name}")
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

            if "Stock" in collections:
                stocks = list(db.Stock.find())
                print(f"Nombre de documents dans 'Stock' : {len(stocks)}")
                for i, s in enumerate(stocks, start=1):
                    print(f"  {i}. Arme : {s.get('name')}")
                    print(f"     - Magasin : {s['store']['name']} ({s['store']['address']})")
                    print(f"     - En ligne : {s['online']['name']} ({s['online']['website']})")
            else:
                print("Collection 'Stock' non trouvée.")
                
        except Exception as e:
            print(f"Erreur lors du test de la base de données : {e}")
    else:
        print("Connexion à la base de données échouée.")


if __name__ == "__main__":
    test_database()
