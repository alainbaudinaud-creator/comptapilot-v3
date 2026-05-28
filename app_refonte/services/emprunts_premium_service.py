from decimal import Decimal, ROUND_HALF_UP


def calcul_mensualite(capital, taux_annuel, duree_mois):
    capital = Decimal(str(capital))
    taux = Decimal(str(taux_annuel)) / Decimal("100")
    mensualite_taux = taux / Decimal("12")

    if mensualite_taux == 0:
        return (capital / duree_mois).quantize(Decimal("0.01"))

    mensualite = capital * (
        mensualite_taux /
        (1 - (1 + mensualite_taux) ** (-duree_mois))
    )

    return mensualite.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def generer_tableau_emprunt(
    capital,
    taux_annuel,
    duree_mois,
    compte_emprunt="164000",
    compte_interets="661100",
    compte_banque="512000",
):
    capital = Decimal(str(capital))
    duree_mois = int(duree_mois)

    mensualite = calcul_mensualite(
        capital,
        taux_annuel,
        duree_mois,
    )

    crd = capital

    lignes = []

    for mois in range(1, duree_mois + 1):

        interets = (
            crd *
            (Decimal(str(taux_annuel)) / Decimal("100")) /
            Decimal("12")
        ).quantize(Decimal("0.01"))

        remboursement = mensualite - interets

        if mois == duree_mois:
            remboursement = crd
            mensualite = remboursement + interets

        crd -= remboursement

        lignes.append({
            "mois": mois,
            "mensualite": float(mensualite),
            "interets": float(interets),
            "remboursement_capital": float(remboursement),
            "capital_restant_du": float(max(crd, Decimal("0"))),
            "compte_emprunt": compte_emprunt,
            "compte_interets": compte_interets,
            "compte_banque": compte_banque,
        })

    return {
        "capital": float(capital),
        "taux_annuel": float(taux_annuel),
        "duree_mois": duree_mois,
        "mensualite": float(mensualite),
        "tableau": lignes,
    }


def generer_ecritures_emprunt(tableau):
    ecritures = []

    for ligne in tableau["tableau"]:

        ecritures.append({
            "journal": "BQ",
            "libelle": f"Echéance emprunt mois {ligne['mois']}",
            "lignes": [
                {
                    "compte": ligne["compte_emprunt"],
                    "debit": ligne["remboursement_capital"],
                    "credit": 0,
                },
                {
                    "compte": ligne["compte_interets"],
                    "debit": ligne["interets"],
                    "credit": 0,
                },
                {
                    "compte": ligne["compte_banque"],
                    "debit": 0,
                    "credit": ligne["mensualite"],
                },
            ]
        })

    return ecritures
