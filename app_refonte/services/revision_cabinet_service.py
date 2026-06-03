import os
from sqlalchemy import create_engine, text


def _database_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot"
    )


def charger_revision_cabinet():
    data = {
        "comptes_a_controler": 0,
        "priorite_haute": 0,
        "ecritures_non_justifiees": 0,
        "anomalies_tva": 0,
        "anomalies_banque": 0,
        "anomalies_tiers": 0,
        "taches_ia_terminees": 0,
        "points_bloquants_bruts": 0,
        "points_bloquants": 0,
        "score_cloture": 100,
        "statut": "POSTGRES_REEL_V3"
    }

    try:
        engine = create_engine(_database_url(), pool_pre_ping=True)

        with engine.connect() as conn:
            comptes_attente = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE compte LIKE '471%'
                   OR compte LIKE '467%'
            """)).scalar() or 0

            libelles_faibles = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE libelle IS NULL
                   OR LENGTH(TRIM(libelle)) < 5
            """)).scalar() or 0

            anomalies_tva = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE compte LIKE '445%'
                  AND COALESCE(debit,0) = 0
                  AND COALESCE(credit,0) = 0
            """)).scalar() or 0

            anomalies_banque = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE compte LIKE '512%'
                  AND COALESCE(debit,0) = 0
                  AND COALESCE(credit,0) = 0
            """)).scalar() or 0

            anomalies_tiers = conn.execute(text("""
                SELECT COUNT(*)
                FROM lignes_ecritures_v3
                WHERE (
                    compte LIKE '401%'
                    AND COALESCE(debit,0) > COALESCE(credit,0)
                )
                OR (
                    compte LIKE '411%'
                    AND COALESCE(credit,0) > COALESCE(debit,0)
                )
            """)).scalar() or 0

            taches_ia_terminees = conn.execute(text("""
                SELECT COUNT(*)
                FROM taches_cabinet_v3
                WHERE titre LIKE '[IA]%'
                  AND statut = 'TERMINE'
            """)).scalar() or 0

        total_alertes = (
            comptes_attente
            + libelles_faibles
            + anomalies_tva
            + anomalies_banque
            + anomalies_tiers
        )

        points_bruts = min(int(total_alertes), 25)
        reduction_taches = int(taches_ia_terminees) * 5
        points_nets = max(0, points_bruts - reduction_taches)

        data["comptes_a_controler"] = int(comptes_attente)
        data["ecritures_non_justifiees"] = int(libelles_faibles)
        data["anomalies_tva"] = int(anomalies_tva)
        data["anomalies_banque"] = int(anomalies_banque)
        data["anomalies_tiers"] = int(anomalies_tiers)
        data["taches_ia_terminees"] = int(taches_ia_terminees)
        data["points_bloquants_bruts"] = points_bruts
        data["points_bloquants"] = points_nets
        data["priorite_haute"] = min(points_nets, 10)
        data["score_cloture"] = max(0, min(100, 100 - points_nets * 3))

    except Exception as e:
        data["statut"] = "ERREUR"
        data["erreur"] = str(e)

    return data
