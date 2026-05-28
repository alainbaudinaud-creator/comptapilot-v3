import re
from decimal import Decimal


FOURNISSEURS_CONNUS = {
    "orange": {
        "compte_charge": "626000",
        "libelle": "Télécommunications",
    },
    "amazon": {
        "compte_charge": "606300",
        "libelle": "Petit équipement",
    },
    "edf": {
        "compte_charge": "606100",
        "libelle": "Electricité",
    },
    "sncf": {
        "compte_charge": "625100",
        "libelle": "Voyages et déplacements",
    },
}


def nettoyer_texte(txt):
    return re.sub(r"\s+", " ", txt or "").strip()


def detecter_fournisseur(txt):
    txt = (txt or "").lower()

    for fournisseur in FOURNISSEURS_CONNUS:
        if fournisseur in txt:
            return fournisseur

    return "inconnu"


def extraire_montants(txt):
    txt = nettoyer_texte(txt)

    montants = re.findall(r"(\d+[.,]\d{2})", txt)

    valeurs = [
        Decimal(m.replace(",", "."))
        for m in montants
    ]

    if not valeurs:
        return {
            "ht": 0,
            "tva": 0,
            "ttc": 0,
        }

    valeurs = sorted(valeurs)

    ttc = valeurs[-1]

    tva = Decimal("0")
    ht = ttc

    if len(valeurs) >= 2:
        tva = valeurs[-2]
        ht = ttc - tva

    return {
        "ht": float(ht),
        "tva": float(tva),
        "ttc": float(ttc),
    }


def analyser_facture(txt):
    txt = nettoyer_texte(txt)

    fournisseur = detecter_fournisseur(txt)

    montants = extraire_montants(txt)

    fournisseur_data = FOURNISSEURS_CONNUS.get(
        fournisseur,
        {
            "compte_charge": "606000",
            "libelle": "Achats non stockés",
        }
    )

    score = 40

    if fournisseur != "inconnu":
        score += 30

    if montants["ttc"] > 0:
        score += 30

    return {
        "fournisseur": fournisseur,
        "compte_charge": fournisseur_data["compte_charge"],
        "libelle_charge": fournisseur_data["libelle"],
        "montants": montants,
        "score_ia": min(score, 100),
    }


def generer_ecriture_achat(analyse):
    ttc = Decimal(str(analyse["montants"]["ttc"]))
    ht = Decimal(str(analyse["montants"]["ht"]))
    tva = Decimal(str(analyse["montants"]["tva"]))

    return {
        "journal": "AC",
        "libelle": f"Facture {analyse['fournisseur']}",
        "score_ia": analyse["score_ia"],
        "lignes": [
            {
                "compte": analyse["compte_charge"],
                "debit": float(ht),
                "credit": 0,
            },
            {
                "compte": "445660",
                "debit": float(tva),
                "credit": 0,
            },
            {
                "compte": "401000",
                "debit": 0,
                "credit": float(ttc),
            }
        ]
    }
