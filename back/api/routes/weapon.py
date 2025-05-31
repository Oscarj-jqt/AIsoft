from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from mongodb.config.connection_db import get_database
# from utils.decorators import login_required
import os
import hashlib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.resnet50 import preprocess_input

# Dossier de stockage temporaire des images
UPLOAD_FOLDER = "/app/static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

upload_bp = Blueprint('upload', __name__)
analyze_bp = Blueprint('analyze', __name__)

# Base MongoDB et collections
db = get_database()
users_collection = db["Users"]
weapon_collection = db["Weapons"]

# Chargement du modèle ResNet50
MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),  
        "..", "..", "model", "aisoft_resnet_model.h5"
    )
)

model = load_model(MODEL_PATH)

# Classe correspondante
class_names = ['AK47', 'Beretta', 'Glock', 'Revolver']

# Dictionnaire de mapping
category_mapping = {
    'AK47': 'Fusil d’assaut',
    'Beretta': 'Pistolet',
    'Glock': 'Pistolet',
    'Revolver': 'Revolver'
}

def predict_weapon_class(img_path):
    # Charger et préparer l'image
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Prédiction
    preds = model.predict(x)
    predicted_index = np.argmax(preds)
    predicted_class = class_names[predicted_index]
    confidence = round(float(np.max(preds)) * 100, 2)


    # Ajouter la catégorie
    category = category_mapping.get(predicted_class, "Catégorie inconnue")

    return predicted_class, category, confidence


    # Charger l'image au format attendu (224x224 pour ResNet50)
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    
    # Prétraitement pour ResNet50
    x = preprocess_input(x)
    
    # Prédiction
    preds = model.predict(x)
    predicted_index = np.argmax(preds)
    predicted_class = class_names[predicted_index]
    confidence = float(np.max(preds)) * 100
    
    return predicted_class, confidence

# Indexer l'image pour éviter les doublons
def hash_image(image_file):
        """Crée un hash SHA256 de l'image"""
        image_file.seek(0)
        image_bytes = image_file.read()
        image_file.seek(0)
        return hashlib.sha256(image_bytes).hexdigest()

# Téléchargement d'arme
@upload_bp.route('/upload', methods=['POST'])
def upload_weapon():            
    name = request.form.get("name")
    brand = request.form.get("brand")
    image = request.files.get("image")

    if not image:
        return jsonify({"error": "L'image est requise"}), 400

    # Vérifie doublon via hash
    image_hash = hash_image(image)
    existing = weapon_collection.find_one({"image_hash": image_hash})
    if existing:
        return jsonify({"error": "Cette image a déjà été envoyée."}), 409

    # Sauvegarde image
    from uuid import uuid4
    ext = image.filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)


    new_weapon = {
        "weapon": {
            "name": name,
            "brand": brand,
            "image_hash": image_hash
        }
    }

    result = weapon_collection.insert_one(new_weapon)
    weapon_id = result.inserted_id

    return jsonify({"message": "Upload réussi", "weapon_id": str(weapon_id)}), 200

# Analyse d'arme (traitement et identification)
@analyze_bp.route('/analyze', methods=['POST'])
def analyze_weapon():
    image = request.files.get("image")
    if not image or image.filename == '':
        return jsonify({"error": "Image invalide."}), 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    # Obtenir les prédictions
    predicted_class, category, confidence = predict_weapon_class(image_path)

    threshold = 60.0  # même seuil que précédemment

    if confidence > threshold:
        return jsonify({
            "match_found": True,
            "weapon": {
                "name": predicted_class,
                "category": category
            },
            "confidence_score": confidence,
            "processed_image": image_path
        })
    else:
        return jsonify({
            "match_found": False,
            "message": "Arme inconnue ou non reconnue avec confiance suffisante.",
            "confidence_score": confidence,
            "processed_image": image_path
        })
