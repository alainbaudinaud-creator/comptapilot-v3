from flask import Blueprint, render_template, jsonify

from services.pdp_v3.workflow_service import get_workflows
from services.pdp_v3.supervision_service import get_supervision_stats

bp_pdp_v3 = Blueprint("pdp_v3", __name__)

@bp_pdp_v3.route("/pdp-v3")
def pdp_v3():
    return render_template("pdp_v3/index.html")

@bp_pdp_v3.route("/pdp-v3/workflow")
def workflow_pdp_v3():

    workflows = get_workflows()

    return render_template(
        "pdp_v3/workflow.html",
        workflows=workflows
    )

@bp_pdp_v3.route("/pdp-v3/supervision")
def supervision_pdp_v3():

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
        "mode": "lecture_seule",
        "count": len(workflows),
        "workflows": workflows
    })
