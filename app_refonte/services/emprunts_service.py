from decimal import Decimal, ROUND_HALF_UP


def _money(value):
    return Decimal(str(value or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def tableau_amortissement_emprunt(montant, taux_annuel, duree_mois):
    capital = _money(montant)
    taux = Decimal(str(taux_annuel or 0)) / Decimal("100")
    duree = int(duree_mois or 0)

    if capital <= 0 or duree <= 0:
        return {
            "success": False,
            "message": "Paramètres emprunt invalides",
            "tableau": [],
        }

    taux_mensuel = taux / Decimal("12")

    if taux_mensuel == 0:
        mensualite = _money(capital / Decimal(duree))
    else:
        mensualite = _money(capital * taux_mensuel / (1 - (1 + taux_mensuel) ** Decimal(-duree)))

    restant = capital
    tableau = []

    for mois in range(1, duree + 1):
        interets = _money(restant * taux_mensuel)
        principal = _money(mensualite - interets)

        if mois == duree:
            principal = restant
            mensualite_reelle = _money(principal + interets)
        else:
            mensualite_reelle = mensualite

        restant = _money(restant - principal)

        tableau.append({
            "mois": mois,
            "mensualite": float(mensualite_reelle),
            "interets": float(interets),
            "capital_rembourse": float(principal),
            "capital_restant": float(max(restant, Decimal("0.00"))),
        })

    return {
        "success": True,
        "montant": float(capital),
        "taux_annuel": float(taux_annuel or 0),
        "duree_mois": duree,
        "mensualite": float(mensualite),
        "tableau": tableau,
    }
