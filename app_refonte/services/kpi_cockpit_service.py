from decimal import Decimal


def _money(value):
    return float(Decimal(str(value or 0)).quantize(Decimal("0.01")))


def calculer_kpis_cockpit(data: dict) -> dict:
    societes = data.get("societes", [])
    ecritures = data.get("ecritures", [])
    documents = data.get("documents", [])
    taches = data.get("taches", [])
    alertes = data.get("alertes", [])

    total_debit = sum(Decimal(str(e.get("debit", 0) or 0)) for e in ecritures)
    total_credit = sum(Decimal(str(e.get("credit", 0) or 0)) for e in ecritures)

    docs_a_traiter = [d for d in documents if d.get("statut") in ["A_ANALYSER", "A_VALIDER"]]
    taches_urgentes = [t for t in taches if t.get("priorite") == "HAUTE" and t.get("statut") != "TERMINE"]
    alertes_critiques = [a for a in alertes if a.get("niveau") in ["CRITIQUE", "WARNING"]]

    score_base = 100
    score_base -= min(len(docs_a_traiter) * 2, 25)
    score_base -= min(len(taches_urgentes) * 4, 25)
    score_base -= min(len(alertes_critiques) * 5, 30)
    score_base -= 10 if total_debit != total_credit else 0

    return {
        "total_societes": len(societes),
        "total_ecritures": len(ecritures),
        "total_documents": len(documents),
        "documents_a_traiter": len(docs_a_traiter),
        "taches_urgentes": len(taches_urgentes),
        "alertes_critiques": len(alertes_critiques),
        "total_debit": _money(total_debit),
        "total_credit": _money(total_credit),
        "equilibre_comptable": total_debit == total_credit,
        "score_production": max(score_base, 0),
    }


def priorites_cockpit(data: dict) -> list[dict]:
    priorites = []

    for doc in data.get("documents", []):
        if doc.get("statut") in ["A_ANALYSER", "A_VALIDER"]:
            priorites.append({
                "type": "DOCUMENT",
                "titre": f"Traiter document : {doc.get('fichier')}",
                "niveau": "HAUTE" if doc.get("montant_ttc", 0) and doc.get("montant_ttc", 0) > 1000 else "NORMALE",
            })

    for tache in data.get("taches", []):
        if tache.get("statut") != "TERMINE":
            priorites.append({
                "type": "WORKFLOW",
                "titre": tache.get("titre"),
                "niveau": tache.get("priorite", "NORMALE"),
            })

    for alerte in data.get("alertes", []):
        if alerte.get("niveau") in ["CRITIQUE", "WARNING"]:
            priorites.append({
                "type": "ALERTE",
                "titre": alerte.get("message"),
                "niveau": alerte.get("niveau"),
            })

    ordre = {"CRITIQUE": 0, "HAUTE": 1, "WARNING": 2, "NORMALE": 3, "INFO": 4}
    return sorted(priorites, key=lambda x: ordre.get(x.get("niveau"), 9))[:10]
