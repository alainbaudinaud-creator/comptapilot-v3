from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from services_v3.client_portal.client_portal_service import (
    get_client_portal_dashboard
)

from services_v3.documents.document_upload_service import (
    upload_client_document
)

from services_v3.ocr.ocr_service import (
    run_ocr_on_document
)

from services_v3.precompta_ai.precompta_ai_service import (
    generate_precompta_from_document
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


@bp_client_portal.route(
    "/api/v3/client-portal/upload",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_upload_client_document():

    societe_id = request.form.get("societe_id", 1)
    file = request.files.get("file")

    result = upload_client_document(
        file=file,
        societe_id=societe_id
    )

    return jsonify(
        success_response(result)
    )


@bp_client_portal.route(
    "/api/v3/client-portal/document/<int:document_id>/ocr",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_run_document_ocr(document_id):

    result = run_ocr_on_document(document_id)

    return jsonify(
        success_response(result)
    )


@bp_client_portal.route(
    "/api/v3/client-portal/document/<int:document_id>/precompta",
    methods=["POST"]
)
@login_required
@permission_required("ACCESS_ECRITURES")
def api_generate_document_precompta(document_id):

    result = generate_precompta_from_document(document_id)

    return jsonify(
        success_response(result)
    )


