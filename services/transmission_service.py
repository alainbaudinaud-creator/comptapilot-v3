from services.audit_service import ajouter_log


def enregistrer_acces_transmission():
    ajouter_log(
        "TRANSMISSION_FACTURE",
        "Accès au module transmission factures"
    )


def lister_factures_transmission():
    return []


