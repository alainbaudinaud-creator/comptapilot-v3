from flask import Blueprint, jsonify
from services.integrations_reelles_service import (
    initialiser_integrations_reelles,
    stats_integrations_reelles,
)

bp_integrations_reelles = Blueprint("integrations_reelles", __name__)


@bp_integrations_reelles.route("/api/v3/integrations")
def api_integrations():

    try:
        initialiser_integrations_reelles()

        return jsonify({
            "success": True,
            "module": "integrations_reelles_v3",
            "stats": stats_integrations_reelles(),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "module": "integrations_reelles_v3",
            "error": str(e),
        }), 500

