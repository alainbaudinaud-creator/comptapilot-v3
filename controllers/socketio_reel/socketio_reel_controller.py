from flask import Blueprint, jsonify, request
from services.socketio_reel_service import (
    initialiser_socketio_reel,
    stats_socketio_reel,
    push_dashboard_event,
    push_ocr_event,
)

bp_socketio_reel = Blueprint("socketio_reel", __name__)


@bp_socketio_reel.route("/api/v3/socketio/stats")
def socketio_stats():

    try:
        initialiser_socketio_reel()

        return jsonify({
            "success": True,
            "module": "socketio_reel_v3",
            "stats": stats_socketio_reel(),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "module": "socketio_reel_v3",
            "error": str(e),
        }), 500


@bp_socketio_reel.route("/api/v3/socketio/push-dashboard")
def socketio_push_dashboard():

    return jsonify({
        "success": True,
        "event": push_dashboard_event(),
    })


@bp_socketio_reel.route("/api/v3/socketio/push-ocr")
def socketio_push_ocr():

    filename = request.args.get("filename", "facture_live.pdf")

    return jsonify({
        "success": True,
        "event": push_ocr_event(filename),
    })
