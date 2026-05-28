from decimal import Decimal, ROUND_HALF_UP
from datetime import date


def generer_plan_amortissement(
    designation,
    valeur_origine,
    duree_mois,
    compte_immo="218300",
    compte_amortissement="281830",
    compte_dotation="681120",
):
    valeur = Decimal(str(valeur_origine or 0))
    duree = int(duree_mois or 0)

    if valeur <= 0 or duree <= 0:
        return {
            "success": False,
            "erreur": "Valeur ou durée invalide",
        }

    mensualite = (valeur / Decimal(duree)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    lignes = []
    cumul = Decimal("0.00")

    for mois in range(1, duree + 1):

        dotation = mensualite

        if mois == duree:
            dotation = valeur - cumul

        cumul += dotation

        lignes.append({
            "mois": mois,
            "designation": designation,
            "compte_dotation": compte_dotation,
            "compte_amortissement": compte_amortissement,
            "dotation": float(dotation),
            "cumul": float(cumul),
            "vnc": float(valeur - cumul),
        })

    return {
        "success": True,
        "designation": designation,
        "compte_immo": compte_immo,
        "valeur_origine": float(valeur),
        "duree_mois": duree,
        "plan": lignes,
    }


def generer_ecritures_amortissement(plan):
    if not plan.get("success"):
        return []

    ecritures = []

    for ligne in plan["plan"]:

        montant = Decimal(str(ligne["dotation"]))

        ecritures.append({
            "journal": "OD",
            "date_ecriture": str(date.today()),
            "libelle": f"Dotation amortissement {ligne['designation']} - Mois {ligne['mois']}",
            "lignes": [
                {
                    "compte": ligne["compte_dotation"],
                    "debit": float(montant),
                    "credit": 0,
                },
                {
                    "compte": ligne["compte_amortissement"],
                    "debit": 0,
                    "credit": float(montant),
                }
            ]
        })

    return ecritures
