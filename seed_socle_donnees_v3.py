from sqlalchemy import text
from database import engine

statements = [
    """
    CREATE TABLE IF NOT EXISTS clients_v3 (
        id SERIAL PRIMARY KEY,
        siren VARCHAR(20),
        siret VARCHAR(20),
        raison_sociale VARCHAR(255) NOT NULL,
        forme_juridique VARCHAR(100),
        regime_fiscal VARCHAR(100),
        regime_tva VARCHAR(100),
        adresse TEXT,
        statut VARCHAR(50) DEFAULT 'ONBOARDING',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS exercices_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        date_debut DATE,
        date_fin DATE,
        statut VARCHAR(50) DEFAULT 'OUVERT',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS journaux_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        code VARCHAR(20) NOT NULL,
        libelle VARCHAR(255) NOT NULL,
        type_journal VARCHAR(50)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ecritures_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        exercice_id INTEGER,
        journal_id INTEGER,
        date_ecriture DATE,
        piece VARCHAR(100),
        libelle VARCHAR(255),
        statut VARCHAR(50) DEFAULT 'BROUILLARD',
        source VARCHAR(80) DEFAULT 'MANUEL',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lignes_ecritures_v3 (
        id SERIAL PRIMARY KEY,
        ecriture_id INTEGER NOT NULL,
        compte VARCHAR(20) NOT NULL,
        libelle VARCHAR(255),
        debit NUMERIC(14,2) DEFAULT 0,
        credit NUMERIC(14,2) DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS factures_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        sens VARCHAR(20),
        fournisseur_client VARCHAR(255),
        numero VARCHAR(100),
        date_facture DATE,
        montant_ht NUMERIC(14,2) DEFAULT 0,
        montant_tva NUMERIC(14,2) DEFAULT 0,
        montant_ttc NUMERIC(14,2) DEFAULT 0,
        statut VARCHAR(50) DEFAULT 'A_ANALYSER',
        score_ia INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS pieces_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        facture_id INTEGER,
        nom_fichier VARCHAR(255) NOT NULL,
        type_piece VARCHAR(80),
        chemin_stockage VARCHAR(500),
        statut_ocr VARCHAR(50) DEFAULT 'A_TRAITER',
        texte_ocr TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS imports_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        type_import VARCHAR(80) NOT NULL,
        nom_fichier VARCHAR(255),
        statut VARCHAR(50) DEFAULT 'RECU',
        nb_lignes INTEGER DEFAULT 0,
        rapport TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS workflow_cabinet_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        module VARCHAR(100) NOT NULL,
        etape VARCHAR(100) NOT NULL,
        statut VARCHAR(50) DEFAULT 'A_FAIRE',
        responsable VARCHAR(255),
        commentaire TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS taches_cabinet_v3 (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL,
        titre VARCHAR(255) NOT NULL,
        priorite VARCHAR(30) DEFAULT 'NORMALE',
        statut VARCHAR(50) DEFAULT 'A_FAIRE',
        echeance DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
]

with engine.begin() as conn:
    for statement in statements:
        conn.execute(text(statement))

    existing = conn.execute(
        text("SELECT id FROM clients_v3 WHERE siren = '000000000' LIMIT 1")
    ).fetchone()

    if not existing:
        client_id = conn.execute(text("""
            INSERT INTO clients_v3
            (siren, siret, raison_sociale, forme_juridique, regime_fiscal, regime_tva, adresse, statut)
            VALUES
            ('000000000', '00000000000000', 'CLIENT DEMO COMPTAPILOT V3', 'SAS', 'IS', 'REEL_NORMAL', 'Dossier de démonstration', 'ONBOARDING')
            RETURNING id
        """)).scalar()

        conn.execute(text("""
            INSERT INTO exercices_v3 (client_id, date_debut, date_fin, statut)
            VALUES (:client_id, '2026-01-01', '2026-12-31', 'OUVERT')
        """), {"client_id": client_id})

        for code, libelle, type_journal in [
            ("AC", "Achats", "ACHAT"),
            ("VE", "Ventes", "VENTE"),
            ("BQ", "Banque", "BANQUE"),
            ("OD", "Opérations diverses", "OD"),
        ]:
            conn.execute(text("""
                INSERT INTO journaux_v3 (client_id, code, libelle, type_journal)
                VALUES (:client_id, :code, :libelle, :type_journal)
            """), {
                "client_id": client_id,
                "code": code,
                "libelle": libelle,
                "type_journal": type_journal,
            })

        for module, etape in [
            ("ONBOARDING", "Création dossier"),
            ("IMPORT", "Import FEC / balance"),
            ("OCR", "Analyse pièces"),
            ("REVISION", "Contrôle comptes"),
            ("CLOTURE", "Production finale"),
        ]:
            conn.execute(text("""
                INSERT INTO workflow_cabinet_v3 (client_id, module, etape, statut)
                VALUES (:client_id, :module, :etape, 'A_FAIRE')
            """), {
                "client_id": client_id,
                "module": module,
                "etape": etape,
            })

        for titre, priorite in [
            ("Récupérer documents réglementaires", "HAUTE"),
            ("Importer plan comptable et FEC", "HAUTE"),
            ("Contrôler régime TVA", "NORMALE"),
        ]:
            conn.execute(text("""
                INSERT INTO taches_cabinet_v3 (client_id, titre, priorite)
                VALUES (:client_id, :titre, :priorite)
            """), {
                "client_id": client_id,
                "titre": titre,
                "priorite": priorite,
            })

print("SOCLE DONNEES V3 OK")


