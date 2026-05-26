
from flask import Blueprint, jsonify
from services.ia_erp_service import analyser_comptabilite

bp_ia_controller = Blueprint("ia_controller", __name__)

@bp_ia_controller.route("/ia/analyse")
def ia_analyse():
    return jsonify(analyser_comptabilite())


