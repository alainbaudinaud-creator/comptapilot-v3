from services_v3.supervision.supervision_service import get_supervision_comptable
from services_v3.analytics.analytics_service import get_analytics_financier


def get_audit_comptable():

    supervision = get_supervision_comptable()
    analytics = get_analytics_financier()

    alertes = []

    ecart = supervision["ecritures"]["ecart"]

    if abs(ecart) > 0.01:
        alertes.append({
            "niveau": "critique",
            "message": "Écart débit/crédit détecté"
        })

    if analytics["tva_a_payer"] < 0:
        alertes.append({
            "niveau": "warning",
            "message": "TVA négative détectée"
        })

    if analytics["resultat"] < 0:
        alertes.append({
            "niveau": "warning",
            "message": "Résultat comptable négatif"
        })

    return {
        "statut": "ok",
        "nb_alertes": len(alertes),
        "alertes": alertes,
        "supervision": supervision,
        "analytics": analytics
    }
