from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response

from services_v3.validation.validation_service import (
    get_validation_queue,
    validate_precompta,
    reject_precompta
)

from services_v3.ecritures.ecriture_service import (
    convert_precompta_to_ecriture
)


bp_validation = Blueprint(
    "bp_validation",
    __name__
)


@bp_validation.route("/validation/precompta")
@login_required
@permission_required("ACCESS_ECRITURES")
def validation_precompta_page():

    return render_template(
        "validation_precompta_v3.html"
    )


@bp_validation.route("/api/v3/validation/precompta")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_validation_precompta_queue():

    result = get_validation_queue()

    return jsonify(
        success_response(result)
    )


@bp_validation.route(
    "/api/v3/validation/precompta/<int:precompta_id>/validate",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_validate_precompta(precompta_id):

    data = request.json or {}

    result = validate_precompta(
        precompta_id,
        data
    )

    return jsonify(
        success_response(result)
    )


@bp_validation.route(
    "/api/v3/validation/precompta/<int:precompta_id>/reject",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_reject_precompta(precompta_id):

    data = request.json or {}

    result = reject_precompta(
        precompta_id,
        data
    )

    return jsonify(
        success_response(result)
    )


@bp_validation.route(
    "/api/v3/validation/precompta/<int:precompta_id>/convert-ecriture",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_convert_precompta_to_ecriture(precompta_id):

    result = convert_precompta_to_ecriture(precompta_id)

    return jsonify(
        success_response(result)
    )

