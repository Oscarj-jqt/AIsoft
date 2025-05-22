CloudSoft

https://trello.com/b/MGjzE0wC/cloudsoft

Une application qui permet d’analyser une image capturée (ex. GoPro pendant une partie d’Airsoft), d’identifier l’arme et ses accessoires grâce à une IA, puis de rechercher et comparer les prix de cette arme sur le web.

## Infrastructure du projet

### Dockerisation

- Le projet est conteneurisé avec Docker :

- Un service backend Flask

- Une base de données MongoDB

- Lancement de l'infrastructure depuis le dossier back/ :

```bash
docker-compose up --build
```

## CI/CD avec GitHub Actions et AZURE


### Intégration Continue CI
- Le projet CloudSoft utilise GitHub Actions pour automatiser le code soure et les dépendances à chaque push ou pull request sur la branche main.

### Déploiement Continu CD

- Le projet est conçu pour être déployé automatiquement sur Microsoft Azure via GitHub Actions

Lien du déploiement 
https://cloudsoft-e2h0egbma8a9agc6.francecentral-01.azurewebsites.net