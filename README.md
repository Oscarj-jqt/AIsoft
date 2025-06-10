# AIsoft

**AIsoft** est une application capable d’analyser une image uploadée, d’identifier une arme grâce à une intelligence artificielle intégrée, puis de rechercher les sources de cette arme pour la retrouver.


## Infrastructure du projet

### Dockerisation

Le projet est conteneurisé avec **Docker**, et repose sur :

- Un service **backend** développé avec **Flask**.
- Une base de données **MongoDB**.

> L’infrastructure se lance via `docker-compose` depuis le dossier `back/`.

---

## CI/CD & Hébergement

### Intégration Continue (CI)

- L’application utilise **GitHub Actions** pour automatiser :
  - l’installation des dépendances,
  - la vérification du code source,
  - le déclenchement des workflows à chaque `push` ou `pull request` sur la branche `main`.

### Hébergement Cloud (Azure)

- L’infrastructure est conçue pour être **déployée automatiquement sur Microsoft Azure** via GitHub Actions.
- **Serveur backend (Flask)** hébergé sur Azure :  
  [https://cloudsoft-e2h0egbma8a9agc6.francecentral-01.azurewebsites.net](https://cloudsoft-e2h0egbma8a9agc6.francecentral-01.azurewebsites.net)
- **Frontend statique** hébergé sur Azure :  
  [https://calm-mushroom-0eda30b03.6.azurestaticapps.net](https://calm-mushroom-0eda30b03.6.azurestaticapps.net)

### Déploiement Continu (CD)

- Le code est automatiquement mis à jour sur Azure grâce au **déploiement continu** configuré avec GitHub Actions.

---

## Serveur et Base de Données

### Backend

Le backend est développé en **Python avec Flask**. Il expose plusieures routes API RESTful :

- `POST /register` & `POST /login` : création de compte et authentification
- `POST /upload` : permet à l’utilisateur connecté de **téléverser une image**.
- `POST /analyze` : lance **l’analyse par IA** entraînée pour identifier l’arme présente dans l’image puis recherche les sources 

### Base de Données (MongoDB)

La base de données utilisée est **MongoDB**, avec deux collections principales :

- `users` : stocke les informations des utilisateurs.
- `weapons` : stocke les résultats des analyses d’armes

---

## Interface Utilisateur

### Frontend (React + Tailwind CSS)

Le frontend est développé avec **React** et utilise **Tailwind CSS** pour les composants graphiques.  
L’interface permet de :

- Se connecter ou créer un compte.
- Uploader une image.
- Visualiser le résultat d’analyse en temps réel.
- Obtenir des ressources réelles pour se procurer l'arme

---

## Installation et Configuration


### Télécharger le modèle IA requis
L'application nécessite un modèle IA pour effectuer la fonctionnalité d'intelligence artificielle.

Télécharger le modèle ResNet50 "aisoft_resnet_model.h5" ici :
https://drive.google.com/drive/folders/1ZCgY-3rM_GiuHx4W9QfvvsxpftVQX0Uc

Placez le fichier téléchargé à cet emplacement précis :

aisoft/back/model/


### Cloner le projet

```bash
git clone https://github.com/Oscarj-jqt/AIsoft
cd aisoft
```

### Démarrer l'application:

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
