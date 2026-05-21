from datetime import datetime

from services.db import get_connection
from services.audit_service import ajouter_log
from services.log_service import log_info
from services.notifications_service import creer_notification


def generer_ecriture_automatique_test():

    conn = get_connection()
    c = conn.cursor()

    date_ecriture = datetime.now().strftime("%Y-%m-%d")
    piece = "AUTO-V7"
    libelle = "Écriture automatique générée par robot V7"

    c.execute("""
        INSERT INTO ecritures (
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            societe_id,
            compte_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        date_ecriture,
        piece,
        libelle,
        0,
        0,
        1,
        1
    ))

    conn.commit()
    conn.close()

    message = "Écriture automatique V7 générée"

    log_info(message)
    ajouter_log("GENERATION_ECRITURE_AUTO", message)

    creer_notification(
        "admin",
        "Une écriture automatique a été générée par le robot V7."
    )
