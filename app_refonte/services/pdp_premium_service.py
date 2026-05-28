from datetime import datetime
from decimal import Decimal


STATUTS_FACTURE = [
    "BROUILLON",
    "A_VALIDER",
    "VALIDEE",
    "TRANSMISE_PDP",
    "ACCEPTEE",
    "REJETEE",
]


CHAMPS_OBLIGATOIRES_FACTURE = [
    "numero",
    "date_facture",
    "emetteur_siret",
    "client_siret",
    "montant_ht",
    "montant_tva",
    "montant_ttc",
]


def creer_facture_electronique(numero, date_facture, emetteur_siret, client_siret, montant_ht, montant_tva):
    ht = Decimal(str(montant_ht or 0))
    tva = Decimal(str(montant_tva or 0))
    ttc = ht + tva

    return {
        "numero": numero,
        "date_facture": date_facture,
        "emetteur_siret": emetteur_siret,
        "client_siret": client_siret,
        "montant_ht": float(ht),
        "montant_tva": float(tva),
        "montant_ttc": float(ttc),
        "statut": "BROUILLON",
        "created_at": datetime.utcnow().isoformat(),
    }


def valider_facture_pdp(facture):
    erreurs = []

    for champ in CHAMPS_OBLIGATOIRES_FACTURE:
        if facture.get(champ) in [None, ""]:
            erreurs.append(f"Champ obligatoire manquant : {champ}")

    if facture.get("emetteur_siret") and len(str(facture["emetteur_siret"])) != 14:
        erreurs.append("SIRET émetteur invalide")

    if facture.get("client_siret") and len(str(facture["client_siret"])) != 14:
        erreurs.append("SIRET client invalide")

    ht = Decimal(str(facture.get("montant_ht", 0)))
    tva = Decimal(str(facture.get("montant_tva", 0)))
    ttc = Decimal(str(facture.get("montant_ttc", 0)))

    if ht + tva != ttc:
        erreurs.append("Incohérence HT + TVA != TTC")

    return {
        "valide": len(erreurs) == 0,
        "erreurs": erreurs,
    }


def changer_statut_facture(facture, nouveau_statut):
    if nouveau_statut not in STATUTS_FACTURE:
        raise ValueError("Statut facture invalide")

    facture["statut"] = nouveau_statut
    facture["updated_at"] = datetime.utcnow().isoformat()

    return facture


def generer_evenement_pdp(facture, action, utilisateur="system"):
    return {
        "facture_numero": facture.get("numero"),
        "action": action,
        "statut": facture.get("statut"),
        "utilisateur": utilisateur,
        "timestamp": datetime.utcnow().isoformat(),
    }


def preparer_e_reporting(factures):
    total_ht = sum(Decimal(str(f.get("montant_ht", 0))) for f in factures)
    total_tva = sum(Decimal(str(f.get("montant_tva", 0))) for f in factures)
    total_ttc = sum(Decimal(str(f.get("montant_ttc", 0))) for f in factures)

    return {
        "nombre_factures": len(factures),
        "total_ht": float(total_ht),
        "total_tva": float(total_tva),
        "total_ttc": float(total_ttc),
    }
