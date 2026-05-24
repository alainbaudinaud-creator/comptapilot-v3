from flask import Blueprint
from flask import render_template
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.relances.relances_service import (
    get_relances_center,
    generate_relances_from_alerts,
    send_relance
)


bp_relances = Blueprint(
    "bp_relances",
    __name__
)


@bp_relances.route("/relances")
@login_required
@permission_required("ACCESS_ECRITURES")
def relances_page():

    return render_template(
        "relances_client_v3.html"
    )


@bp_relances.route("/api/v3/relances")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_relances_center():

    result = get_relances_center()

    return jsonify(
        success_response(result)
    )


@bp_relances.route(
    "/api/v3/relances/generate-from-alerts",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_generate_relances_from_alerts():

    result = generate_relances_from_alerts()

    return jsonify(
        success_response(result)
    )


@bp_relances.route(
    "/api/v3/relances/<int:relance_id>/send",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_send_relance(relance_id):

    result = send_relance(relance_id)

    return jsonify(
        success_response(result)
    )
