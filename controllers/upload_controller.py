
import sqlite3
from pathlib import Path

from flask import Blueprint
from flask import render_template

from services.ocr_service import analyser_facture

bp_upload = Blueprint("upload", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_upload.route("/uploads")
def uploads():

    analyser_facture(
        "IFG SOLUTIONS",
        "facture_orange.pdf"
    )

    con = sqlite3.connect(DB)
    cur = con.cursor()

    stats = {}

    tables = [
        "pieces_comptables",
        "ecritures_auto"
    ]

    for t in tables:

        stats[t] = cur.execute(
            f"SELECT COUNT(*) FROM {t}"
        ).fetchone()[0]

    con.close()

    return render_template(
        "cabinet/uploads.html",
        stats=stats
    )


