import os
from sqlalchemy import create_engine, text


def db_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot"
    )


def _table_exists(conn, table_name):
    return bool(conn.execute(text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = :table_name
        )
    """), {"table_name": table_name}).scalar())


def _detecter_table_ecritures(conn):
    for table in ["ecritures_premium", "ecritures_v3", "ecritures"]:
        if _table_exists(conn, table):
            return table
    return None


def calculer_controles_ia():

    resultat = {
        "score_risque": 0,
        "table_source": None,
        "alertes": []
    }

    try:
        engine = create_engine(db_url(), pool_pre_ping=True)

        with engine.connect() as conn:
            table = _detecter_table_ecritures(conn)
            resultat["table_source"] = table

            if not table:
                resultat["alertes"].append("Aucune table d'écritures détectée")
                return resultat

            comptes_attente = conn.execute(text(f"""
                SELECT COUNT(*)
                FROM {table}
                WHERE compte::text LIKE '471%'
                   OR compte::text LIKE '467%'
            """)).scalar() or 0

            libelles_vides = conn.execute(text(f"""
                SELECT COUNT(*)
                FROM {table}
                WHERE libelle IS NULL
                   OR TRIM(libelle)=''
            """)).scalar() or 0

            fournisseurs_debiteurs = conn.execute(text(f"""
                SELECT COUNT(*)
                FROM {table}
                WHERE compte::text LIKE '401%'
                  AND COALESCE(debit,0) > COALESCE(credit,0)
            """)).scalar() or 0

            clients_crediteurs = conn.execute(text(f"""
                SELECT COUNT(*)
                FROM {table}
                WHERE compte::text LIKE '411%'
                  AND COALESCE(credit,0) > COALESCE(debit,0)
            """)).scalar() or 0

        score = (
            comptes_attente * 5 +
            libelles_vides * 2 +
            fournisseurs_debiteurs * 3 +
            clients_crediteurs * 3
        )

        resultat["score_risque"] = min(score, 100)

        if comptes_attente:
            resultat["alertes"].append(f"{comptes_attente} écritures sur comptes d'attente 471/467")

        if libelles_vides:
            resultat["alertes"].append(f"{libelles_vides} écritures sans libellé")

        if fournisseurs_debiteurs:
            resultat["alertes"].append(f"{fournisseurs_debiteurs} écritures fournisseurs débitrices")

        if clients_crediteurs:
            resultat["alertes"].append(f"{clients_crediteurs} écritures clients créditrices")

        if not resultat["alertes"]:
            resultat["alertes"].append("Aucune anomalie majeure détectée")

    except Exception as e:
        resultat["erreur"] = str(e)

    return resultat
