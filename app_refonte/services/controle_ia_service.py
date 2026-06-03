import os
from sqlalchemy import create_engine, text


def db_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot"
    )


def calculer_controles_ia():

    resultat = {
        "score_risque": 0,
        "alertes": []
    }

    try:

        engine = create_engine(db_url(), pool_pre_ping=True)

        with engine.connect() as conn:

            comptes_attente = conn.execute(text("""
                SELECT COUNT(*)
                FROM ecritures_premium
                WHERE compte::text LIKE '471%'
                   OR compte::text LIKE '467%'
            """)).scalar() or 0

            libelles_vides = conn.execute(text("""
                SELECT COUNT(*)
                FROM ecritures_premium
                WHERE libelle IS NULL
                   OR TRIM(libelle)=''
            """)).scalar() or 0

            fournisseurs_debiteurs = conn.execute(text("""
                SELECT COUNT(*)
                FROM ecritures_premium
                WHERE compte::text LIKE '401%'
                  AND debit > credit
            """)).scalar() or 0

            clients_crediteurs = conn.execute(text("""
                SELECT COUNT(*)
                FROM ecritures_premium
                WHERE compte::text LIKE '411%'
                  AND credit > debit
            """)).scalar() or 0

        score = (
            comptes_attente * 5 +
            libelles_vides * 2 +
            fournisseurs_debiteurs * 3 +
            clients_crediteurs * 3
        )

        resultat["score_risque"] = min(score, 100)

        if comptes_attente:
            resultat["alertes"].append(
                f"{comptes_attente} écritures sur comptes d'attente"
            )

        if libelles_vides:
            resultat["alertes"].append(
                f"{libelles_vides} écritures sans libellé"
            )

        if fournisseurs_debiteurs:
            resultat["alertes"].append(
                f"{fournisseurs_debiteurs} fournisseurs débiteurs"
            )

        if clients_crediteurs:
            resultat["alertes"].append(
                f"{clients_crediteurs} clients créditeurs"
            )

    except Exception as e:

        resultat["erreur"] = str(e)

    return resultat
