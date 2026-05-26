from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response

from services_v3.notifications.notifications_service import (
    get_notifications_center,
    notify_from_alerts,
    read_notification
)


bp_notifications = Blueprint(
    "bp_notifications",
    __name__
)


@bp_notifications.route("/notifications")
@login_required
@permission_required("ACCESS_ECRITURES")
def notifications_page():

    return render_template(
        "notifications_center_v3.html"
    )


@bp_notifications.route("/api/v3/notifications")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_notifications_center():

    result = get_notifications_center()

    return jsonify(
        success_response(result)
    )


@bp_notifications.route(
    "/api/v3/notifications/generate-from-alerts",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_generate_notifications_from_alerts():

    result = notify_from_alerts()

    return jsonify(
        success_response(result)
    )


@bp_notifications.route(
    "/api/v3/notifications/<int:notification_id>/read",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_read_notification(notification_id):

    result = read_notification(notification_id)

    return jsonify(
        success_response(result)
    )

