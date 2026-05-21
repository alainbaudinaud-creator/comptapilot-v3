
import sqlite3
from pathlib import Path

from services.teledec_gateway_service import envoyer_a_teledec_simulation
from services.documents_auto_service import envoyer_liasse_client

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def teledeclarer_exercice(exercice="2026", email_client=None):
    resultat = envoyer_a_teledec_simulation()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO depot_fiscal_auto
    (exercice, type_depot, fichier, statut)
    VALUES (?, ?, ?, ?)
    """, (
        exercice,
        "EDI_TDFC",
        resultat.get("dossier"),
        resultat.get("statut")
    ))

    con.commit()
    con.close()

    if email_client:
        envoyer_liasse_client(email_client)

    return resultat
