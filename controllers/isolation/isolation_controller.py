from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.isolation.isolation_service import (
    get_isolation_dashboard
)


bp_isolation = Blueprint(
    "bp_isolation",
    __name__
)


@bp_isolation.route("/isolation")
@login_required
@permission_required("ACCESS_ECRITURES")
def isolation_page():

    return render_template(
        "isolation_v3.html"
    )


@bp_isolation.route("/api/v3/isolation")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_isolation_dashboard():

    result = get_isolation_dashboard()

    return jsonify(
        success_response(result)
    )


