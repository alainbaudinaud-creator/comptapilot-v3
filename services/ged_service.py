
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def ajouter_document(
    client,
    type_document,
    fichier
):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO documents_clients
    (
        client,
        type_document,
        fichier,
        statut
    )
    VALUES (?, ?, ?, ?)
    """, (
        client,
        type_document,
        fichier,
        "UPLOADED"
    ))

    con.commit()
    con.close()

def importer_fec(
    dossier,
    fichier
):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO imports_fec_reels
    (
        dossier,
        fichier,
        lignes,
        statut
    )
    VALUES (?, ?, ?, ?)
    """, (
        dossier,
        fichier,
        1250,
        "IMPORTE"
    ))

    con.commit()
    con.close()

def analyse_ocr(fichier):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO ocr_analyse
    (
        fichier,
        fournisseur,
        montant,
        tva,
        statut
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        fichier,
        "EDF",
        1200,
        240,
        "ANALYSE"
    ))

    con.commit()
    con.close()


