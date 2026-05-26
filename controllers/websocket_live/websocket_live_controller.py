from flask import Blueprint, jsonify
from services.websocket_live_service import (
    initialiser_websocket_live,
    stats_websocket_live,
    generer_event_live,
)

bp_websocket_live = Blueprint("websocket_live", __name__)


@bp_websocket_live.route("/api/v3/live/websocket/stats")
def api_websocket_stats():

    initialiser_websocket_live()

    return jsonify({
        "success": True,
        "module": "websocket_live_v3",
        "stats": stats_websocket_live(),
    })


@bp_websocket_live.route("/api/v3/live/websocket/push")
def api_websocket_push():

    initialiser_websocket_live()

    payload = generer_event_live()

    return jsonify({
        "success": True,
        "event": payload,
    })

