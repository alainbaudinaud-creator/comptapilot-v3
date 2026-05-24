from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.security.security_service import (
    get_security_dashboard
)


bp_security = Blueprint(
    "bp_security",
    __name__
)


@bp_security.route("/security")
@login_required
@permission_required("ACCESS_ECRITURES")
def security_page():

    return render_template(
        "security_roles_v3.html"
    )


@bp_security.route("/api/v3/security")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_security_dashboard():

    result = get_security_dashboard()

    return jsonify(
        success_response(result)
    )
