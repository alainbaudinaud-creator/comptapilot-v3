from sqlalchemy import text
from database import engine
import random
from datetime import datetime


def initialiser_dashboard_financier():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dashboard_financier_v3 (
                id SERIAL PRIMARY KEY,
                chiffre_affaires NUMERIC(14,2),
                tresorerie NUMERIC(14,2),
                tva_due NUMERIC(14,2),
                charges NUMERIC(14,2),
                resultat NUMERIC(14,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS production_cabinet_live_v3 (
                id SERIAL PRIMARY KEY,
                dossiers INTEGER,
                revisions INTEGER,
                liasses INTEGER,
                tva INTEGER,
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM dashboard_financier_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO dashboard_financier_v3
                (
                    chiffre_affaires,
                    tresorerie,
                    tva_due,
                    charges,
                    resultat
                )
                VALUES
                (
                    485000,
                    132000,
                    18200,
                    296000,
                    189000
                )
            """))

            conn.execute(text("""
                INSERT INTO production_cabinet_live_v3
                (
                    dossiers,
                    revisions,
                    liasses,
                    tva,
                    statut
                )
                VALUES
                (
                    126,
                    48,
                    32,
                    71,
                    'LIVE'
                )
            """))


def dashboard_financier_data():

    initialiser_dashboard_financier()

    with engine.connect() as conn:

        finance = conn.execute(text("""
            SELECT *
            FROM dashboard_financier_v3
            ORDER BY id DESC
            LIMIT 1
        """)).mappings().first()

        production = conn.execute(text("""
            SELECT *
            FROM production_cabinet_live_v3
            ORDER BY id DESC
            LIMIT 1
        """)).mappings().first()

    graphiques = []

    mois = [
        "Jan",
        "Fev",
        "Mar",
        "Avr",
        "Mai",
        "Jun",
        "Jul",
        "Aou",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    base = 28000

    for index, mois_nom in enumerate(mois):

        graphiques.append({
            "mois": mois_nom,
            "ca": base + (index * 2400) + random.randint(-1800, 1800),
            "tresorerie": 60000 + (index * 3500),
            "resultat": 9000 + (index * 1200),
        })

    return {
        "finance": dict(finance),
        "production": dict(production),
        "charts": graphiques,
        "server_time": datetime.utcnow().isoformat(),
    }


