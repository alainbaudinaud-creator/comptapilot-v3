from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.audit.audit_service import (
    get_audit_dashboard
)


bp_audit_v3 = Blueprint(
    "bp_audit_v3",
    __name__
)


@bp_audit_v3.route("/audit-v3")
@login_required
@permission_required("ACCESS_ECRITURES")
def audit_v3_page():

    return render_template(
        "audit_dashboard_v3.html"
    )


@bp_audit_v3.route("/api/v3/audit-dashboard")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_audit_v3_dashboard():

    result = get_audit_dashboard()

    return jsonify(
        success_response(result)
    )


