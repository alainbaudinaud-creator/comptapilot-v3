from sqlalchemy import text
from database import engine
from datetime import datetime
import uuid
import random


def initialiser_commercialisation():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stripe_saas_v3 (
                id SERIAL PRIMARY KEY,
                client_email VARCHAR(255),
                abonnement VARCHAR(100),
                montant NUMERIC(18,2),
                statut VARCHAR(50),
                stripe_session VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS onboarding_clients_v3 (
                id SERIAL PRIMARY KEY,
                client_nom VARCHAR(255),
                email VARCHAR(255),
                progression INTEGER,
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS marketplace_connecteurs_v3 (
                id SERIAL PRIMARY KEY,
                connecteur VARCHAR(255),
                categorie VARCHAR(100),
                statut VARCHAR(50),
                version VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM marketplace_connecteurs_v3
        """)).scalar() or 0

        if existing == 0:

            connecteurs = [
                ("Pennylane", "COMPTABILITE", "READY", "1.0"),
                ("Qonto", "BANQUE", "READY", "1.0"),
                ("Stripe", "PAIEMENT", "READY", "1.0"),
                ("Chorus Pro", "FACTURATION", "READY", "1.0"),
                ("PEPPOL", "REGLEMENTAIRE", "READY", "1.0"),
                ("OpenAI", "IA", "READY", "1.0"),
            ]

            for c, cat, statut, version in connecteurs:

                conn.execute(text("""
                    INSERT INTO marketplace_connecteurs_v3
                    (connecteur, categorie, statut, version)
                    VALUES
                    (:c, :cat, :statut, :version)
                """), {
                    "c": c,
                    "cat": cat,
                    "statut": statut,
                    "version": version,
                })


def simulation_stripe():

    session = "cs_test_" + str(uuid.uuid4()).replace("-", "")

    montant = random.choice([49, 99, 199, 399])

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO stripe_saas_v3
            (
                client_email,
                abonnement,
                montant,
                statut,
                stripe_session
            )
            VALUES
            (
                'client.demo@comptapilot.local',
                'ENTERPRISE',
                :montant,
                'PAID',
                :session
            )
        """), {
            "montant": montant,
            "session": session,
        })

    return {
        "stripe_session": session,
        "montant": montant,
        "abonnement": "ENTERPRISE",
        "statut": "PAIEMENT_OK",
    }


def onboarding_client():

    progression = random.randint(65, 100)

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO onboarding_clients_v3
            (
                client_nom,
                email,
                progression,
                statut
            )
            VALUES
            (
                'Cabinet Client Demo',
                'client.demo@comptapilot.local',
                :progression,
                'ONBOARDING'
            )
        """), {
            "progression": progression,
        })

    return {
        "client": "Cabinet Client Demo",
        "progression": progression,
        "statut": "ONBOARDING_READY",
    }


def dashboard_commercial():

    initialiser_commercialisation()

    with engine.connect() as conn:

        abonnements = conn.execute(text("""
            SELECT COUNT(*) FROM stripe_saas_v3
        """)).scalar() or 0

        onboardings = conn.execute(text("""
            SELECT COUNT(*) FROM onboarding_clients_v3
        """)).scalar() or 0

        connecteurs = conn.execute(text("""
            SELECT *
            FROM marketplace_connecteurs_v3
            ORDER BY id
        """)).mappings().all()

    return {
        "abonnements": abonnements,
        "onboardings": onboardings,
        "connecteurs": [dict(c) for c in connecteurs],
        "cloud_public": "READY",
        "server_time": datetime.utcnow().isoformat(),
    }

