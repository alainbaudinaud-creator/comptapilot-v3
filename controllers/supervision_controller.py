import sqlite3
from pathlib import Path
from flask import Blueprint, render_template

bp_supervision = Blueprint("supervision", __name__)

ROOT = Path("/app")
DB = ROOT / "db.sqlite"

@bp_supervision.route("/supervision")
def supervision():
    stats = {
        "mails": 0,
        "events": 0,
        "notifications": 0
    }

    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()

        tables = {
            "mails": "mail_queue",
            "events": "supervision_events",
            "notifications": "notifications_realtime"
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
        print("SUPERVISION WARNING:", e)

    return render_template(
        "supervision/index.html",
        mails=stats["mails"],
        events=stats["events"],
        notifications=stats["notifications"]
    )


