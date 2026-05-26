from flask import Blueprint, jsonify
from services.orchestration_reelle_service import (
    initialiser_orchestration_reelle,
    lancer_worker_pdf,
    lancer_worker_excel,
    dashboard_orchestration,
)

bp_orchestration_reelle = Blueprint("orchestration_reelle", __name__)


@bp_orchestration_reelle.route("/api/v3/orchestration/dashboard")
def api_orchestration_dashboard():

    try:

        initialiser_orchestration_reelle()

        return jsonify({
            "success": True,
            "module": "orchestration_reelle_v3",
            "data": dashboard_orchestration(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_orchestration_reelle.route("/api/v3/orchestration/pdf")
def api_orchestration_pdf():

    try:

        return jsonify({
            "success": True,
            "resultat": lancer_worker_pdf(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_orchestration_reelle.route("/api/v3/orchestration/excel")
def api_orchestration_excel():

    try:

        return jsonify({
            "success": True,
            "resultat": lancer_worker_excel(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


