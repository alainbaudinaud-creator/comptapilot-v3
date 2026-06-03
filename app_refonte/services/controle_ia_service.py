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
        "table_source": "lignes_ecritures_v3",
        "alertes": []
    }

    try:
        engine = create_engine(db_url(), pool_pre_ping=True)

        with engine.connect() as conn:
            comptes_attente = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE compte LIKE '471%'
                   OR compte LIKE '467%'
            """)).scalar() or 0

            libelles_vides = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE libelle IS NULL
                   OR TRIM(libelle) = ''
            """)).scalar() or 0

            fournisseurs_debiteurs = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE compte LIKE '401%'
                  AND COALESCE(debit,0) > COALESCE(credit,0)
            """)).scalar() or 0

            clients_crediteurs = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE compte LIKE '411%'
                  AND COALESCE(credit,0) > COALESCE(debit,0)
            """)).scalar() or 0

            lignes_sans_montant = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE COALESCE(debit,0) = 0
                  AND COALESCE(credit,0) = 0
            """)).scalar() or 0

        score = (
            comptes_attente * 5
            + libelles_vides * 2
            + fournisseurs_debiteurs * 3
            + clients_crediteurs * 3
            + lignes_sans_montant * 4
        )

        resultat["score_risque"] = min(score, 100)

        if comptes_attente:
            resultat["alertes"].append(f"{comptes_attente} lignes sur comptes d'attente 471/467")

        if libelles_vides:
            resultat["alertes"].append(f"{libelles_vides} lignes sans libellé")

        if fournisseurs_debiteurs:
            resultat["alertes"].append(f"{fournisseurs_debiteurs} fournisseurs débiteurs")

        if clients_crediteurs:
            resultat["alertes"].append(f"{clients_crediteurs} clients créditeurs")

        if lignes_sans_montant:
            resultat["alertes"].append(f"{lignes_sans_montant} lignes sans montant")

        if not resultat["alertes"]:
            resultat["alertes"].append("Aucune anomalie majeure détectée")

    except Exception as e:
        resultat["erreur"] = str(e)

    return resultat
