from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from services_v3.client_portal.client_portal_service import (
    get_client_portal_dashboard
)

from schemas_v3.api_response import success_response


bp_client_portal = Blueprint(
    "bp_client_portal",
    __name__
)


@bp_client_portal.route("/client-portal")
@login_required
@permission_required("ACCESS_ECRITURES")
def client_portal_home():

    return render_template(
        "client_portal_v3.html"
    )


@bp_client_portal.route("/api/v3/client-portal")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_client_portal():

    societe_id = request.args.get("societe_id", 1)

    result = get_client_portal_dashboard(societe_id)

    return jsonify(
        success_response(result)
    )
