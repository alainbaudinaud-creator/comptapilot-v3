
import sqlite3
from pathlib import Path
from flask import Blueprint, render_template

from services.ia_fiscale_service import analyser_risque_fiscal

bp_erp_premium = Blueprint("erp_premium", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_erp_premium.route("/erp-premium")
def erp_premium():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    stats = {}

    tables = [
        "notifications_centre",
        "timeline_dossiers",
        "workflow_taches",
        "rapprochements_bancaires",
        "imports_documents",
        "mail_queue"
    ]

    for t in tables:
        try:
            stats[t] = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        except:
            stats[t] = 0

    ia = analyser_risque_fiscal()

    con.close()

    return render_template(
        "cabinet/erp_premium.html",
        stats=stats,
        ia=ia
    )
