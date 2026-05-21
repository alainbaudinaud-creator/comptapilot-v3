
from services.smtp_service import envoyer_email

def relancer_client(email, document):

    return envoyer_email(
        destinataire=email,
        sujet="Relance Comptapilot",
        contenu=f"""
Bonjour,

Nous vous rappelons la disponibilité du document :
{document}

Cordialement,
IFG SOLUTION
"""
    )
