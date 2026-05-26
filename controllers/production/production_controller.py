from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response

from services_v3.production.production_service import (
    get_production_dashboard
)


bp_production = Blueprint(
    "bp_production",
    __name__
)


@bp_production.route("/production")
@login_required
@permission_required("ACCESS_ECRITURES")
def production_page():

    return render_template(
        "production_dashboard_v3.html"
    )


@bp_production.route("/api/v3/production")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_production_dashboard():

    result = get_production_dashboard()

    return jsonify(
        success_response(result)
    )

