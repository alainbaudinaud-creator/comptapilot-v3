from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

from controllers.auth import login_required
from services.permission_service import permission_required
from schemas_v3.api_response import success_response

from services_v3.ged.ged_service import (
    get_ged_dashboard,
    classify_document,
    archive_ged_document
)


bp_ged = Blueprint(
    "bp_ged",
    __name__
)


@bp_ged.route("/ged")
@login_required
@permission_required("ACCESS_ECRITURES")
def ged_page():

    return render_template(
        "ged_v3.html"
    )


@bp_ged.route("/api/v3/ged")
@login_required
@permission_required("ACCESS_ECRITURES")
def api_ged_dashboard():

    result = get_ged_dashboard()

    return jsonify(
        success_response(result)
    )


@bp_ged.route(
    "/api/v3/ged/document/<int:document_id>/classify",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_classify_document(document_id):

    data = request.json or {}

    result = classify_document(
        document_id,
        data
    )

    return jsonify(
        success_response(result)
    )


@bp_ged.route(
    "/api/v3/ged/document/<int:document_id>/archive",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_archive_document(document_id):

    result = archive_ged_document(document_id)

    return jsonify(
        success_response(result)
    )

