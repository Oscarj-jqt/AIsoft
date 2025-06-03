AIsoft

https://trello.com/b/MGjzE0wC/cloudsoft

Une application qui permet d’analyser une image uploadée, d’identifier l’arme grâce à une IA intégrée, puis de rechercher les sources de cette arme pour la retrouver.

## Infrastructure du projet

  ### Dockerisation

    - Le projet est conteneurisé avec Docker :

    - Un service backend Flask

    - Une base de données MongoDB

    - Installation de l'infrastructure depuis le dossier back/ :
  
    ```bash
    docker-compose up --build
    ```

## CI/CD et Hébergement

  ### Intégration Continue CI
  
    - Le projet AIsoft utilise GitHub Actions pour automatiser le code soure et les dépendances à chaque push ou pull       request sur la branche main.

  ### Hébergement Cloud 

    - Le projet est conçu pour être déployé automatiquement sur Microsoft Azure via GitHub Actions

    - Le serveur Flask "cloudsoft" est hébergé sous via
      https://cloudsoft-e2h0egbma8a9agc6.francecentral-01.azurewebsites.net

    - Le frontend "aisoft" est hébergé sous via
      lien

  ### Déploiement Continu CD
  
  - Le code déployé sur Azure est mis à jour grâce au déploiement continu configuré avec GitHub Actions


## Serveur et Base de donnée
