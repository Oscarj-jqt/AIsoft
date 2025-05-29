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

db = get_database()
users_collection = db["Users"]
weapon_collection = db["Weapons"]

# Chargement du modèle ResNet50
MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),  
        "..", "..", "dataset", "airsoft_resnet_model.h5"
    )
)
model = load_model(MODEL_PATH)

# Classe correspondante
class_names = ['ak47', 'beretta', 'glock', 'revolver']

def predict_weapon_class(img_path):
    # Charger l'image au format attendu (224x224 pour ResNet50)
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    
    # Prétraitement pour ResNet50
    from tensorflow.keras.applications.resnet50 import preprocess_input
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

    # Prétraitement pour ResNet
    img_pil = keras_image.load_img(image_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img_pil)
    img_array = np.expand_dims(img_array, axis=0)
    processed_img = preprocess_input(img_array)

    # Prédiction
    preds = model.predict(processed_img)
    predicted_class_index = np.argmax(preds)
    confidence = preds[0][predicted_class_index]

    # Seuil de confiance
    threshold = 0.6

    if confidence > threshold:
        weapon_name = class_names[predicted_class_index]
        return jsonify({
            "match_found": True,
            "weapon": {"name": weapon_name},
            "confidence_score": float(confidence),
            "processed_image": image_path
        })
    else:
        return jsonify({
            "match_found": False,
            "message": "Arme inconnue ou non reconnue avec confiance suffisante.",
            "confidence_score": float(confidence),
            "processed_image": image_path
        })
