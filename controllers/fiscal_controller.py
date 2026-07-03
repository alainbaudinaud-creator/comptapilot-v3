from flask import Blueprint, render_template
from sqlalchemy import text
from database import engine

from services.ia_fiscale_service import analyse_fiscale
from services.tva_service import generer_tva
from services.liasse_service import generer_liasse

bp_fiscal = Blueprint("fiscal", __name__)

@bp_fiscal.route("/fiscal")
def fiscal():

    try:
        analyse_fiscale()
    except:
        pass

    try:
        generer_tva()
    except:
        pass

    try:
        generer_liasse()
    except:
        pass

    stats = {}

    try:

        with engine.begin() as conn:

            stats["fec_imports"] = conn.execute(text(
                "select count(*) from ecritures_premium"
            )).scalar() or 0

            stats["ocr_factures"] = conn.execute(text(
                "select count(*) from factures"
            )).scalar() or 0

            stats["tva_auto"] = conn.execute(text(
                "select count(*) from societes_clientes_premium"
            )).scalar() or 0

            stats["liasses_auto"] = conn.execute(text(
                "select count(*) from immobilisations"
            )).scalar() or 0

            stats["workflow_cabinet"] = conn.execute(text(
                "select count(*) from cabinet_workflow_taches"
            )).scalar() or 0

            stats["notifications_auto"] = conn.execute(text(
                "select count(*) from notifications_workflow"
            )).scalar() or 0

    except Exception as e:
        print("FISCAL WARNING:", e)

    return render_template(
        "cabinet/fiscal.html",
        stats=stats
    )
