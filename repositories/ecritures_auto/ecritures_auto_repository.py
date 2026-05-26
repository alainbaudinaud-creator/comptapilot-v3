from repositories.sql_stats_repository import fetch_count
from repositories.sql_stats_repository import fetch_sum_debit_credit


def fetch_stats_ecritures_auto():

    stats = fetch_sum_debit_credit("ecritures_auto")

    return {
        "total_debit": stats["total_debit"],
        "total_credit": stats["total_credit"],
        "nb_ecritures_auto": stats["count"]
    }


def fetch_nombre_ecritures_auto():

    return fetch_count("ecritures_auto")

