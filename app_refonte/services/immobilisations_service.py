from decimal import Decimal, ROUND_HALF_UP


def _money(value):
    return Decimal(str(value or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def amortissement_lineaire(valeur_origine, duree_mois):
    valeur = _money(valeur_origine)
    duree = int(duree_mois or 0)

    if duree <= 0:
        return {
            "success": False,
            "message": "Durée d'amortissement invalide",
            "valeur_origine": float(valeur),
            "duree_mois": duree,
            "mensualite": 0,
            "tableau": [],
        }

    mensualite = _money(valeur / Decimal(duree))
    tableau = []
    cumul = Decimal("0.00")

    for mois in range(1, duree + 1):
        dotation = mensualite if mois < duree else _money(valeur - cumul)
        cumul = _money(cumul + dotation)
        valeur_nette = _money(valeur - cumul)

        tableau.append({
            "mois": mois,
            "dotation": float(dotation),
            "cumul_amortissement": float(cumul),
            "valeur_nette": float(valeur_nette),
        })

    return {
        "success": True,
        "valeur_origine": float(valeur),
        "duree_mois": duree,
        "mensualite": float(mensualite),
        "tableau": tableau,
    }
