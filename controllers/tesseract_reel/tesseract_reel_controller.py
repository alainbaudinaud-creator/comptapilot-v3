from flask import Blueprint, jsonify, request
from services.tesseract_reel_service import (
    initialiser_tesseract_reel,
    analyser_document_tesseract,
    dashboard_tesseract,
)

bp_tesseract_reel = Blueprint("tesseract_reel", __name__)


@bp_tesseract_reel.route("/api/v3/tesseract/dashboard")
def api_tesseract_dashboard():

    try:

        initialiser_tesseract_reel()

        return jsonify({
            "success": True,
            "module": "tesseract_reel_v3",
            "data": dashboard_tesseract(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_tesseract_reel.route("/api/v3/tesseract/analyse", methods=["POST"])
def api_tesseract_analyse():

    try:

        initialiser_tesseract_reel()

        nom_fichier = request.form.get(
            "nom_fichier",
            "facture_demo.pdf"
        )

        resultat = analyser_document_tesseract(nom_fichier)

        return jsonify({
            "success": True,
            "resultat": resultat,
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


