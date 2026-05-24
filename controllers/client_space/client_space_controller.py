from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.client_space.client_space_service import (
    get_client_space_dashboard
)


bp_client_space = Blueprint(
    "bp_client_space",
    __name__
)


@bp_client_space.route("/client-space")
@login_required
@permission_required("ACCESS_ECRITURES")
def client_space_page():

    return render_template(
        "client_space_v3.html"
    )


@bp_client_space.route("/api/v3/client-space")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_client_space_dashboard():

    societe_id = request.args.get(
        "societe_id",
        1
    )

    result = get_client_space_dashboard(
        societe_id=societe_id
    )

    return jsonify(
        success_response(result)
    )
