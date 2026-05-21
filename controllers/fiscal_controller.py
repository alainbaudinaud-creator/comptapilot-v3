
import sqlite3
from pathlib import Path

from flask import Blueprint
from flask import render_template

from services.ia_fiscale_service import analyse_fiscale
from services.tva_service import generer_tva
from services.liasse_service import generer_liasse

bp_fiscal = Blueprint("fiscal", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_fiscal.route("/fiscal")
def fiscal():

    analyse_fiscale()
    generer_tva()
    generer_liasse()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    stats = {}

    tables = [
        "fec_imports",
        "ocr_factures",
        "tva_auto",
        "liasses_auto",
        "workflow_cabinet",
        "notifications_auto"
    ]

    for t in tables:
        stats[t] = cur.execute(
            f"SELECT COUNT(*) FROM {t}"
        ).fetchone()[0]

    con.close()

    return render_template(
        "cabinet/fiscal.html",
        stats=stats
    )
