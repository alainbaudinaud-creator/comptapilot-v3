from services_v3.analytics.analytics_service import get_analytics_financier
from services_v3.tva.tva_service import get_tva_estimee
from services_v3.supervision.supervision_service import get_supervision_comptable


def get_kpi_financiers():

    analytics = get_analytics_financier()
    tva = get_tva_estimee()
    supervision = get_supervision_comptable()

    total_debit = supervision["ecritures"]["total_debit"]
    total_credit = supervision["ecritures"]["total_credit"]

    marge = analytics["produits"] - analytics["charges"]

    ratio_marge = 0

    if analytics["produits"] > 0:
        ratio_marge = round(
            (marge / analytics["produits"]) * 100,
            2
        )

    return {
        "ca": analytics["produits"],
        "charges": analytics["charges"],
        "resultat": analytics["resultat"],
        "marge": round(marge, 2),
        "ratio_marge": ratio_marge,
        "tva_a_payer": tva["tva_a_payer"],
        "nb_ecritures": supervision["ecritures"]["nb"],
        "equilibre_comptable": round(
            total_credit - total_debit,
            2
        ),
        "statut": "ok"
    }
