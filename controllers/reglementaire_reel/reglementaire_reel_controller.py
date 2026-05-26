from flask import Blueprint, jsonify
from services.reglementaire_reel_service import (
    initialiser_reglementaire,
    dashboard_reglementaire,
    simulation_dsp2,
    simulation_peppol,
    moteur_tva_avance,
)

bp_reglementaire_reel = Blueprint("reglementaire_reel", __name__)


@bp_reglementaire_reel.route("/api/v3/reglementaire/dashboard")
def api_reglementaire_dashboard():

    try:

        initialiser_reglementaire()

        return jsonify({
            "success": True,
            "module": "reglementaire_reel_v3",
            "data": dashboard_reglementaire(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_reglementaire_reel.route("/api/v3/reglementaire/dsp2")
def api_dsp2():

    return jsonify({
        "success": True,
        "resultat": simulation_dsp2(),
    })


@bp_reglementaire_reel.route("/api/v3/reglementaire/peppol")
def api_peppol():

    return jsonify({
        "success": True,
        "resultat": simulation_peppol(),
    })


@bp_reglementaire_reel.route("/api/v3/reglementaire/tva")
def api_tva():

    return jsonify({
        "success": True,
        "resultat": moteur_tva_avance(),
    })


