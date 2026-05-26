from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.monitoring.monitoring_service import (
    get_system_health
)


bp_monitoring = Blueprint(
    "bp_monitoring",
    __name__
)


@bp_monitoring.route("/system-health")
@login_required
@permission_required("ACCESS_EXPORTS")
def system_health_page():

    return render_template(
        "system_health_v3.html"
    )


@bp_monitoring.route("/api/v3/system-health")
@login_required
@permission_required("ACCESS_EXPORTS")
def api_system_health():

    result = get_system_health()

    return jsonify(
        success_response(result)
    )

