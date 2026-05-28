from decimal import Decimal

def calcul_tva(tva_collectee, tva_deductible):
    collectee = Decimal(str(tva_collectee or 0))
    deductible = Decimal(str(tva_deductible or 0))
    solde = collectee - deductible

    return {
        "tva_collectee": float(collectee),
        "tva_deductible": float(deductible),
        "tva_a_payer": float(solde if solde > 0 else 0),
        "credit_tva": float(abs(solde) if solde < 0 else 0),
        "statut": "A_PAYER" if solde > 0 else "CREDIT_TVA" if solde < 0 else "NEANT",
    }
