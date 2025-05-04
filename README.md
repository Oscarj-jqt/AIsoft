CloudSoft

https://trello.com/b/MGjzE0wC/cloudsoft

Une application qui permet d’analyser une image capturée (ex. GoPro pendant une partie d’Airsoft), d’identifier l’arme et ses accessoires grâce à une IA, puis de rechercher et comparer les prix de cette arme sur le web.

## Infrastructure du projet

### Dockerisation
- Le projet est conteneurisé avec Docker :

- Un service backend Flask

- Une base de données MongoDB

- Le backend se connecte à Mongo via :

```bash
MONGO_URL=mongodb://mongo:27017
DB_NAME=cloudsoft_db
```

- Lancement de l'infrastructure depuis le dossier back/ :

```bash
docker-compose up --build
```

## CI/CD avec GitHub Actions et AZURE


### Intégration Continue CI
- Le projet CloudSoft utilise GitHub Actions pour automatiser les étapes suivantes à chaque push ou pull request sur la branche main :

- Vérification du code source.

- Installation des dépendances Python.

- Lancement d’un conteneur Mongo pour les tests.

- Lancement de l’application backend.

### Déploiement Continu CD (en cours)

- Le projet est conçu pour être déployé automatiquement sur Microsoft Azure via GitHub Actions

- L'image Docker du backend sera déployée automatiquement à chaque modification sur main

- Le déploiement est sécurisé à l'aide de GitHub Secrets