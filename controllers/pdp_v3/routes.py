from flask import Blueprint, render_template
import sqlite3
from pathlib import Path

bp_pdp_v3 = Blueprint("pdp_v3", __name__)

ROOT = Path("/app")
DB = ROOT / "db.sqlite"

@bp_pdp_v3.route("/pdp-v3")
def pdp_v3():
    return render_template("pdp_v3/index.html")

@bp_pdp_v3.route("/pdp-v3/workflow")
def workflow_pdp_v3():
    workflows = []

    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()

        try:
            workflows = cur.execute("""
                SELECT id, facture_id, numero, sens, statut, canal, accuse_reception, date_action, detail
                FROM workflow_factures_pdp
                ORDER BY id DESC
            """).fetchall()
        except Exception:
            workflows = []

        con.close()

    except Exception as e:
        print("PDP V3 WORKFLOW WARNING:", e)

    return render_template(
        "pdp_v3/workflow.html",
        workflows=workflows
    )

@bp_pdp_v3.route("/pdp-v3/supervision")
def supervision_pdp_v3():

    stats = {
        "workflows": 0,
        "archives": 0,
        "journal": 0
    }

    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()

        tables = {
            "workflows": "workflow_factures_pdp",
            "archives": "archives_probatoires",
            "journal": "journal_technique_pdp_v2"
        }

        for key, table in tables.items():
            try:
                stats[key] = cur.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]
            except Exception:
                stats[key] = 0

        con.close()

    except Exception as e:
        print("PDP V3 SUPERVISION WARNING:", e)

    return render_template(
        "pdp_v3/supervision.html",
        stats=stats
    )
