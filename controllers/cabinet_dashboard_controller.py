
import sqlite3
from pathlib import Path
from flask import Blueprint, render_template

bp_cabinet_dashboard = Blueprint("cabinet_dashboard", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_cabinet_dashboard.route("/cabinet")
def cabinet_dashboard():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    data = {}

    tables = [
        "workflow_taches",
        "ia_alertes",
        "mail_queue",
        "depot_fiscal_auto",
        "ecritures",
        "plan_comptable"
    ]

    for t in tables:
        try:
            data[t] = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        except:
            data[t] = 0

    con.close()

    return render_template(
        "cabinet/dashboard.html",
        data=data
    )
