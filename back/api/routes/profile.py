from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from mongodb.config.connection_db import get_database
from bson.objectid import ObjectId
from utils.decorators import login_required

profile_bp = Blueprint('profile', __name__, template_folder='front/templates')

db = get_database()
users_collection = db["Users"]
weapon_collection = db["Weapons"]

@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    Afficher les informations de base de l'utilisateur.
    """
    if 'user_id' not in session:
        flash("Veuillez vous connecter pour accéder à votre profil.", "warning")
        return redirect(url_for('auth.login'))

    user = users_collection.find_one({"_id": ObjectId(session['user_id'])})
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for('auth.login'))
    

    uploaded_weapon_ids = user.get("uploaded_weapons", [])
    uploaded_weapons = list(weapon_collection.find({"_id": {"$in": uploaded_weapon_ids}}))

    return render_template('profile.html', user=user, uploaded_weapons=uploaded_weapons)


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Permet à l'utilisateur de modifier son pseudo.
    (On ne modifie pas le mot de passe ici pour des raisons de sécurité)
    """
    if 'user_id' not in session:
        flash("Veuillez vous connecter pour modifier votre profil.", "warning")
        return redirect(url_for('auth.login'))

    user = users_collection.find_one({"_id": ObjectId(session['user_id'])})
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_pseudo = request.form.get("pseudo")
        if new_pseudo:
            users_collection.update_one(
                {"_id": ObjectId(session['user_id'])},
                {"$set": {"pseudo": new_pseudo}}
            )
            flash("Pseudo mis à jour avec succès.", "success")
            return redirect(url_for('profile.profile'))
        else:
            flash("Le champ pseudo ne peut pas être vide.", "warning")

    return render_template('edit_profile.html', user=user)


