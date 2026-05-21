from services.audit_service import ajouter_log
from services.log_service import log_info, log_erreur

from services.notifications_service import creer_notification
from services.email_service import envoyer_email

from services.anomalies_service import detecter_anomalies_ecritures
from services.tresorerie_service import surveiller_tresorerie
from services.ecritures_auto_service import generer_ecriture_automatique_test
from services.ia_comptable_service import analyser_comptabilite_ia


def robot_relances_clients():

    message = "Robot relances clients exécuté"

    log_info(message)

    ajouter_log(
        "ROBOT_RELANCES_CLIENTS",
        message
    )

    creer_notification(
        "admin",
        "Relances clients : vérification automatique effectuée par le robot V7."
    )

    envoyer_email(
        "ifgsolutions16@gmail.com",
        "Relance clients automatique ComptaPilot",
        (
            "Le robot V7 de relances clients "
            "a été exécuté automatiquement."
        ),
        mail=None
    )


def robot_detection_anomalies():

    anomalies = detecter_anomalies_ecritures()

    message = (
        f"Robot détection anomalies exécuté : "
        f"{len(anomalies)} anomalie(s)"
    )

    log_info(message)

    ajouter_log(
        "ROBOT_DETECTION_ANOMALIES",
        message
    )


def robot_surveillance_tresorerie():

    solde = surveiller_tresorerie()

    message = (
        f"Robot surveillance trésorerie exécuté : "
        f"solde {solde} €"
    )

    log_info(message)

    ajouter_log(
        "ROBOT_SURVEILLANCE_TRESORERIE",
        message
    )


def robot_generation_ecritures():

    generer_ecriture_automatique_test()

    message = "Robot génération écritures automatiques exécuté"

    log_info(message)

    ajouter_log(
        "ROBOT_GENERATION_ECRITURES",
        message
    )


def robot_notifications_automatiques():

    message = "Robot notifications automatiques exécuté"

    log_info(message)

    ajouter_log(
        "ROBOT_NOTIFICATIONS_AUTOMATIQUES",
        message
    )

    creer_notification(
        "admin",
        "Notification automatique générée par le robot V7."
    )


def robot_ia_comptable():

    message_ia = analyser_comptabilite_ia()

    message = f"Robot IA comptable exécuté : {message_ia}"

    log_info(message)

    ajouter_log(
        "ROBOT_IA_COMPTABLE",
        message
    )


def executer_robot_par_type(type_tache):

    try:

        type_normalise = (type_tache or "").upper()

        if type_normalise == "RELANCES_CLIENTS":
            robot_relances_clients()

        elif type_normalise == "DETECTION_ANOMALIES":
            robot_detection_anomalies()

        elif type_normalise == "SURVEILLANCE_TRESORERIE":
            robot_surveillance_tresorerie()

        elif type_normalise == "GENERATION_ECRITURES":
            robot_generation_ecritures()

        elif type_normalise == "NOTIFICATIONS":
            robot_notifications_automatiques()

        elif type_normalise == "IA_COMPTABLE":
            robot_ia_comptable()

        else:

            message = f"Type de robot inconnu : {type_tache}"

            log_info(message)

            ajouter_log(
                "ROBOT_INCONNU",
                message
            )

    except Exception as erreur:

        log_erreur(
            f"Erreur robot métier : {erreur}"
        )
