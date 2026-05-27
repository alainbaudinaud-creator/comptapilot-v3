from flask import Blueprint, jsonify
from sqlalchemy import text
from database import engine

bp_public_kpi = Blueprint("public_kpi", __name__)

@bp_public_kpi.route("/public/kpi")
def public_kpi():
    data = {
        "ca": 12500,
        "charges": 1800,
        "resultat": 10700,
        "tva_a_payer": 2500,
        "nb_ecritures": 6,
        "equilibre_comptable": 0,
        "marge": 10700,
        "ratio_marge": 85.6,
        "statut": "OK"
    }

    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ecritures (
                    id SERIAL PRIMARY KEY,
                    journal VARCHAR(20),
                    compte VARCHAR(20),
                    libelle TEXT,
                    debit NUMERIC(14,2) DEFAULT 0,
                    credit NUMERIC(14,2) DEFAULT 0,
                    date_ecriture DATE DEFAULT CURRENT_DATE
                )
            """))

            nb = conn.execute(text("SELECT COUNT(*) FROM ecritures")).scalar() or 0

            if int(nb) == 0:
                conn.execute(text("""
                    INSERT INTO ecritures (journal, compte, libelle, debit, credit)
                    VALUES
                    ('VE','706000','Prestations cabinet',0,12500),
                    ('VE','445700','TVA collectée',0,2500),
                    ('AC','606000','Achats et charges',1800,0),
                    ('AC','445660','TVA déductible',360,0),
                    ('BQ','512000','Banque',15000,0),
                    ('OD','401000','Dette fournisseur',0,2160)
                """))

            total_debit = conn.execute(text("SELECT COALESCE(SUM(debit),0) FROM ecritures")).scalar() or 0
            total_credit = conn.execute(text("SELECT COALESCE(SUM(credit),0) FROM ecritures")).scalar() or 0
            nb = conn.execute(text("SELECT COUNT(*) FROM ecritures")).scalar() or 0
            ca = conn.execute(text("SELECT COALESCE(SUM(credit-debit),0) FROM ecritures WHERE compte LIKE '7%'")).scalar() or 0
            charges = conn.execute(text("SELECT COALESCE(SUM(debit-credit),0) FROM ecritures WHERE compte LIKE '6%'")).scalar() or 0
            tva = conn.execute(text("SELECT COALESCE(SUM(credit-debit),0) FROM ecritures WHERE compte LIKE '4457%'")).scalar() or 0
            resultat = float(ca) - float(charges)

            data.update({
                "ca": float(ca),
                "charges": float(charges),
                "resultat": resultat,
                "tva_a_payer": float(tva),
                "nb_ecritures": int(nb),
                "equilibre_comptable": float(total_debit) - float(total_credit),
                "marge": resultat,
                "ratio_marge": round((resultat / float(ca)) * 100, 2) if float(ca) else 0,
                "statut": "OK"
            })

    except Exception as e:
        data["statut"] = "ERREUR"
        data["error"] = str(e)

    return jsonify({"success": True, "data": data})
