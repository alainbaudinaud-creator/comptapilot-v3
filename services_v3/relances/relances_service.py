from repositories.relances.relances_repository import (
    create_relance,
    list_relances,
    get_relance,
    get_societe_email,
    prepare_relance_email,
    mark_relance_sent
)

from services_v3.alerts.alerts_service import (
    get_alerts_center
)

from services_v3.email.email_service import (
    send_email_smtp
)


def get_relances_center():

    relances = list_relances()

    return {
        "count": len(relances),
        "draft_count": len([item for item in relances if item.get("statut") == "brouillon"]),
        "prepared_count": len([item for item in relances if item.get("email_status") == "pret"]),
        "sent_count": len([item for item in relances if item.get("statut") == "envoyee"]),
        "items": relances
    }


def generate_relances_from_alerts():

    alerts = get_alerts_center().get("items", [])
    created = []

    for alert in alerts:

        if alert.get("type") not in [
            "ocr_erreur",
            "ocr_en_attente",
            "precompta_rejetee"
        ]:
            continue

        relance_id = create_relance(
            {
                "societe_id": alert.get("societe_id"),
                "type_relance": alert.get("type"),
                "titre": build_relance_title(alert),
                "message": build_relance_message(alert),
                "reference_type": alert.get("type"),
                "reference_id": alert.get("reference_id")
            }
        )

        created.append(relance_id)

    return {
        "success": True,
        "created_count": len(created),
        "relance_ids": created,
        "message": "Relances générées depuis les alertes"
    }


def prepare_email_for_relance(relance_id):

    relance = get_relance(relance_id)

    if not relance:
        return {
            "success": False,
            "message": "Relance introuvable"
        }

    email_to = get_societe_email(
        relance.get("societe_id")
    )

    if not email_to:
        email_to = "client@example.com"

    email_subject = relance.get("titre") or "Relance cabinet"

    email_body = relance.get("message") or ""

    prepare_relance_email(
        relance_id=relance_id,
        email_to=email_to,
        email_subject=email_subject,
        email_body=email_body
    )

    return {
        "success": True,
        "relance_id": relance_id,
        "email_to": email_to,
        "email_subject": email_subject,
        "email_status": "pret",
        "message": "Email de relance préparé"
    }


def send_relance(relance_id):

    relance = get_relance(relance_id)

    if not relance:
        return {
            "success": False,
            "message": "Relance introuvable"
        }

    if relance.get("email_status") != "pret":
        return {
            "success": False,
            "message": "Email non préparé"
        }

    email_result = send_email_smtp(
        to_email=relance.get("email_to"),
        subject=relance.get("email_subject"),
        body=relance.get("email_body")
    )

    if not email_result.get("success"):
        return {
            "success": False,
            "relance_id": relance_id,
            "email_status": email_result.get("status"),
            "message": email_result.get("message")
        }

    mark_relance_sent(relance_id)

    return {
        "success": True,
        "relance_id": relance_id,
        "email_status": "envoye",
        "message": "Email de relance envoyé"
    }


def build_relance_title(alert):

    if alert.get("type") == "ocr_erreur":
        return "Action requise sur une pièce transmise"

    if alert.get("type") == "ocr_en_attente":
        return "Pièce en attente de traitement"

    if alert.get("type") == "precompta_rejetee":
        return "Information complémentaire requise"

    return "Relance client"


def build_relance_message(alert):

    return (
        "Bonjour,\n\n"
        "Votre cabinet a besoin d'une action ou d'une précision concernant "
        "un document de votre dossier.\n\n"
        f"Détail : {alert.get('message')}\n\n"
        "Merci de vous connecter à votre portail client ou de transmettre "
        "les éléments complémentaires nécessaires.\n\n"
        "Cordialement,\n"
        "Votre cabinet"
    )

