from flask import Blueprint, jsonify
from services.dashboard_financier_service import (
    initialiser_dashboard_financier,
    dashboard_financier_data,
)

bp_dashboard_financier = Blueprint("dashboard_financier", __name__)


@bp_dashboard_financier.route("/api/v3/dashboard-financier")
def api_dashboard_financier():

    try:

        initialiser_dashboard_financier()

        return jsonify({
            "success": True,
            "module": "dashboard_financier_v3",
            "data": dashboard_financier_data(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

