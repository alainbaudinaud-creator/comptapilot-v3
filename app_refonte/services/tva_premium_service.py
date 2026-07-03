from decimal import Decimal, ROUND_HALF_UP


TVA_RATES = {
    "20": Decimal("0.20"),
    "10": Decimal("0.10"),
    "5.5": Decimal("0.055"),
    "2.1": Decimal("0.021"),
}


def calcul_tva(ht, taux):
    ht = Decimal(str(ht))
    taux_decimal = TVA_RATES[str(taux)]

    tva = (ht * taux_decimal).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    ttc = ht + tva

    return {
        "ht": float(ht),
        "tva": float(tva),
        "ttc": float(ttc),
        "taux": str(taux),
    }


def calcul_declaration_ca3(ecritures_tva):
    tva_collectee = Decimal("0")
    tva_deductible = Decimal("0")

    for e in ecritures_tva:

        montant = Decimal(str(e["montant"]))

        if e["type"] == "COLLECTEE":
            tva_collectee += montant

        if e["type"] == "DEDUCTIBLE":
            tva_deductible += montant

    tva_nette = tva_collectee - tva_deductible

    return {
        "tva_collectee": float(tva_collectee),
        "tva_deductible": float(tva_deductible),
        "tva_nette": float(tva_nette),
        "credit_tva": float(abs(tva_nette)) if tva_nette < 0 else 0,
        "a_payer": float(tva_nette) if tva_nette > 0 else 0,
    }


def generer_ecriture_tva(tva_nette):
    montant = Decimal(str(abs(tva_nette)))

    if tva_nette > 0:
        return {
            "journal": "OD",
            "libelle": "TVA à décaisser",
            "lignes": [
                {"compte": "445710", "debit": montant, "credit": 0},
                {"compte": "445510", "debit": 0, "credit": montant},
            ]
        }

    return {
        "journal": "OD",
        "libelle": "Crédit de TVA",
        "lignes": [
            {"compte": "445670", "debit": montant, "credit": 0},
            {"compte": "445710", "debit": 0, "credit": montant},
        ]
    }
