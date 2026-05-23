from flask import Blueprint, jsonify

from services_v3.kpi.kpi_service import get_kpi_financiers
from services_v3.tva.tva_service import get_tva_estimee
from services_v3.audit.audit_service import get_audit_comptable
from services_v3.supervision.supervision_service import get_supervision_comptable


api_v3_routes = Blueprint("api_v3_routes", __name__)


@api_v3_routes.route("/api/v3/kpi")
def api_v3_kpi():

    return jsonify(get_kpi_financiers())


@api_v3_routes.route("/api/v3/tva")
def api_v3_tva():

    return jsonify(get_tva_estimee())


@api_v3_routes.route("/api/v3/audit")
def api_v3_audit():

    return jsonify(get_audit_comptable())


@api_v3_routes.route("/api/v3/supervision")
def api_v3_supervision():

    return jsonify(get_supervision_comptable())
