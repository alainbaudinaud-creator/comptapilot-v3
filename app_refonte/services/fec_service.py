REQUIRED_FEC_COLUMNS = [
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

def controle_colonnes_fec(columns):
    colonnes = list(columns or [])
    manquantes = [c for c in REQUIRED_FEC_COLUMNS if c not in colonnes]

    return {
        "conforme": len(manquantes) == 0,
        "colonnes_attendues": REQUIRED_FEC_COLUMNS,
        "colonnes_manquantes": manquantes,
    }
