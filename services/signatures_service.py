from datetime import datetime
import hashlib

from services.db import get_connection
from services.audit_service import ajouter_log


def initialiser_signatures():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document TEXT,
            signataire TEXT,
            date_signature TEXT,
            empreinte_sha256 TEXT
        )
    """)

    conn.commit()
    conn.close()


def signer_document(document, signataire):
    initialiser_signatures()

    date_signature = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contenu = f"{document}|{signataire}|{date_signature}"
    empreinte = hashlib.sha256(contenu.encode("utf-8")).hexdigest()

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO signatures (
            document, signataire, date_signature, empreinte_sha256
        )
        VALUES (?, ?, ?, ?)
    """, (
        document,
        signataire,
        date_signature,
        empreinte
    ))

    conn.commit()
    conn.close()

    ajouter_log(
        "SIGNATURE",
        f"Document signé : {document} par {signataire}"
    )

    return {
        "document": document,
        "signataire": signataire,
        "date_signature": date_signature,
        "empreinte": empreinte
    }


