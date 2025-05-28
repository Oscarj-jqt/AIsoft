from datetime import datetime
from flask import Blueprint, redirect, url_for, flash, request, jsonify, session
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from mongodb.config.connection_db import get_database
# from utils.decorators import login_required
import os
import cv2 as cv
import numpy as np
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
        from uuid import uuid4
        import os

        ext = image.filename.split('.')[-1]
        filename = f"{uuid4()}.{ext}"

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

    # Traitement Opencv : conversion en niveaux de gris et redimensionnement
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    resized = cv.resize(gray, (100, 100))
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
            # "uploaded_by": ObjectId(user_id)
        },
        "image_features": flattened_features
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
    Traitement de l'image (Opencv) + Matching dans MongoDB.
    Retourne les détails de l'arme identifiée (ou un message d'échec).
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
    img_resized = cv.resize(gray, (100, 100)).flatten().tolist()

    # 4. Matching dans MongoDB
    best_match = None
    min_diff = float("inf")
    threshold = 80  # seuil au-delà duquel on considère qu'il n'y a pas de correspondance fiable

    for weapon in weapon_collection.find({"image_features": {"$exists": True}}):
        db_features = np.array(weapon["image_features"], dtype=np.uint8)

        diff = np.linalg.norm(img_resized - db_features)

        print(f"Comparaison avec {weapon['weapon']['name']} : diff = {diff}")

        if diff < min_diff:
            min_diff = diff
            best_match = weapon

    if min_diff < 30:
        note = "Excellent match"
    elif min_diff < 60:
        note = "Match probable"
    elif min_diff < 100:
        note = "Match douteux"
    else:
        note = "Aucun match"

    # Après avoir trouvé le meilleur match, vérifier si le diff est suffisamment bas
    if best_match and min_diff < threshold:
        return jsonify({
            "match_found": True,
            "weapon": {
                "name": best_match["weapon"]["name"],
                "brand": best_match["weapon"]["brand"],
                "model": best_match["weapon"]["model"]
            },
            "confidence_score": round(100 - min_diff / 10, 2),
            "processed_image": processed_path
        }), 200
    else:
        print(f"Aucun match fiable trouvé. Meilleure différence : {min_diff}")
        return jsonify({
            "match_found": False,
            "message": "Aucune correspondance trouvée dans la base.",
            "note": note,
            "next_step": "Enrichir la base ou faire une identification manuelle.",
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


