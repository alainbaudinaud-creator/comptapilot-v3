from decimal import Decimal


FEC_COLUMNS = [
    "JournalCode",
    "JournalLib",
    "EcritureNum",
    "EcritureDate",
    "CompteNum",
    "CompteLib",
    "CompAuxNum",
    "CompAuxLib",
    "PieceRef",
    "PieceDate",
    "EcritureLib",
    "Debit",
    "Credit",
    "EcritureLet",
    "DateLet",
    "ValidDate",
    "Montantdevise",
    "Idevise",
]


def valider_structure_fec(columns):
    columns = list(columns or [])
    manquantes = [c for c in FEC_COLUMNS if c not in columns]

    return {
        "conforme": len(manquantes) == 0,
        "colonnes_attendues": FEC_COLUMNS,
        "colonnes_manquantes": manquantes,
    }


def controler_lignes_fec(lignes):
    erreurs = []

    for index, ligne in enumerate(lignes, start=1):
        debit = Decimal(str(ligne.get("Debit", 0) or 0))
        credit = Decimal(str(ligne.get("Credit", 0) or 0))

        if debit < 0 or credit < 0:
            erreurs.append({
                "ligne": index,
                "erreur": "Debit ou credit negatif",
            })

        if debit > 0 and credit > 0:
            erreurs.append({
                "ligne": index,
                "erreur": "Debit et credit simultanes",
            })

        if debit == 0 and credit == 0:
            erreurs.append({
                "ligne": index,
                "erreur": "Debit et credit nuls",
            })

    return {
        "conforme": len(erreurs) == 0,
        "erreurs": erreurs,
    }


def exporter_fec_txt(lignes):
    output = ["|".join(FEC_COLUMNS)]

    for ligne in lignes:
        row = []
        for col in FEC_COLUMNS:
            row.append(str(ligne.get(col, "")))
        output.append("|".join(row))

    return "\n".join(output) + "\n"


def generer_ligne_fec_demo():
    return {
        "JournalCode": "AC",
        "JournalLib": "Achats",
        "EcritureNum": "AC000001",
        "EcritureDate": "20260131",
        "CompteNum": "606000",
        "CompteLib": "Achats non stockes",
        "CompAuxNum": "",
        "CompAuxLib": "",
        "PieceRef": "FAC-DEMO-001",
        "PieceDate": "20260131",
        "EcritureLib": "Facture demo",
        "Debit": "120.00",
        "Credit": "0.00",
        "EcritureLet": "",
        "DateLet": "",
        "ValidDate": "20260131",
        "Montantdevise": "",
        "Idevise": "",
    }
