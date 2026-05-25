from sqlalchemy import text
from database import engine
from datetime import datetime
import random
import uuid


def initialiser_reglementaire():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dsp2_banking_v3 (
                id SERIAL PRIMARY KEY,
                banque VARCHAR(255),
                iban VARCHAR(255),
                statut VARCHAR(50),
                transactions INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS peppol_pdp_v3 (
                id SERIAL PRIMARY KEY,
                facture_numero VARCHAR(255),
                statut VARCHAR(50),
                flux VARCHAR(100),
                plateforme VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics_decisionnels_v3 (
                id SERIAL PRIMARY KEY,
                indicateur VARCHAR(255),
                valeur NUMERIC(18,2),
                tendance VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM analytics_decisionnels_v3
        """)).scalar() or 0

        if existing == 0:

            data = [
                ("CHIFFRE_AFFAIRES", 520000, "HAUSSE"),
                ("TRESORERIE", 182000, "STABLE"),
                ("TVA_DUE", 24000, "CONTROLE"),
                ("MARGE", 38, "HAUSSE"),
                ("RISQUE_CLIENT", 12, "FAIBLE"),
            ]

            for indicateur, valeur, tendance in data:

                conn.execute(text("""
                    INSERT INTO analytics_decisionnels_v3
                    (indicateur, valeur, tendance)
                    VALUES
                    (:indicateur, :valeur, :tendance)
                """), {
                    "indicateur": indicateur,
                    "valeur": valeur,
                    "tendance": tendance,
                })


def simulation_dsp2():

    banque = random.choice([
        "BNP PARIBAS",
        "CREDIT AGRICOLE",
        "SOCIETE GENERALE",
        "BPCE"
    ])

    iban = "FR76" + str(random.randint(1000000000, 9999999999))

    transactions = random.randint(50, 250)

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO dsp2_banking_v3
            (banque, iban, statut, transactions)
            VALUES
            (:banque, :iban, 'SYNC_OK', :transactions)
        """), {
            "banque": banque,
            "iban": iban,
            "transactions": transactions,
        })

    return {
        "banque": banque,
        "iban": iban,
        "transactions": transactions,
        "statut": "DSP2_READY",
    }


def simulation_peppol():

    numero = "FACT-" + str(uuid.uuid4())[:8]

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO peppol_pdp_v3
            (facture_numero, statut, flux, plateforme)
            VALUES
            (:numero, 'TRANSMIS', 'PEPPOL', 'PDP_COMPTAPILOT')
        """), {
            "numero": numero,
        })

    return {
        "facture_numero": numero,
        "flux": "PEPPOL",
        "plateforme": "PDP_COMPTAPILOT",
        "statut": "TRANSMIS",
    }


def moteur_tva_avance():

    tva_collectee = random.randint(20000, 50000)
    tva_deductible = random.randint(8000, 25000)

    return {
        "tva_collectee": tva_collectee,
        "tva_deductible": tva_deductible,
        "tva_due": tva_collectee - tva_deductible,
        "controle": "OK",
        "statut": "TVA_ENGINE_READY",
    }


def dashboard_reglementaire():

    initialiser_reglementaire()

    with engine.connect() as conn:

        banques = conn.execute(text("""
            SELECT COUNT(*) FROM dsp2_banking_v3
        """)).scalar() or 0

        peppol = conn.execute(text("""
            SELECT COUNT(*) FROM peppol_pdp_v3
        """)).scalar() or 0

        analytics = conn.execute(text("""
            SELECT *
            FROM analytics_decisionnels_v3
            ORDER BY id
        """)).mappings().all()

    return {
        "banques_connectees": banques,
        "factures_peppol": peppol,
        "analytics": [dict(a) for a in analytics],
        "statut": "REGLEMENTAIRE_READY",
        "server_time": datetime.utcnow().isoformat(),
    }
