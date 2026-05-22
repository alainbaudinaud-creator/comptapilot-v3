import sqlite3
from pathlib import Path

from flask import Blueprint
from flask import render_template

bp_ged = Blueprint("ged", __name__)

ROOT = Path("/app")
DB = ROOT / "db.sqlite"

@bp_ged.route("/ged")
def ged():

    stats = {
        "documents_clients": 0,
        "imports_fec_reels": 0,
        "ocr_analyse": 0
    }

    try:

        con = sqlite3.connect(DB)
        cur = con.cursor()

        tables = [
            "documents_clients",
            "imports_fec_reels",
            "ocr_analyse"
        ]

        for t in tables:

            try:
                stats[t] = cur.execute(
                    f"SELECT COUNT(*) FROM {t}"
                ).fetchone()[0]

            except Exception:
                stats[t] = 0

        con.close()

    except Exception as e:
        print("GED WARNING:", e)

    return render_template(
        "cabinet/ged.html",
        stats=stats
    )
