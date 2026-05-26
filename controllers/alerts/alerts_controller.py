from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response

from services_v3.alerts.alerts_service import (
    get_alerts_center
)


bp_alerts = Blueprint(
    "bp_alerts",
    __name__
)


@bp_alerts.route("/alerts")
@login_required
@permission_required("ACCESS_ECRITURES")
def alerts_page():

    return render_template(
        "alerts_center_v3.html"
    )


@bp_alerts.route("/api/v3/alerts")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_alerts_center():

    result = get_alerts_center()

    return jsonify(
        success_response(result)
    )


