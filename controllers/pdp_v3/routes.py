from flask import Blueprint, render_template, jsonify

import sqlite3
from pathlib import Path

from services.pdp_v3.workflow_service import get_workflows
from services.pdp_v3.supervision_service import get_supervision_stats
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
        "mode": "lecture_seule",
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

@bp_pdp_v3.route("/api/pdp-v3/journal-technique")
def api_pdp_v3_journal_technique():

    db = Path("/app/db.sqlite")

    events = []

    try:

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row

        cur = con.cursor()

        rows = cur.execute("""
            SELECT *
            FROM journal_technique_pdp_v3
            ORDER BY id DESC
            LIMIT 50
        """).fetchall()

        events = [dict(row) for row in rows]

        con.close()

    except Exception as e:
        print("PDP V3 JOURNAL API WARNING:", e)

    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "journal": events,
        "count": len(events)
    })
