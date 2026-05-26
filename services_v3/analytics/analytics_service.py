from repositories.ecritures.analytics_repository import fetch_global_stats
from repositories.ecritures.analytics_repository import fetch_dashboard_financier_par_type


def get_analytics_financier():

    stats = fetch_global_stats()
    rows = fetch_dashboard_financier_par_type()

    charges = 0
    produits = 0

    for type_compte, debit, credit in rows:
        if type_compte == "Charge":
            charges += float(debit or 0) - float(credit or 0)

        if type_compte == "Produit":
            produits += float(credit or 0) - float(debit or 0)

    resultat = produits - charges

    return {
        "global": stats,
        "produits": round(produits, 2),
        "charges": round(charges, 2),
        "resultat": round(resultat, 2),
        "tva_collectee": round(produits * 0.20, 2),
        "tva_deductible": round(charges * 0.20, 2),
        "tva_a_payer": round((produits * 0.20) - (charges * 0.20), 2)
    }


