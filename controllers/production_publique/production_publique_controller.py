from flask import Blueprint, jsonify
from services.production_publique_service import (
    initialiser_production_publique,
    dashboard_production_publique,
    simulation_autoscaling,
    simulation_socketio,
    simulation_mobile,
)

bp_production_publique = Blueprint(
    "production_publique",
    __name__
)


@bp_production_publique.route("/api/v3/production-publique/dashboard")
def api_dashboard_public():

    try:

        initialiser_production_publique()

        return jsonify({
            "success": True,
            "module": "production_publique_v3",
            "data": dashboard_production_publique(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_production_publique.route("/api/v3/production-publique/autoscaling")
def api_autoscaling():

    return jsonify({
        "success": True,
        "resultat": simulation_autoscaling(),
    })


@bp_production_publique.route("/api/v3/production-publique/socketio")
def api_socketio():

    return jsonify({
        "success": True,
        "resultat": simulation_socketio(),
    })


@bp_production_publique.route("/api/v3/production-publique/mobile")
def api_mobile():

    return jsonify({
        "success": True,
        "resultat": simulation_mobile(),
    })


