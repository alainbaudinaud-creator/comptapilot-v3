from services_v3.analytics.analytics_service import get_analytics_financier


def get_tva_estimee():

    analytics = get_analytics_financier()

    return {
        "tva_collectee": analytics["tva_collectee"],
        "tva_deductible": analytics["tva_deductible"],
        "tva_a_payer": analytics["tva_a_payer"],
        "base_produits": analytics["produits"],
        "base_charges": analytics["charges"],
        "statut": "ok"
    }
