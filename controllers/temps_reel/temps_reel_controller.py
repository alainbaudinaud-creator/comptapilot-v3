from flask import Blueprint, jsonify
from services.temps_reel_service import (
    initialiser_temps_reel,
    liste_notifications,
    stats_temps_reel,
)

bp_temps_reel = Blueprint("temps_reel", __name__)


@bp_temps_reel.route("/api/v3/live/stats")
def api_live_stats():
    initialiser_temps_reel()

    return jsonify({
        "success": True,
        "module": "temps_reel_v3",
        "stats": stats_temps_reel(),
    })


@bp_temps_reel.route("/api/v3/live/notifications")
def api_live_notifications():
    initialiser_temps_reel()

    return jsonify({
        "success": True,
        "notifications": liste_notifications(),
    })


