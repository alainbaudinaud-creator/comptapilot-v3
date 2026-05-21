
import sqlite3
from pathlib import Path
from flask import Blueprint, render_template

bp_supervision = Blueprint("supervision", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_supervision.route("/supervision")
def supervision():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    mails = cur.execute("""
        SELECT COUNT(*)
        FROM mail_queue
    """).fetchone()[0]

    events = cur.execute("""
        SELECT COUNT(*)
        FROM supervision_events
    """).fetchone()[0]

    notifications = cur.execute("""
        SELECT COUNT(*)
        FROM notifications_realtime
    """).fetchone()[0]

    con.close()

    return render_template(
        "supervision/index.html",
        mails=mails,
        events=events,
        notifications=notifications
    )
