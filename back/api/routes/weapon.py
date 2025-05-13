from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.utils import secure_filename
from mongodb.config.connection_db import get_database
from utils.decorators import login_required
import os
import cv2 as cv
from ultralytics import YOLO

# Dossier de stockage temporaire des images
UPLOAD_FOLDER = "front/cloudsoft/static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# route de téléchargement d'arme
upload_bp = Blueprint('upload', __name__, template_folder='front/templates')

# route de détection d'arme, l'IA va analyser pour détecter l'arme et retourner ses caractéristiques
detect_bp = Blueprint('detect', __name__, template_folder='front/templates')

db = get_database()
users_collection = db["Users"]
weapon_collection = db["Weapons"]

# Chargement du modèle YOLOv11 pour la détection d'armes
yolo_model = YOLO("yolo11n.pt") 

#Route de téléchargement d'arme
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

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
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

#Route de détection d'arme
@detect_bp.route('/detect', methods=['GET'])
@login_required
def detect_weapon_form():
    """
    Afficher le formulaire de détection d'une arme.
    """
    return render_template('detect_form.html')


@detect_bp.route('/detect', methods=['POST'])
@login_required
def detect_weapon():
    """
    Traiter le formulaire de détection d'une arme.
    """
    image = request.files.get("image")

    # Vérifier que l'image est fournie
    if not image:
        flash("Aucune image reçue","Veuillez en télécharger une")
        return redirect(url_for('upload.upload_weapon_form'))
    
    if image.filename == '':
        flash("Fichier vide.", "warning")
        return redirect(url_for('upload.upload_weapon_form'))
    
    
    # Sécuriser et sauvegarder l'image
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    # Détection avec YOLOv11
    results = yolo_model(image_path)

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

    # Importation de l'image dans la base de données
    new_weapon = {
        "weapon": {
            "name": detected_classes[0]["class"] if detected_classes else "Unknown",
            "brand": "",
            "model": "",
            "type": "",
            "price": None,
            "detected_by_ai": True,
            "image_path": image_path,
            "description": "",
            "created_at": datetime.utcnow()
        }
    }

    weapon_collection.insert_one(new_weapon)       

    return jsonify({
        "filename": "Détection réussie et enregistrement effectué.",
        "detected": detected_classes,
        "saved_weapon": new_weapon["weapon"]
    })

#Route de l'identification d'arme
@detect_bp.route('/process', methods=['GET'])
@login_required
def process_weapon():
    """
    Traiter le formulaire de détection d'une arme.
    """
    return render_template('process_form.html')

@detect_bp.route('/process', methods=['POST'])
@login_required
def process_weapon_post():
    """
    Traiter le formulaire de traitement d'une arme avec OpenCV
    """
    image = request.files.get("image")

    # Vérifier que l'image est fournie
    if not image:
        flash("Aucune image reçue","Veuillez en télécharger une")
        return redirect(url_for('upload.upload_weapon_form'))
    
    if image.filename == '':
        flash("Fichier vide.", "warning")
        return redirect(url_for('upload.upload_weapon_form'))
    
    # Sécuriser et sauvegarder l'image
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    # Traitement de l'image avec OpenCV (exemple : conversion en niveaux de gris)
    img = cv.imread(image_path)
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Enregistrer l'image traitée
    processed_image_path = os.path.join(UPLOAD_FOLDER, f"processed_{filename}")
    cv.imwrite(processed_image_path, gray_img)

    return jsonify({
        "filename": processed_image_path,
        "message": "Image traitée avec succès."
    })
    
