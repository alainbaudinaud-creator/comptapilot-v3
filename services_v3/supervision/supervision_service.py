from repositories.ecritures.supervision_repository import fetch_nombre_ecritures
from repositories.ecritures.supervision_repository import fetch_totaux_debit_credit


def get_supervision_comptable():

    totaux = fetch_totaux_debit_credit()

    return {
        "nb_ecritures": fetch_nombre_ecritures(),
        "total_debit": totaux["total_debit"],
        "total_credit": totaux["total_credit"],
        "ecart": round(totaux["total_debit"] - totaux["total_credit"], 2)
    }
