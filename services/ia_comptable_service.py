from services.db import get_connection
from services.audit_service import ajouter_log
from services.log_service import log_info
from services.notifications_service import creer_notification


def analyser_comptabilite_ia():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0)
        FROM ecritures
    """)

    nombre_ecritures, total_debit, total_credit = c.fetchone()
    conn.close()

    solde = round((total_debit or 0) - (total_credit or 0), 2)

    message = (
        f"Analyse IA comptable : {nombre_ecritures} écritures analysées, "
        f"solde estimé {solde} €"
    )

    log_info(message)
    ajouter_log("IA_COMPTABLE_PLANIFIEE", message)

    creer_notification(
        "admin",
        message
    )

    return message

