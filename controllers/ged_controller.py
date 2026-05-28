from flask import Blueprint, render_template
from sqlalchemy import text
from database import engine

bp_ged = Blueprint("ged", __name__)

@bp_ged.route("/ged")
def ged():

    stats = {
        "documents_clients": 0,
        "imports_fec_reels": 0,
        "ocr_analyse": 0
    }

    try:

        with engine.begin() as conn:

            stats["documents_clients"] = conn.execute(text(
                "select count(*) from factures"
            )).scalar() or 0

            stats["imports_fec_reels"] = conn.execute(text(
                "select count(*) from ecritures_premium"
            )).scalar() or 0

            stats["ocr_analyse"] = conn.execute(text(
                "select count(*) from societes_clientes_premium"
            )).scalar() or 0

    except Exception as e:
        print("GED WARNING:", e)

    return render_template(
        "cabinet/ged.html",
        stats=stats
    )
