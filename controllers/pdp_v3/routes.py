from flask import Blueprint, render_template, jsonify

from services.pdp_v3.workflow_service import get_workflows
from services.pdp_v3.supervision_service import get_supervision_stats
from services.pdp_v3.supervision_live_service import charger_supervision_temps_reel
from services.pdp_v3.depot_service import simuler_depot_facture

bp_pdp_v3 = Blueprint("pdp_v3", __name__)

@bp_pdp_v3.route("/pdp-v3")
def pdp_v3():
    return render_template("pdp_v3/index.html")

@bp_pdp_v3.route("/pdp-v3/workflow")
def pdp_v3_workflow():

    workflows = get_workflows()

    return render_template(
        "pdp_v3/workflow.html",
        workflows=workflows
    )

@bp_pdp_v3.route("/pdp-v3/supervision")
def pdp_v3_supervision():

    stats = get_supervision_stats()

    return render_template(
        "pdp_v3/supervision.html",
        stats=stats
    )

@bp_pdp_v3.route("/api/pdp-v3/workflows")
def api_pdp_v3_workflows():

    workflows = get_workflows()

    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "count": len(workflows),
        "workflows": workflows
    })

@bp_pdp_v3.route("/api/pdp-v3/simuler-depot/<int:facture_id>", methods=["GET", "POST"])
def api_pdp_v3_simuler_depot(facture_id):

    workflow = simuler_depot_facture(facture_id)

    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "action": "simulation_depot",
        "workflow": workflow
    })

@bp_pdp_v3.route("/api/pdp-v3/live")
def api_pdp_v3_live():

    data = charger_supervision_temps_reel()

    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "live": data
    })
