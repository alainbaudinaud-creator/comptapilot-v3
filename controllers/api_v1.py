from flask import Blueprint, jsonify, request

from services.audit_service import lister_logs
from services.bancaire_service import lister_ecritures_bancaires
from services.taches_v7_service import (
    lister_taches_actives,
    creer_tache_v7,
    recuperer_tache_v7_par_id,
    modifier_tache_v7,
    supprimer_tache_v7
)
from services.api_security_service import api_key_required
from flask_jwt_extended import jwt_required
from services.rbac_service import role_required


api_v1_routes = Blueprint('api_v1', __name__)


@api_v1_routes.route('/health')
def api_health():
    return jsonify({
        "status": "ok",
        "application": "ComptaPilot",
        "api": "v1"
    })


@api_v1_routes.route('/audit/logs')
@jwt_required()
@api_key_required
@role_required("ADMIN")
def api_audit_logs():
    logs = lister_logs(50)

    return jsonify([
        {
            "id": log[0],
            "action": log[1],
            "detail": log[2],
            "date_action": log[3]
        }
        for log in logs
    ])
@api_v1_routes.route('/bancaire/ecritures')
@jwt_required()
@api_key_required
@role_required(["ADMIN", "COMPTABLE"])
def api_bancaire_ecritures():
    ecritures = lister_ecritures_bancaires()

    return jsonify([
        {
            "id": e[0],
            "date_ecriture": e[1],
            "piece": e[2],
            "libelle": e[3],
            "debit": e[4],
            "credit": e[5],
            "rapproche_bancaire": e[6]
        }
        for e in ecritures
    ])


@api_v1_routes.route('/v7/taches-actives')
@jwt_required()
def api_taches_actives():
    taches = lister_taches_actives()

    return jsonify([
        {
            "id": t[0],
            "nom": t[1],
            "type_tache": t[2],
            "frequence": t[3],
            "statut": t[4],
            "date_creation": t[5]
        }
        for t in taches
    ])


@api_v1_routes.route('/v7/taches', methods=['POST'])
@api_key_required
def api_creer_tache_v7():
    """
    Création d'une tâche V7
    ---
    tags:
      - Tâches V7
    """

    data = request.get_json()

    nom = data.get('nom')
    type_tache = data.get('type_tache')
    frequence = data.get('frequence')

    if not nom:
        return jsonify({
            "error": "Champ nom obligatoire"
        }), 400

    if not type_tache:
        return jsonify({
            "error": "Champ type_tache obligatoire"
        }), 400

    if not frequence:
        return jsonify({
            "error": "Champ frequence obligatoire"
        }), 400

    tache_id = creer_tache_v7(
        nom,
        type_tache,
        frequence
    )

    return jsonify({
        "message": "Tâche créée avec succès",
        "tache": {
            "id": tache_id,
            "nom": nom,
            "type_tache": type_tache,
            "frequence": frequence,
            "statut": "ACTIVE"
        }
    }), 201

@api_v1_routes.route('/v7/taches/<int:tache_id>', methods=['GET'])
@api_key_required
def api_recuperer_tache_v7(tache_id):
    tache = recuperer_tache_v7_par_id(tache_id)

    if not tache:
        return jsonify({
            "error": "Tâche introuvable"
        }), 404

    return jsonify({
        "id": tache[0],
        "nom": tache[1],
        "type_tache": tache[2],
        "frequence": tache[3],
        "statut": tache[4],
        "date_creation": tache[5]
    })

@api_v1_routes.route('/v7/taches/<int:tache_id>', methods=['PUT'])
@api_key_required
def api_modifier_tache_v7(tache_id):
    tache_existante = recuperer_tache_v7_par_id(tache_id)

    if not tache_existante:
        return jsonify({
            "error": "Tâche introuvable"
        }), 404

    data = request.get_json()

    nom = data.get('nom', tache_existante[1])
    type_tache = data.get('type_tache', tache_existante[2])
    frequence = data.get('frequence', tache_existante[3])
    statut = data.get('statut', tache_existante[4])

    modifier_tache_v7(
        tache_id,
        nom,
        type_tache,
        frequence,
        statut
    )

    return jsonify({
        "message": "Tâche modifiée avec succès",
        "tache": {
            "id": tache_id,
            "nom": nom,
            "type_tache": type_tache,
            "frequence": frequence,
            "statut": statut
        }
    })

@api_v1_routes.route('/v7/taches/<int:tache_id>', methods=['DELETE'])
@jwt_required()
@role_required("ADMIN")
def api_supprimer_tache_v7(tache_id):
    tache_existante = recuperer_tache_v7_par_id(tache_id)

    if not tache_existante:
        return jsonify({
            "error": "Tâche introuvable"
        }), 404

    supprimer_tache_v7(tache_id)

    return jsonify({
        "message": "Tâche supprimée avec succès",
        "id_supprime": tache_id
    })
