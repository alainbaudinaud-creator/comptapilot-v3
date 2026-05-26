from flask import Blueprint, jsonify
from services.production_premium_service import (
    initialiser_production_premium,
    stats_production_premium,
)

bp_production_premium = Blueprint("production_premium", __name__)


@bp_production_premium.route("/api/v3/production-premium")
def api_production_premium():

    try:

        initialiser_production_premium()

        return jsonify({
            "success": True,
            "module": "production_premium_v3",
            "stats": stats_production_premium(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


