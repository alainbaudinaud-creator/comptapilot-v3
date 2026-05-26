from repositories.journal.journal_repository import (
    list_ecritures_v3
)


def get_journal_dashboard(societe_id=None):

    ecritures = list_ecritures_v3(societe_id)

    total_debit = sum(
        item.get("debit", 0)
        for item in ecritures
    )

    total_credit = sum(
        item.get("credit", 0)
        for item in ecritures
    )

    ecart = round(
        total_debit - total_credit,
        2
    )

    return {
        "count": len(ecritures),
        "total_debit": round(total_debit, 2),
        "total_credit": round(total_credit, 2),
        "ecart": ecart,
        "equilibre": ecart == 0,
        "items": ecritures
    }

