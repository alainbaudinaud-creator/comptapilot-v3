import sqlite3
from pathlib import Path
from flask import Blueprint, render_template

bp_production = Blueprint("production", __name__)

ROOT = Path("/app")
DB = ROOT / "db.sqlite"

@bp_production.route("/production")
def production():
    data = {}

    tables = [
        "mail_queue",
        "depot_fiscal_auto",
        "signatures_electroniques",
        "supervision_realtime",
        "portail_clients",
    ]

    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()

        for table in tables:
            try:
                data[table] = cur.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]
            except Exception:
                data[table] = 0

        con.close()

    except Exception as e:
        print("PRODUCTION WARNING:", e)
        for table in tables:
            data[table] = 0

    return render_template("production/index.html", data=data)

