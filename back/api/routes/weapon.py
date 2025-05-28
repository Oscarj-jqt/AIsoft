from datetime import datetime
from flask import Blueprint, redirect, url_for, flash, request, jsonify, session
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from mongodb.config.connection_db import get_database
# from utils.decorators import login_required
import os
import hashlib
import cv2 as cv
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import Model
# from transformers import pipeline
# from PIL import Image

# Dossier de stockage temporaire des images
UPLOAD_FOLDER = "/app/static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# route de téléchargement d'arme
upload_bp = Blueprint('upload', __name__)

analyze_bp = Blueprint('analyze', __name__)
# Connexion à la base de données MongoDB et récupération des collections
db = get_database()
users_collection = db["Users"]
weapon_collection = db["Weapons"]

# Initialiser le modèle ResNet50 sans la couche de classification
resnet_model = ResNet50(weights="imagenet", include_top=False, pooling="avg")

def extract_features_resnet(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    features = resnet_model.predict(image)[0] 
    return features.tolist()
# Indexer l'image pour éviter les doublons
def hash_image(image_file):
        """Crée un hash SHA256 de l'image"""
        image_file.seek(0)
        image_bytes = image_file.read()
        image_file.seek(0)
        return hashlib.sha256(image_bytes).hexdigest()

# Affichage des armes stockées dans la base de données
@upload_bp.route('/weapons', methods=['GET'])
def get_all_weapons():
    db = get_database()
    weapons = list(db["Weapons"].find())
    for w in weapons:
        w["_id"] = str(w["_id"])
        w["weapon"]["uploaded_by"] = str(w["weapon"]["uploaded_by"])
    return jsonify(weapons)


# Téléchargement d'arme
@upload_bp.route('/upload', methods=['POST'])
# @login_required
def upload_weapon():            
    
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    weapon_type = request.form.get("type")
    price = request.form.get("price")
    description = request.form.get("description")
    image = request.files.get("image")
    # user_id = request.form.get("user_id")  

    # Validation des champs
    if not image:
        flash("L'image est requise", "warning")
        return redirect(url_for('home'))
    
    # L'enregistrement de l'image
    filename = None
    image_path = None
    if image:
        image_hash = hash_image(image)
        # Vérifie si une image identique a déjà été enregistrée
        existing = weapon_collection.find_one({"image_hash": image_hash})
        if existing:
            return jsonify({"error": "Cette image a déjà été envoyée."}), 409
        from uuid import uuid4

        ext = image.filename.split('.')[-1]
        filename = f"{uuid4()}.{ext}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

    # Traitement Opencv : conversion en niveaux de gris et redimensionnement
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    resized = cv.resize(gray, (100, 100))
    # flattened_features = resized.flatten().tolist()
    
    features = extract_features_resnet(image_path)

    new_weapon = {
        "weapon": {
            "name": name,
            "brand": brand,
            "model": model,
            "image_hash": image_hash
        },
        "image_features": features
    }

    result = weapon_collection.insert_one(new_weapon)
    weapon_id = result.inserted_id
    
    

    # users_collection.update_one(
    # {"_id": ObjectId(session['user_id'])},
    # {"$push": {"uploaded_weapons": weapon_id}}
# )

    return jsonify({"message": "Upload réussi", "weapon_id": str(weapon_id)}), 200


# Analyse d'arme (traitement et identification)

@analyze_bp.route('/analyze', methods=['POST'])
# @login_required
def analyze_weapon():
    """
    Traitement de l'image (OpenCV) + Matching dans MongoDB.
    """
    image = request.files.get("image")
    if not image or image.filename == '':
        return jsonify({"error": "Image invalide."}), 400

    # 1. Sauvegarde temporaire
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    # 2. Traitement de l'image
    img = cv.imread(image_path)
    if img is None:
        return jsonify({"error": "Erreur lors du chargement de l'image."}), 500

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    processed_path = os.path.join(UPLOAD_FOLDER, f"processed_{filename}")
    cv.imwrite(processed_path, gray)

    # 3. Préparation des features
    img_resized_features = extract_features_resnet(image_path)


    # 4. Matching dans MongoDB
    best_match = None
    min_diff = float("inf")
    THRESHOLD = 60  # seuil de rejet des mauvaises correspondances
    MAX_DIFF = 150  # pour normaliser le score de confiance

    img_features = np.array(img_resized_features)


    for weapon in weapon_collection.find({"image_features": {"$exists": True}}):
        db_features = np.array(weapon["image_features"])

        
        diff = np.linalg.norm(img_features - db_features)

        print(f"Comparaison avec {weapon['weapon']['name']} : diff = {diff}")

        if diff < min_diff:
            min_diff = diff
            best_match = weapon

    # Normalisation du score
    confidence_score = max(0, round(100 * (1 - min_diff / MAX_DIFF), 2))

    if min_diff < 30:
        note = "Excellent match"
    elif min_diff < 60:
        note = "Match probable"
    elif min_diff < 100:
        note = "Match douteux"
    else:
        note = "Aucun match"

    if best_match and min_diff < THRESHOLD:
        return jsonify({
            "match_found": True,
            "weapon": {
                "name": best_match["weapon"]["name"],
                "brand": best_match["weapon"]["brand"],
                "model": best_match["weapon"]["model"]
            },
            "confidence_score": confidence_score,
            "note": note,
            "processed_image": processed_path
        }), 200
    else:
        print(f"Aucun match fiable trouvé. Meilleure différence : {min_diff}")
        return jsonify({
            "match_found": False,
            "message": "Aucune correspondance trouvée dans la base.",
            "note": note,
            "confidence_score": confidence_score,
            "processed_image": processed_path
        }), 200




    # # Charger le pipeline de HuggingFace pour l'image-to-text
    # captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

    # # Charger l'image à partir du chemin local (uploadé par l'utilisateur)
    # image = Image.open(image_path)

    # # Générer la description de l'image
    # caption = captioner(image)

    # # Extraction du texte généré
    # generated_text = caption[0]['generated_text']

    # # Affichage du texte généré
    # flash(f"Texte généré : {generated_text}", "success")

    # # On peut prendre ce texte généré et l'insérér dans la propriété "description" de l'arme
    # # ou l'utiliser pour d'autres traitements
    # # Par exemple, on peut l'enregistrer dans la base de données
    # # ou l'afficher à l'utilisateur
    # # Pour l'instant, on va juste l'afficher
    # return render_template('identify_weapon.html', generated_text=generated_text, image_path=image_path)

    # # Si aucune correspondance n'est trouvée, on redirige vers le formulaire
    # flash("Aucune correspondance trouvée.", "warning")
    # return redirect(url_for('upload.upload_weapon_form'))

    # # Envoie de l'image à l'API IA de reconnaissance d'arme
    # # URL avec HuggingFace
    # # api_url = "https://api-inference.huggingface.co/models/username/model_name"
    
    # # files = {'image': open(image_path, 'rb')}

    # # response = requests.post(api_url, files=files)
    # # if response.status_code == 200:
    # #     data = response.json()
    # #     if data.get("match_found"):
    # #         weapon = data["weapon"]
    # #         confidence_score = data["confidence_score"]
    # #         processed_image = data["processed_image"]

    # #         return render_template('identify_weapon.html', weapon=weapon, confidence_score=confidence_score, processed_image=processed_image)
    # #     else:
    # #         flash(data.get("message", "Aucune correspondance trouvée."), "warning")
    # # else:
    # #     flash("Erreur lors de l'appel à l'API IA.", "danger")

    # # Charger le pipeline de HuggingFace pour l'image-to-text
    

# Enregistrement des blueprints
# def register_routes(app):
#     app.register_blueprint(upload_bp)


