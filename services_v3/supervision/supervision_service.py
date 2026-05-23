from repositories.ecritures.supervision_repository import fetch_nombre_ecritures
from repositories.ecritures.supervision_repository import fetch_totaux_debit_credit
from repositories.ecritures_auto.ecritures_auto_repository import fetch_stats_ecritures_auto


def get_supervision_comptable():

    totaux = fetch_totaux_debit_credit()
    auto = fetch_stats_ecritures_auto()

    return {
        "ecritures": {
            "nb": fetch_nombre_ecritures(),
            "total_debit": totaux["total_debit"],
            "total_credit": totaux["total_credit"],
            "ecart": round(totaux["total_debit"] - totaux["total_credit"], 2)
        },
        "ecritures_auto": {
            "nb": auto["nb_ecritures_auto"],
            "total_debit": auto["total_debit"],
            "total_credit": auto["total_credit"],
            "ecart": round(auto["total_debit"] - auto["total_credit"], 2)
        },
        "statut": "ok"
    }

from repositories.ecritures.supervision_repository import (
    fetch_supervision_counts,
    fetch_supervision_events
)


def get_supervision_page_data():

    counts = fetch_supervision_counts()

    return {
        "nb_ecritures": counts["nb_ecritures"],
        "nb_precompta": counts["nb_precompta"],
        "nb_audit": counts["nb_audit"],
        "events": fetch_supervision_events()
    }
