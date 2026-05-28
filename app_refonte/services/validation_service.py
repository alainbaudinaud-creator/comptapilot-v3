from decimal import Decimal


def valider_siret(siret: str) -> bool:
    if not siret:
        return False
    digits = "".join(ch for ch in str(siret) if ch.isdigit())
    return len(digits) == 14


def valider_ecriture(debit, credit) -> dict:
    d = Decimal(str(debit or 0))
    c = Decimal(str(credit or 0))

    erreurs = []

    if d < 0 or c < 0:
        erreurs.append("Debit et credit doivent etre positifs")

    if d == 0 and c == 0:
        erreurs.append("Une ligne doit avoir un debit ou un credit")

    if d > 0 and c > 0:
        erreurs.append("Une ligne ne peut pas avoir debit et credit simultanement")

    return {
        "valide": len(erreurs) == 0,
        "erreurs": erreurs,
    }


def controle_equilibre_piece(lignes: list[dict]) -> dict:
    total_debit = sum(Decimal(str(l.get("debit", 0) or 0)) for l in lignes)
    total_credit = sum(Decimal(str(l.get("credit", 0) or 0)) for l in lignes)

    return {
        "total_debit": float(total_debit),
        "total_credit": float(total_credit),
        "equilibre": total_debit == total_credit,
        "ecart": float(total_debit - total_credit),
    }
