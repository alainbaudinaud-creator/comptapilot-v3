from repositories.ecritures.dashboard_repository import fetch_global_stats


def get_dashboard_financier():

    stats = fetch_global_stats()

    total_credit = stats["total_credit"]
    total_debit = stats["total_debit"]

    resultat = round(total_credit - total_debit, 2)

    return {
        "ca": round(total_credit, 2),
        "charges": round(total_debit, 2),
        "resultat": resultat,
        "tva_estimee": round(total_credit * 0.20, 2),
        "nb_ecritures": stats["nb_ecritures"],
        "statut": "ok"
    }

