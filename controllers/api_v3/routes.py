from flask import Blueprint, jsonify

from controllers.auth import login_required
from services.permission_service import permission_required

from schemas_v3.api_response import success_response
from schemas_v3.api_handlers import api_safe

from services_v3.kpi.kpi_service import get_kpi_financiers
from services_v3.tva.tva_service import get_tva_estimee
from services_v3.audit.audit_service import get_audit_comptable
from services_v3.supervision.supervision_service import get_supervision_comptable


api_v3_routes = Blueprint("api_v3_routes", __name__)


@api_v3_routes.route("/api/v3/kpi")
@login_required
@permission_required("ACCESS_ECRITURES")
@api_safe
def api_v3_kpi():

    return jsonify(
        success_response(
            get_kpi_financiers()
        )
    )


@api_v3_routes.route("/api/v3/tva")
@login_required
@permission_required("ACCESS_ECRITURES")
@api_safe
def api_v3_tva():

    return jsonify(
        success_response(
            get_tva_estimee()
        )
    )


@api_v3_routes.route("/api/v3/audit")
@login_required
@permission_required("ACCESS_ECRITURES")
@api_safe
def api_v3_audit():

    return jsonify(
        success_response(
            get_audit_comptable()
        )
    )


@api_v3_routes.route("/api/v3/supervision")
@login_required
@permission_required("ACCESS_ECRITURES")
@api_safe
def api_v3_supervision():

    return jsonify(
        success_response(
            get_supervision_comptable()
        )
    )
