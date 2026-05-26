from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from services_v3.onboarding.onboarding_service import (
    onboard_new_client
)

from schemas_v3.api_response import success_response


bp_onboarding = Blueprint(
    "bp_onboarding",
    __name__
)


@bp_onboarding.route("/onboarding/client")
@login_required
@permission_required("ACCESS_ECRITURES")
def onboarding_client():

    return render_template(
        "onboarding_client_v3.html"
    )


@bp_onboarding.route(
    "/api/v3/onboarding/client",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_onboarding_client():

    data = request.json or {}

    result = onboard_new_client(data)

    return jsonify(
        success_response(result)
    )


