def calcul_score_client(client):

    score = 100

    if client.get("retard"):
        score -= 25

    score -= client.get("alertes", 0) * 5

    if client.get("tva_a_declarer", 0) > 5000:
        score -= 10

    if client.get("factures_pdp", 0) == 0:
        score -= 10

    return max(score, 0)


def analyser_client(client):

    score = calcul_score_client(client)

    alertes = []

    if client.get("retard"):
        alertes.append("DOSSIER_EN_RETARD")

    if client.get("alertes", 0) > 0:
        alertes.append("ALERTES_ACTIVES")

    if client.get("tva_a_declarer", 0) > 5000:
        alertes.append("TVA_IMPORTANTE")

    return {
        "nom": client["nom"],
        "score": score,
        "alertes": alertes,
        "priorite": 100 - score
    }


def supervision_cabinet(clients):

    analyses = [
        analyser_client(client)
        for client in clients
    ]

    score_global = int(
        sum(x["score"] for x in analyses)
        / len(analyses)
    )

    alertes = sum(
        len(x["alertes"])
        for x in analyses
    )

    dossiers_critiques = len([
        x for x in analyses
        if x["score"] < 60
    ])

    return {
        "score_cabinet": score_global,
        "alertes": alertes,
        "dossiers_critiques": dossiers_critiques,
        "clients": sorted(
            analyses,
            key=lambda x: x["priorite"],
            reverse=True
        )
    }
