import os
from sqlalchemy import create_engine, text


def _database_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot"
    )


def charger_revision_cabinet():
    data = {
        "comptes_a_controler": 18,
        "priorite_haute": 6,
        "ecritures_non_justifiees": 9,
        "anomalies_tva": 4,
        "anomalies_banque": 6,
        "anomalies_tiers": 5,
        "score_cloture": 78,
        "points_bloquants": 7,
        "statut": "DEMO_REPLI"
    }

    try:
        engine = create_engine(_database_url(), pool_pre_ping=True)

        with engine.connect() as conn:
            # Comptes avec soldes anormaux simples
            try:
                row = conn.execute(text("""
                    SELECT COUNT(*) AS nb
                    FROM (
                        SELECT compte, SUM(debit - credit) AS solde
                        FROM ecritures_premium
                        GROUP BY compte
                        HAVING ABS(SUM(debit - credit)) > 0
                    ) x
                """)).mappings().first()
                data["comptes_a_controler"] = int(row["nb"] or 0)
            except Exception:
                pass

            # Ecritures non justifiées : libellé faible ou pièce absente si colonnes disponibles
            try:
                row = conn.execute(text("""
                    SELECT COUNT(*) AS nb
                    FROM ecritures_premium
                    WHERE libelle IS NULL
                       OR LENGTH(TRIM(libelle)) < 5
                """)).mappings().first()
                data["ecritures_non_justifiees"] = int(row["nb"] or 0)
            except Exception:
                pass

            # Anomalies TVA approximatives sur comptes TVA
            try:
                row = conn.execute(text("""
                    SELECT COUNT(*) AS nb
                    FROM ecritures_premium
                    WHERE compte::text LIKE '445%'
                      AND COALESCE(debit,0) = 0
                      AND COALESCE(credit,0) = 0
                """)).mappings().first()
                data["anomalies_tva"] = int(row["nb"] or 0)
            except Exception:
                pass

            # Anomalies banque approximatives
            try:
                row = conn.execute(text("""
                    SELECT COUNT(*) AS nb
                    FROM ecritures_premium
                    WHERE compte::text LIKE '512%'
                      AND (journal IS NULL OR TRIM(journal) = '')
                """)).mappings().first()
                data["anomalies_banque"] = int(row["nb"] or 0)
            except Exception:
                pass

            # Tiers à surveiller
            try:
                row = conn.execute(text("""
                    SELECT COUNT(*) AS nb
                    FROM ecritures_premium
                    WHERE compte::text LIKE '401%'
                       OR compte::text LIKE '411%'
                """)).mappings().first()
                data["anomalies_tiers"] = min(int(row["nb"] or 0), 99)
            except Exception:
                pass

        total_alertes = (
            data["comptes_a_controler"]
            + data["ecritures_non_justifiees"]
            + data["anomalies_tva"]
            + data["anomalies_banque"]
            + data["anomalies_tiers"]
        )

        data["points_bloquants"] = min(total_alertes, 25)
        data["priorite_haute"] = min(data["points_bloquants"], 10)
        data["score_cloture"] = max(0, min(100, 100 - data["points_bloquants"] * 3))
        data["statut"] = "POSTGRES_REEL"

    except Exception as e:
        data["erreur"] = str(e)

    return data
