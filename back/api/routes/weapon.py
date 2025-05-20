from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from mongodb.config.connection_db import get_database
from utils.decorators import login_required
import os
import cv2 as cv
import numpy as np

# Dossier de stockage temporaire des images
UPLOAD_FOLDER = "front/cloudsoft/static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# route de téléchargement d'arme
upload_bp = Blueprint('upload', __name__, template_folder='front/templates')

# route de traitement d'arme
process_bp = Blueprint('process', __name__, template_folder='front/templates')

# route d'identification d'arme
identify_bp = Blueprint('identify', __name__, template_folder='front/templates')

# Connexion à la base de données MongoDB et récupération des collections
db = get_database()
users_collection = db["Users"]
weapon_collection = db["Weapons"]


# Téléchargement d'arme
@upload_bp.route('/upload', methods=['GET'])
@login_required
def upload_weapon_form():
    """
    Afficher le formulaire de création d'une nouvelle arme.
    """
    return render_template('upload_form.html')

@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_weapon():            
    """
    Traiter le formulaire de création d'une nouvelle arme.
    """

    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    weapon_type = request.form.get("type")
    price = request.form.get("price")
    description = request.form.get("description")
    image = request.files.get("image")

    # Validation des champs
    if not name or not weapon_type or not description or not image:
        flash("Tous les champs doivent être remplis.", "warning")
        return redirect(url_for('upload.upload_weapon_form'))

    # L'enregistrement de l'image
    filename = None
    image_path = None
    if image:
        from uuid import uuid4
        import os

        ext = image.filename.split('.')[-1]
        filename = f"{uuid4()}.{ext}"

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

    # Traitement OpenCV : conversion en niveaux de gris et redimensionnement
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (100, 100))
    flattened_features = resized.flatten().tolist()
    

    new_weapon = {
        "weapon": {
            "name": name,
            "brand": brand,
            "model": model,
            "type": weapon_type,
            "price": float(price) if price else None,
            "image_path": image_path,
            "description": description,
            "created_at": datetime.utcnow(),
            "uploaded_by": ObjectId(session['user_id'])
        },
        "image_features": flattened_features
    }

    result = weapon_collection.insert_one(new_weapon)
    weapon_id = result.inserted_id


    users_collection.update_one(
    {"_id": ObjectId(session['user_id'])},
    {"$push": {"uploaded_weapons": weapon_id}}
)



    flash("Arme créée avec succès.", "success")
    return redirect(url_for('upload.upload_weapon_form'))

# Traitement d'arme
@process_bp.route('/process', methods=['GET'])
@login_required
def process_weapon():
    """
    Traiter le formulaire de détection d'une arme.
    """
    return render_template('process_form.html')

@process_bp.route('/process', methods=['POST'])
@login_required
def process_weapon_post():
    """
    Traitement OpenCV + matching avec base MongoDB
    """
    image = request.files.get("image")
    if not image or image.filename == '':
        flash("Image invalide.", "warning")
        return redirect(url_for('upload.upload_weapon_form'))

    # Sauvegarde locale de l’image
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    # Amélioration de la qualité de l'image avec OpenCV
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    processed_path = os.path.join(UPLOAD_FOLDER, f"processed_{filename}")
    cv.imwrite(processed_path, gray)

    # Feature extraction simple
    img_resized = cv.resize(gray, (100, 100)).flatten()

    # Matching dans MongoDB , comparaison avec les images de la base
    best_match = None
    min_diff = float("inf")

    for weapon in weapon_collection.find({"image_features": {"$exists": True}}):
        db_features = np.array(weapon["image_features"])
        diff = np.linalg.norm(img_resized - db_features)

        if diff < min_diff and diff < 1000: 
            min_diff = diff
            best_match = weapon

    if best_match:
        return jsonify({
            "match_found": True,
            "weapon": {
                "name": best_match["weapon"]["name"],
                "brand": best_match["weapon"]["brand"],
                "model": best_match["weapon"]["model"]
            },
            "confidence_score": round(100 - min_diff / 10, 2),
            "processed_image": processed_path
        })
    else:
        return jsonify({
            "match_found": False,
            "message": "Aucune correspondance trouvée dans la base.",
            "next_step": "Le matching n'a pas abouti. Utilisez la méthode d'identification"
        })


# Identification d'arme
@identify_bp.route('/identify', methods=['GET'])
@login_required
def identify_weapon_form():
    """
    Afficher le formulaire d'identification d'une arme.
    """
    return render_template('identify_form.html')

@identify_bp.route('/identify', methods=['POST'])
@login_required
def identify_weapon():
    return