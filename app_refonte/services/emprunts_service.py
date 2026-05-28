from decimal import Decimal, ROUND_HALF_UP

def tableau_amortissement_emprunt(montant, taux_annuel, duree_mois):
    capital = Decimal(str(montant or 0))
    taux = Decimal(str(taux_annuel or 0)) / Decimal("100")
    mois = int(duree_mois or 0)

    if capital <= 0 or mois <= 0:
        return []

    taux_mensuel = taux / Decimal("12")

    if taux_mensuel == 0:
        echeance = (capital / Decimal(mois)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        echeance = (
            capital * taux_mensuel / (1 - (1 + taux_mensuel) ** (-mois))
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    restant = capital
    lignes = []

    for i in range(1, mois + 1):
        interets = (restant * taux_mensuel).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        principal = echeance - interets

        if i == mois:
            principal = restant
            echeance_finale = principal + interets
        else:
            echeance_finale = echeance

        restant -= principal
        if restant < Decimal("0.01"):
            restant = Decimal("0.00")

        lignes.append({
            "mois": i,
            "echeance": float(echeance_finale),
            "interets": float(interets),
            "capital": float(principal),
            "capital_restant": float(restant),
        })

    return lignes
