from flask import Blueprint, jsonify
from services.integrations_production_service import (
    initialiser_integrations_production,
    dashboard_integrations_production,
)

bp_integrations_production = Blueprint("integrations_production", __name__)


@bp_integrations_production.route("/api/v3/integrations-production")
def api_integrations_production():

    try:
        initialiser_integrations_production()

        return jsonify({
            "success": True,
            "module": "integrations_production_v3",
            "data": dashboard_integrations_production(),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


