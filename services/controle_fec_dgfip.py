
import csv

def verifier_fec(fichier):

    erreurs = []

    with open(fichier, encoding="utf-8") as f:

        reader = csv.reader(f, delimiter="|")

        headers = next(reader)

        obligatoires = [
            "JournalCode",
            "EcritureDate",
            "CompteNum",
            "Debit",
            "Credit"
        ]

        for col in obligatoires:
            if col not in headers:
                erreurs.append(f"Colonne absente : {col}")

    return erreurs


