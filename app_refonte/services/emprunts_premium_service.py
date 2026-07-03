from decimal import Decimal, ROUND_HALF_UP


def _money(value):
    return Decimal(str(value or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calcul_mensualite(capital, taux_annuel, duree_mois):
    capital = _money(capital)
    taux = Decimal(str(taux_annuel or 0)) / Decimal("100")
    duree = int(duree_mois or 0)

    if capital <= 0 or duree <= 0:
        return 0

    taux_mensuel = taux / Decimal("12")

    if taux_mensuel == 0:
        return float(_money(capital / Decimal(duree)))

    mensualite = capital * taux_mensuel / (1 - (1 + taux_mensuel) ** Decimal(-duree))
    return float(_money(mensualite))


def generer_tableau_emprunt(capital, taux_annuel, duree_mois, date_debut=None):
    capital = _money(capital)
    taux = Decimal(str(taux_annuel or 0)) / Decimal("100")
    duree = int(duree_mois or 0)

    if capital <= 0 or duree <= 0:
        return {
            "success": False,
            "message": "Paramètres emprunt invalides",
            "tableau": [],
        }

    taux_mensuel = taux / Decimal("12")
    mensualite = _money(calcul_mensualite(capital, taux_annuel, duree))
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
            "date": date_debut,
            "mensualite": float(mensualite_reelle),
            "interets": float(interets),
            "capital": float(principal),
            "capital_restant": float(max(restant, Decimal("0.00"))),
        })

    return {
        "success": True,
        "capital": float(capital),
        "taux_annuel": float(taux_annuel or 0),
        "duree_mois": duree,
        "mensualite": float(mensualite),
        "tableau": tableau,
    }


def generer_ecritures_emprunt(tableau):
    lignes = tableau.get("tableau", tableau) if isinstance(tableau, dict) else tableau

    ecritures = []
    for ligne in lignes:
        mois = ligne.get("mois")
        interets = float(ligne.get("interets", 0))
        capital = float(ligne.get("capital", ligne.get("capital_rembourse", 0)))
        mensualite = float(ligne.get("mensualite", 0))

        ecritures.append({
            "mois": mois,
            "journal": "BQ",
            "libelle": f"Échéance emprunt mois {mois}",
            "debit": [
                {"compte": "164000", "libelle": "Remboursement capital emprunt", "montant": capital},
                {"compte": "661100", "libelle": "Intérêts des emprunts", "montant": interets},
            ],
            "credit": [
                {"compte": "512000", "libelle": "Banque", "montant": mensualite},
            ],
        })

    return {
        "success": True,
        "ecritures": ecritures,
        "nombre": len(ecritures),
    }
