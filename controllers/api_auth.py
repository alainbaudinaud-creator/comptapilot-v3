import bcrypt

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from services.rbac_service import role_required
from extensions import limiter

from services.utilisateur_service import (
    recuperer_utilisateur_par_username,
    creer_utilisateur,
    lister_utilisateurs,
    recuperer_utilisateur_par_id,
    desactiver_utilisateur,
    modifier_role_utilisateur,
    modifier_password_utilisateur,
    supprimer_utilisateur
)

api_auth_routes = Blueprint('api_auth', __name__)
from flask_jwt_extended import create_access_token, jwt_required
from services.rbac_service import role_required
from services.audit_service import ajouter_log

api_auth_routes = Blueprint('api_auth', __name__)

@api_auth_routes.route('/auth/login', methods=['POST'])
@limiter.limit("2 per minute")
def api_login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    utilisateur = recuperer_utilisateur_par_username(username)

    if not utilisateur:
        return jsonify({
            "error": "Identifiants invalides"
        }), 401

    if not bcrypt.checkpw(
        password.encode('utf-8'),
        utilisateur[2].encode('utf-8')
    ):
        return jsonify({
            "error": "Identifiants invalides"
        }), 401

    if utilisateur[4] != 1:
        return jsonify({
            "error": "Utilisateur inactif"
        }), 403

    token = create_access_token(
        identity=utilisateur[1],
        additional_claims={
            "role": utilisateur[3],
            "user_id": utilisateur[0]
        }
    )

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "role": utilisateur[3],
        "user_id": utilisateur[0]
    })
@api_auth_routes.route('/auth/users', methods=['POST'])
@jwt_required()
@role_required("ADMIN")
def api_creer_utilisateur():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username:
        return jsonify({"error": "Champ username obligatoire"}), 400

    if not password:
        return jsonify({"error": "Champ password obligatoire"}), 400

    if role not in ["ADMIN", "COMPTABLE", "CLIENT"]:
        return jsonify({"error": "Rôle invalide"}), 400

    utilisateur_existant = recuperer_utilisateur_par_username(username)

    if utilisateur_existant:
        return jsonify({"error": "Utilisateur déjà existant"}), 409

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    utilisateur_id = creer_utilisateur(
        username,
        password_hash,
        role
    )
    ajouter_log(
        "CREATION_UTILISATEUR",
        f"Utilisateur créé : {username} ({role})"
    )

    return jsonify({
        "message": "Utilisateur créé avec succès",
        "utilisateur": {
            "id": utilisateur_id,
            "username": username,
            "role": role,
            "actif": 1
        }
    }), 201
@api_auth_routes.route('/auth/users', methods=['GET'])
@jwt_required()
@role_required("ADMIN")
def api_lister_utilisateurs():
    utilisateurs = lister_utilisateurs()

    return jsonify([
        {
            "id": u[0],
            "username": u[1],
            "role": u[2],
            "actif": u[3],
            "date_creation": u[4]
        }
        for u in utilisateurs
    ])
@api_auth_routes.route('/auth/users/<int:utilisateur_id>/disable', methods=['PUT'])
@jwt_required()
@role_required("ADMIN")
def api_desactiver_utilisateur(utilisateur_id):
    utilisateur = recuperer_utilisateur_par_id(utilisateur_id)

    if not utilisateur:
        return jsonify({
            "error": "Utilisateur introuvable"
        }), 404

    desactiver_utilisateur(utilisateur_id)
    ajouter_log(
        "DESACTIVATION_UTILISATEUR",
        f"Utilisateur désactivé : ID {utilisateur_id}"
    )

    return jsonify({
        "message": "Utilisateur désactivé avec succès",
        "utilisateur_id": utilisateur_id
    })
@api_auth_routes.route('/auth/users/<int:utilisateur_id>/role', methods=['PUT'])
@jwt_required()
@role_required("ADMIN")
def api_modifier_role_utilisateur(utilisateur_id):
    data = request.get_json()

    nouveau_role = data.get("role")

    if nouveau_role not in ["ADMIN", "COMPTABLE", "CLIENT"]:
        return jsonify({
            "error": "Rôle invalide"
        }), 400

    utilisateur = recuperer_utilisateur_par_id(utilisateur_id)

    if not utilisateur:
        return jsonify({
            "error": "Utilisateur introuvable"
        }), 404

    modifier_role_utilisateur(utilisateur_id, nouveau_role)
    ajouter_log(
        "MODIFICATION_ROLE",
        f"Utilisateur ID {utilisateur_id} → rôle {nouveau_role}"
    )

    return jsonify({
        "message": "Rôle utilisateur modifié avec succès",
        "utilisateur_id": utilisateur_id,
        "nouveau_role": nouveau_role
    })
@api_auth_routes.route('/auth/users/<int:utilisateur_id>/password', methods=['PUT'])
@jwt_required()
@role_required("ADMIN")
def api_modifier_password_utilisateur(utilisateur_id):
    data = request.get_json()

    nouveau_password = data.get("password")

    if not nouveau_password:
        return jsonify({
            "error": "Mot de passe obligatoire"
        }), 400

    utilisateur = recuperer_utilisateur_par_id(utilisateur_id)

    if not utilisateur:
        return jsonify({
            "error": "Utilisateur introuvable"
        }), 404

    password_hash = bcrypt.hashpw(
        nouveau_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    modifier_password_utilisateur(
        utilisateur_id,
        password_hash
    )   
    ajouter_log(
        "RESET_PASSWORD",
        f"Mot de passe modifié pour utilisateur ID {utilisateur_id}"
    )
    

    return jsonify({
        "message": "Mot de passe modifié avec succès",
        "utilisateur_id": utilisateur_id
    })
@api_auth_routes.route('/auth/users/<int:utilisateur_id>', methods=['DELETE'])
@jwt_required()
@role_required("ADMIN")
def api_supprimer_utilisateur(utilisateur_id):
    utilisateur = recuperer_utilisateur_par_id(utilisateur_id)

    if not utilisateur:
        return jsonify({
            "error": "Utilisateur introuvable"
        }), 404

    supprimer_utilisateur(utilisateur_id)
    ajouter_log(
        "SUPPRESSION_UTILISATEUR",
        f"Utilisateur supprimé : ID {utilisateur_id}"
    )

    return jsonify({
        "message": "Utilisateur supprimé avec succès",
        "utilisateur_id": utilisateur_id
    })


