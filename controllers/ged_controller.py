
import sqlite3
from pathlib import Path

from flask import Blueprint
from flask import render_template

from services.ged_service import (
    ajouter_document,
    importer_fec,
    analyse_ocr
)

bp_ged = Blueprint("ged", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_ged.route("/ged")
def ged():

    ajouter_document(
        "IFG SOLUTIONS",
        "PDF",
        "bilan.pdf"
    )

    importer_fec(
        "IFG SOLUTIONS",
        "fec_2025.txt"
    )

    analyse_ocr(
        "facture_edf.pdf"
    )

    con = sqlite3.connect(DB)
    cur = con.cursor()

    stats = {}

    tables = [
        "documents_clients",
        "imports_fec_reels",
        "ocr_analyse"
    ]

    for t in tables:

        stats[t] = cur.execute(
            f"SELECT COUNT(*) FROM {t}"
        ).fetchone()[0]

    con.close()

    return render_template(
        "cabinet/ged.html",
        stats=stats
    )
