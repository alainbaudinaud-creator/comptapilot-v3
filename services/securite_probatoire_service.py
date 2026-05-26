from sqlalchemy import text
from database import engine
from datetime import datetime
import hashlib
import uuid


def initialiser_securite_probatoire():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tenants_avances_v3 (
                id SERIAL PRIMARY KEY,
                tenant_code VARCHAR(100) UNIQUE,
                cabinet_nom VARCHAR(255),
                niveau_abonnement VARCHAR(100),
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS audit_legal_complet_v3 (
                id SERIAL PRIMARY KEY,
                tenant_code VARCHAR(100),
                utilisateur VARCHAR(255),
                action VARCHAR(255),
                module VARCHAR(100),
                empreinte_sha256 TEXT,
                detail TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS coffre_fort_probatoire_v3 (
                id SERIAL PRIMARY KEY,
                tenant_code VARCHAR(100),
                nom_document VARCHAR(255),
                type_document VARCHAR(100),
                hash_document TEXT,
                reference_archivage VARCHAR(255),
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS signatures_electroniques_reelles_v3 (
                id SERIAL PRIMARY KEY,
                tenant_code VARCHAR(100),
                document_nom VARCHAR(255),
                signataire VARCHAR(255),
                preuve_signature TEXT,
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM tenants_avances_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO tenants_avances_v3
                (tenant_code, cabinet_nom, niveau_abonnement, statut)
                VALUES
                ('CABINET_DEMO_V3', 'Cabinet Démo ComptaPilot', 'ENTERPRISE', 'ACTIF')
            """))


def enregistrer_audit(action, module, utilisateur="admin@comptapilot.local", tenant_code="CABINET_DEMO_V3"):

    raw = f"{tenant_code}|{utilisateur}|{action}|{module}|{datetime.utcnow().isoformat()}"
    empreinte = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO audit_legal_complet_v3
            (tenant_code, utilisateur, action, module, empreinte_sha256, detail)
            VALUES
            (:tenant_code, :utilisateur, :action, :module, :empreinte, :detail)
        """), {
            "tenant_code": tenant_code,
            "utilisateur": utilisateur,
            "action": action,
            "module": module,
            "empreinte": empreinte,
            "detail": raw,
        })

    return {
        "action": action,
        "module": module,
        "empreinte_sha256": empreinte,
        "statut": "AUDIT_OK",
    }


def archiver_document_probatoire(nom_document="document_demo.pdf", type_document="PDF"):

    hash_document = hashlib.sha256(
        f"{nom_document}-{datetime.utcnow().isoformat()}".encode("utf-8")
    ).hexdigest()

    reference = "ARCH-" + str(uuid.uuid4())

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO coffre_fort_probatoire_v3
            (tenant_code, nom_document, type_document, hash_document, reference_archivage, statut)
            VALUES
            ('CABINET_DEMO_V3', :nom_document, :type_document, :hash_document, :reference, 'ARCHIVE')
        """), {
            "nom_document": nom_document,
            "type_document": type_document,
            "hash_document": hash_document,
            "reference": reference,
        })

    enregistrer_audit("ARCHIVAGE_PROBATOIRE", "COFFRE_FORT")

    return {
        "nom_document": nom_document,
        "hash_document": hash_document,
        "reference_archivage": reference,
        "statut": "ARCHIVE",
    }


def signer_document(document_nom="document_demo.pdf", signataire="client.demo@comptapilot.local"):

    preuve = hashlib.sha256(
        f"{document_nom}-{signataire}-{datetime.utcnow().isoformat()}".encode("utf-8")
    ).hexdigest()

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO signatures_electroniques_reelles_v3
            (tenant_code, document_nom, signataire, preuve_signature, statut)
            VALUES
            ('CABINET_DEMO_V3', :document_nom, :signataire, :preuve, 'SIGNE')
        """), {
            "document_nom": document_nom,
            "signataire": signataire,
            "preuve": preuve,
        })

    enregistrer_audit("SIGNATURE_ELECTRONIQUE", "SIGNATURE")

    return {
        "document_nom": document_nom,
        "signataire": signataire,
        "preuve_signature": preuve,
        "statut": "SIGNE",
    }


def dashboard_securite_probatoire():

    initialiser_securite_probatoire()

    with engine.connect() as conn:
        tenants = conn.execute(text("SELECT COUNT(*) FROM tenants_avances_v3")).scalar() or 0
        audits = conn.execute(text("SELECT COUNT(*) FROM audit_legal_complet_v3")).scalar() or 0
        archives = conn.execute(text("SELECT COUNT(*) FROM coffre_fort_probatoire_v3")).scalar() or 0
        signatures = conn.execute(text("SELECT COUNT(*) FROM signatures_electroniques_reelles_v3")).scalar() or 0

    return {
        "tenants": tenants,
        "audits": audits,
        "archives": archives,
        "signatures": signatures,
        "statut": "SECURITE_PROBATOIRE_READY",
        "server_time": datetime.utcnow().isoformat(),
    }


