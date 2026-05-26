
import sqlite3
from pathlib import Path

from flask import Blueprint, render_template

from services.kpi_service import generer_kpi
from services.ia_anomalies_service import detecter_anomalies

bp_erp_advanced = Blueprint("erp_advanced", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_erp_advanced.route("/erp-advanced")
def erp_advanced():

    detecter_anomalies()

    kpi = generer_kpi()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    stats = {}

    tables = [
        "collaborateurs",
        "dossiers_cabinets",
        "imports_fec_excel",
        "ocr_factures",
        "ia_anomalies",
        "workflow_taches",
    ]

    for t in tables:
        try:
            stats[t] = cur.execute(
                f"SELECT COUNT(*) FROM {t}"
            ).fetchone()[0]
        except:
            stats[t] = 0

    con.close()

    return render_template(
        "cabinet/erp_advanced.html",
        stats=stats,
        kpi=kpi
    )


