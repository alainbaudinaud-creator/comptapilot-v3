from flask import Blueprint, jsonify, request
from services.securite_probatoire_service import (
    initialiser_securite_probatoire,
    dashboard_securite_probatoire,
    enregistrer_audit,
    archiver_document_probatoire,
    signer_document,
)

bp_securite_probatoire = Blueprint("securite_probatoire", __name__)


@bp_securite_probatoire.route("/api/v3/securite-probatoire/dashboard")
def api_securite_dashboard():

    try:
        initialiser_securite_probatoire()

        return jsonify({
            "success": True,
            "module": "securite_probatoire_v3",
            "data": dashboard_securite_probatoire(),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp_securite_probatoire.route("/api/v3/securite-probatoire/audit")
def api_audit():

    return jsonify({
        "success": True,
        "resultat": enregistrer_audit("TEST_AUDIT_LEGAL", "SECURITE"),
    })


@bp_securite_probatoire.route("/api/v3/securite-probatoire/archive")
def api_archive():

    nom = request.args.get("nom", "document_demo.pdf")

    return jsonify({
        "success": True,
        "resultat": archiver_document_probatoire(nom),
    })


@bp_securite_probatoire.route("/api/v3/securite-probatoire/signature")
def api_signature():

    document = request.args.get("document", "document_demo.pdf")
    signataire = request.args.get("signataire", "client.demo@comptapilot.local")

    return jsonify({
        "success": True,
        "resultat": signer_document(document, signataire),
    })
