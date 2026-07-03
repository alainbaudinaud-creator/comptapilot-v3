from decimal import Decimal
from difflib import SequenceMatcher


def _money(value):
    return Decimal(str(value or 0)).quantize(Decimal("0.01"))


def similarite(a, b):
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def scorer_rapprochement(operation, ecriture):
    score = 0

    montant_op = _money(operation.get("montant"))
    debit = _money(ecriture.get("debit"))
    credit = _money(ecriture.get("credit"))

    montant_ecriture = debit if debit > 0 else credit

    if abs(montant_op) == montant_ecriture:
        score += 60

    lib_score = similarite(operation.get("libelle"), ecriture.get("libelle"))
    score += int(lib_score * 30)

    if operation.get("date_operation") == ecriture.get("date_ecriture"):
        score += 10

    return min(score, 100)


def proposer_rapprochements(operations, ecritures, seuil=70):
    propositions = []

    for op in operations:
        meilleure = None
        meilleur_score = 0

        for ecriture in ecritures:
            score = scorer_rapprochement(op, ecriture)

            if score > meilleur_score:
                meilleur_score = score
                meilleure = ecriture

        if meilleure and meilleur_score >= seuil:
            propositions.append({
                "operation": op,
                "ecriture": meilleure,
                "score": meilleur_score,
                "statut": "PROPOSE",
            })
        else:
            propositions.append({
                "operation": op,
                "ecriture": None,
                "score": meilleur_score,
                "statut": "A_RAPPROCHER",
            })

    return propositions


def generer_ecriture_banque_si_absente(operation, compte_banque="512000", compte_attente="471000"):
    montant = _money(operation.get("montant"))

    if montant >= 0:
        lignes = [
            {"compte": compte_banque, "debit": float(montant), "credit": 0},
            {"compte": compte_attente, "debit": 0, "credit": float(montant)},
        ]
    else:
        montant_abs = abs(montant)
        lignes = [
            {"compte": compte_attente, "debit": float(montant_abs), "credit": 0},
            {"compte": compte_banque, "debit": 0, "credit": float(montant_abs)},
        ]

    return {
        "journal": "BQ",
        "date_ecriture": operation.get("date_operation"),
        "libelle": operation.get("libelle"),
        "lignes": lignes,
    }
