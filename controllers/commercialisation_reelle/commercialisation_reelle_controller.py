from flask import Blueprint, jsonify
from services.commercialisation_reelle_service import (
    initialiser_commercialisation,
    dashboard_commercial,
    simulation_stripe,
    onboarding_client,
)

bp_commercialisation_reelle = Blueprint(
    "commercialisation_reelle",
    __name__
)


@bp_commercialisation_reelle.route("/api/v3/commercial/dashboard")
def api_commercial_dashboard():

    try:

        initialiser_commercialisation()

        return jsonify({
            "success": True,
            "module": "commercialisation_reelle_v3",
            "data": dashboard_commercial(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_commercialisation_reelle.route("/api/v3/commercial/stripe")
def api_stripe():

    return jsonify({
        "success": True,
        "resultat": simulation_stripe(),
    })


@bp_commercialisation_reelle.route("/api/v3/commercial/onboarding")
def api_onboarding():

    return jsonify({
        "success": True,
        "resultat": onboarding_client(),
    })


