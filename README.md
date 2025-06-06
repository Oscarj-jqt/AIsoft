AIsoft

https://trello.com/b/MGjzE0wC/cloudsoft

Une application qui permet d’analyser une image uploadée, d’identifier l’arme grâce à une IA intégrée, puis de rechercher les sources de cette arme pour la retrouver.

## Infrastructure du projet

  ### Dockerisation

    - Le projet est conteneurisé avec Docker :

    - Un service backend Flask

    - Une base de données MongoDB


## CI/CD et Hébergement

  ### Intégration Continue CI
  
    - Le projet AIsoft utilise GitHub Actions pour automatiser le code soure et les dépendances à chaque push ou pull       request sur la branche main.

  ### Hébergement Cloud 

    - Le projet est conçu pour être déployé automatiquement sur Microsoft Azure via GitHub Actions

    - Le serveur Flask "cloudsoft" est hébergé avec Azure
      https://cloudsoft-e2h0egbma8a9agc6.francecentral-01.azurewebsites.net

    - Le frontend "aisoft" est hébergé avec Azure
      lien

  ### Déploiement Continu CD
  
  - Le code déployé sur Azure est mis à jour grâce au déploiement continu configuré avec GitHub Actions


## Serveur et Base de donnée

  ### Backend

Le backend est développé avec Python Flask.

Il expose plusieurs routes API RESTful, dont les principales sont :

 - la création de compte et l'authentification sécurisée des utilisateurs

 - l’upload d’une image par un utilisateur authentifié.

 - analyze : déclenche l’analyse de l’image via l’IA intégrée afin d’identifier une arme.



  ### Base de Données MongoDB

  MongoDB est la base de donnée utilisée dans laquelle sont stockées :

    - les informations des utilisateurs

    - les informations sur les armes détectées


## Interface utilisateur

  ### Frontend

  Le frontend est développé avec React et Tailwind pour l'utilisation de composants graphiques en temps réel.


## Installation et configuration

 **Cloner le projet** :
```bash
git clone https://github.com/Oscarj-jqt/AIsoft
cd aisoft
```

### Installation de l'infrastructure:

 **Depuis le dossier back/**
  ```bash
  docker-compose up --build
  ```

  **Depuis le dossier front/cloudsoft/**
  
  -Lancer le frontend
  ```bash
  npm run dev
  ```
  
## Auteurs


  - Oscar JACQUET - DevOps, Développeur Back End
  - Alexis HU - Développeur Front End
  - Aryles BEN-CHABANE - Développeur Back End
  - Issa ABDOULAYE - Développeur Front End
  - Hugo DA ROCHA - Développeur Front End
    
