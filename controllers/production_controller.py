
import sqlite3
from pathlib import Path
from flask import Blueprint, render_template

bp_production = Blueprint("production", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_production.route("/production")
def production():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    data = {}

    for table in [
        "mail_queue",
        "depot_fiscal_auto",
        "signatures_electroniques",
        "supervision_realtime",
        "portail_clients",
    ]:
        try:
            data[table] = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        except Exception:
            data[table] = 0

    con.close()
    return render_template("production/index.html", data=data)
