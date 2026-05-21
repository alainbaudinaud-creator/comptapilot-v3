from services.db import get_connection
from services.audit_service import ajouter_log
from services.log_service import log_info
from services.notifications_service import creer_notification


def surveiller_tresorerie():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0)
        FROM ecritures
    """)

    total_debit, total_credit = c.fetchone()
    conn.close()

    solde = round((total_debit or 0) - (total_credit or 0), 2)

    message = f"Surveillance trésorerie : solde estimé {solde} €"

    log_info(message)
    ajouter_log("SURVEILLANCE_TRESORERIE", message)

    if solde < 0:
        creer_notification(
            "admin",
            f"Alerte trésorerie : solde négatif détecté ({solde} €)"
        )

    return solde
