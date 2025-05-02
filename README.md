CloudSoft

Une application qui permet d’analyser une image capturée (ex. GoPro pendant une partie d’Airsoft), d’identifier l’arme et ses accessoires grâce à une IA, puis de rechercher et comparer les prix de cette arme sur le web.

Lancer le serveur avec Docker
cd back
docker-compose up --build




## 📅 Planning par phases

### ✅ Phase 1 : Initialisation

- [x] Création du repo GitHub + branches (`main`, `back`, `front`, `infra`) – *Tous*
- [x] Initialisation de Flask + `requirements.txt` – *D2*
- [x] Mise en place du dossier MongoDB + fonction `get_database()` – *D1*
- [x] Création du fichier `.env` + valeurs fictives – *D2*

### ⚙️ Phase 2 : Infrastructure

- [ ] Dockerisation (Flask + MongoDB) – *D3*
- [ ] Setup MongoDB volume (persistance) – *D3*
- [ ] CI/CD simple avec GitHub Actions – *D4*
- [ ] Déploiement Cloud (Railway / Render) – *D4*
- [ ] Documentation Infra (README) – *D4*

### 🧠 Phase 3 : Développement Python

- [ ] Route `/upload` avec réception de l’image – *D2*
- [ ] Traitement image avec OpenCV ou PIL – *D1*
- [ ] Identification de l’arme via modèle IA pré-entraîné (CLIP / Hugging Face) – *D1*
- [ ] Recherche des prix via API web ou scraping – *D2*
- [ ] Enregistrement des résultats dans MongoDB – *D1*

### 💻 Phase 4 : Frontend et Intégration

- [ ] Interface d’accueil + upload image – *D5*
- [ ] Affichage résultat image + nom + prix – *D5*
- [ ] Test complet de l’application – *D5 & D2*

---