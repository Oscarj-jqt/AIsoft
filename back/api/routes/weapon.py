from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from mongodb.config.connection_db import get_database
from utils.decorators import login_required
from bson.objectid import ObjectId

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
    if not name or not brand or not model or not weapon_type or not description or not image:
        flash("Tous les champs doivent être remplis.", "warning")
        return redirect(url_for('upload.upload_weapon_form'))

    # Gérer l'enregistrement de l'image
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
