from flask import Blueprint, render_template, jsonify

import sqlite3
from pathlib import Path

from services.pdp_v3.workflow_service import get_workflows
from services.pdp_v3.supervision_service import get_supervision_stats
from services.pdp_v3.supervision_live_service import charger_supervision_temps_reel
from services.pdp_v3.depot_service import simuler_depot_facture, deposer_facture_pdp

bp_pdp_v3 = Blueprint("pdp_v3", __name__)

DB = Path("/app/db.sqlite")

@bp_pdp_v3.route("/pdp-v3")
def pdp_v3():
    return render_template("pdp_v3/index.html")

@bp_pdp_v3.route("/pdp-v3/workflow")
def pdp_v3_workflow():
    workflows = get_workflows()
    return render_template("pdp_v3/workflow.html", workflows=workflows)

@bp_pdp_v3.route("/pdp-v3/supervision")
def pdp_v3_supervision():
    stats = get_supervision_stats()
    return render_template("pdp_v3/supervision.html", stats=stats)

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
    result = simuler_depot_facture(facture_id)
    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "action": "simulation_depot",
        "result": result
    })

@bp_pdp_v3.route("/api/pdp-v3/deposer-facture/<int:facture_id>", methods=["GET", "POST"])
def api_pdp_v3_deposer_facture(facture_id):
    result = deposer_facture_pdp(facture_id)
    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "action": "depot_facture_controle",
        "result": result
    })

@bp_pdp_v3.route("/api/pdp-v3/live")
def api_pdp_v3_live():
    data = charger_supervision_temps_reel()
    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "live": data
    })

@bp_pdp_v3.route("/api/pdp-v3/journal-technique")
def api_pdp_v3_journal_technique():
    events = []

    try:
        con = sqlite3.connect(DB)
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

@bp_pdp_v3.route("/api/pdp-v3/archives")
def api_pdp_v3_archives():
    archives = []

    try:
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        rows = cur.execute("""
            SELECT *
            FROM archives_probatoires_pdp_v3
            ORDER BY id DESC
            LIMIT 50
        """).fetchall()
        archives = [dict(row) for row in rows]
        con.close()
    except Exception as e:
        print("PDP V3 ARCHIVES API WARNING:", e)

    return jsonify({
        "application": "ComptaPilot V3",
        "module": "PDP V3",
        "archives": archives,
        "count": len(archives)
    })
