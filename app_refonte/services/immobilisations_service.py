from decimal import Decimal, ROUND_HALF_UP

def amortissement_lineaire(valeur_origine, duree_mois):
    valeur = Decimal(str(valeur_origine or 0))
    mois = int(duree_mois or 0)

    if mois <= 0:
        return []

    mensualite = (valeur / Decimal(mois)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    cumul = Decimal("0.00")
    lignes = []

    for i in range(1, mois + 1):
        dotation = mensualite if i < mois else valeur - cumul
        cumul += dotation
        vnc = valeur - cumul

        lignes.append({
            "mois": i,
            "dotation": float(dotation),
            "cumul": float(cumul),
            "vnc": float(vnc),
        })

    return lignes
