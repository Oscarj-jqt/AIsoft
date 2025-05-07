from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.utils import secure_filename
from mongodb.config.connection_db import get_database
from utils.decorators import login_required
import os
from ultralytics import YOLO

# Dossier de stockage temporaire des images
UPLOAD_FOLDER = "front/cloudsoft/static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# route de téléchargement d'arme
upload_bp = Blueprint('upload', __name__, template_folder='front/templates')


db = get_database()
users_collection = db["Users"]
weapon_collection = db["Weapons"]

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

    # Vérifier que les champs obligatoires sont remplis
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
        upload_folder = 'front/cloudsoft/static/images' 
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

    new_weapon = {
        "weapon": {
            "name": name,
            "brand": brand,
            "model": model,
            "type": weapon_type,
            "price": float(price) if price else None,
            "detected_by_ai": False,
            "image_path": image_path,
            "description": description,
            "created_at": datetime.utcnow()
        }
    }

    # Insertion dans la base de données
    weapon_collection.insert_one(new_weapon)

    flash("Arme créée avec succès.", "success")
    return redirect(url_for('upload.upload_weapon_form'))

# route de détection d'arme, l'IA va analyser pour détecter l'arme et retourner ses caractéristiques
detect_bp = Blueprint('detect', __name__, template_folder='front/templates')

model = YOLO("yolo11n.pt") 


@detect_bp.route('/detect', methods=['POST'])
@login_required
def detect_weapon():
    """
    Traiter le formulaire de détection d'une arme.
    """
    image = request.files.get("image")

    # Vérifier que l'image est fournie
    if not image in request.files:
        flash("Aucune image reçue","Veuillez en télécharger une")
        return redirect(url_for('upload.upload_weapon_form'))
    
    image_file = request.files['image']

    if image_file.filename == '':
        flash("Fichier vide.", "warning")
        return redirect(url_for('upload.upload_weapon_form'))
    
    
    # Sécuriser et sauvegarder l'image
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(image_path)

    # Détection avec YOLOv11
    results = model(image_path)

    # Extraction des objets détectés
    detected_classes = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]
            detected_classes.append({
                "class": class_name,
                "confidence": round(confidence, 2)
            }) 

    return jsonify({
        "filename": filename,
        "detected_objects": detected_classes
    })