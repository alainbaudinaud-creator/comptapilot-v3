from flask_mail import Message

from services.log_service import log_info, log_erreur
from services.audit_service import ajouter_log


def envoyer_email(destinataire, sujet, contenu, mail=None):

    if mail is None:
        log_erreur("Service email non initialisé : objet mail absent")
        return False

    try:
        message = Message(
            subject=sujet,
            recipients=[destinataire],
            body=contenu
        )

        mail.send(message)

        log_info(f"Email envoyé à {destinataire}")

        ajouter_log(
            "EMAIL_AUTO",
            f"Email envoyé à {destinataire} : {sujet}"
        )

        return True

    except Exception as erreur:
        log_erreur(f"Erreur email : {erreur}")
        return False


