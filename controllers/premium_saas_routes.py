from flask import Blueprint, render_template
from sqlalchemy import text

premium_saas = Blueprint("premium_saas", __name__)

def fetch_all_safe(query):
    try:
        from database import engine
        with engine.connect() as conn:
            return conn.execute(text(query)).mappings().all()
    except Exception as e:
        print("premium_saas error:", e)
        return []

@premium_saas.route("/centre-fiscal")
def centre_fiscal_premium():
    notifications = fetch_all_safe("""
        SELECT * FROM notifications_workflow
        ORDER BY created_at DESC
        LIMIT 20
    """)
    immobilisations = fetch_all_safe("""
        SELECT * FROM immobilisations
        ORDER BY created_at DESC
        LIMIT 20
    """)
    rapprochements = fetch_all_safe("""
        SELECT * FROM rapprochements_bancaires
        ORDER BY created_at DESC
        LIMIT 20
    """)
    return render_template(
        "centre_fiscal.html",
        notifications=notifications,
        immobilisations=immobilisations,
        rapprochements=rapprochements
    )

@premium_saas.route("/immobilisations")
def immobilisations_premium():
    immobilisations = fetch_all_safe("""
        SELECT * FROM immobilisations
        ORDER BY created_at DESC
        LIMIT 50
    """)
    return render_template("immobilisations.html", immobilisations=immobilisations)

@premium_saas.route("/rapprochement-bancaire")
def rapprochement_bancaire_premium():
    rapprochements = fetch_all_safe("""
        SELECT * FROM rapprochements_bancaires
        ORDER BY date_operation DESC NULLS LAST, created_at DESC
        LIMIT 50
    """)
    return render_template("rapprochement_bancaire.html", rapprochements=rapprochements)

@premium_saas.route("/workflow-cabinet")
def workflow_cabinet_premium():
    taches = fetch_all_safe("""
        SELECT
            t.id,
            t.titre,
            t.module,
            t.statut,
            t.priorite,
            c.nom AS assigne_a,
            t.echeance
        FROM cabinet_workflow_taches t
        LEFT JOIN cabinet_collaborateurs c ON c.id = t.assigne_a
        ORDER BY t.echeance NULLS LAST, t.created_at DESC
    """)
    return render_template("workflow_cabinet_premium.html", taches=taches)
