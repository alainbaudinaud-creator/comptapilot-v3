from flask import Blueprint, jsonify
from services.go_live_service import (
    initialiser_go_live,
    dashboard_go_live,
    generer_rapport_lancement,
)

bp_go_live = Blueprint("go_live", __name__)


@bp_go_live.route("/api/v3/go-live/dashboard")
def api_go_live_dashboard():

    try:
        initialiser_go_live()

        return jsonify({
            "success": True,
            "module": "go_live_v3",
            "data": dashboard_go_live(),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_go_live.route("/api/v3/go-live/rapport")
def api_go_live_rapport():

    return jsonify({
        "success": True,
        "resultat": generer_rapport_lancement(),
    })
