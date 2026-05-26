from flask import Blueprint, jsonify, request
from services.openai_reel_service import (
    initialiser_openai_reel,
    analyser_facture_openai,
    dashboard_openai_reel,
)

bp_openai_reel = Blueprint("openai_reel", __name__)


@bp_openai_reel.route("/api/v3/openai/dashboard")
def api_openai_dashboard():

    try:
        initialiser_openai_reel()

        return jsonify({
            "success": True,
            "module": "openai_reel_v3",
            "data": dashboard_openai_reel(),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_openai_reel.route("/api/v3/openai/analyse-facture", methods=["POST", "GET"])
def api_openai_analyse_facture():

    try:
        initialiser_openai_reel()

        data = request.get_json(silent=True) or {}

        texte = data.get(
            "texte",
            "FACTURE DEMO OPENAI HT 1000 TVA 200 TTC 1200 FOURNISSEUR DEMO"
        )

        resultat = analyser_facture_openai(texte)

        return jsonify({
            "success": True,
            "resultat": resultat,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

