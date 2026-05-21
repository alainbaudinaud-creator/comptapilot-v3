from services.db import get_connection
from services.audit_service import ajouter_log
from services.log_service import log_info
from services.notifications_service import creer_notification


def detecter_anomalies_ecritures():

    anomalies = []

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT id, date_ecriture, piece, libelle, debit, credit
        FROM ecritures
        ORDER BY id DESC
        LIMIT 500
    """)

    lignes = c.fetchall()
    conn.close()

    for ligne in lignes:

        ecriture_id = ligne[0]
        piece = ligne[2]
        libelle = ligne[3]
        debit = ligne[4] or 0
        credit = ligne[5] or 0

        if not piece:
            anomalies.append(
                f"Écriture #{ecriture_id} sans pièce justificative"
            )

        if debit == 0 and credit == 0:
            anomalies.append(
                f"Écriture #{ecriture_id} avec débit et crédit à zéro"
            )

        if debit > 10000 or credit > 10000:
            anomalies.append(
                f"Écriture #{ecriture_id} montant élevé détecté : {libelle}"
            )

        if debit > 0 and credit > 0:
            anomalies.append(
                f"Écriture #{ecriture_id} contient débit ET crédit"
            )

    if anomalies:

        message = f"{len(anomalies)} anomalie(s) détectée(s) sur les écritures"

        log_info(message)
        ajouter_log("DETECTION_ANOMALIES", message)

        creer_notification(
            "admin",
            message
        )

    else:

        log_info("Détection anomalies : aucune anomalie détectée")
        ajouter_log(
            "DETECTION_ANOMALIES",
            "Aucune anomalie détectée"
        )

    return anomalies
