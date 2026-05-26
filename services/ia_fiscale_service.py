
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def analyse_fiscale():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    anomalies = [
        "TVA incohérente détectée",
        "Compte 471 à contrôler",
        "Variation charges élevée"
    ]

    for a in anomalies:

        cur.execute("""
        INSERT INTO notifications_auto
        (type_notif, message)
        VALUES (?, ?)
        """, (
            "IA",
            a
        ))

    con.commit()
    con.close()

    return len(anomalies)

def analyser_risque_fiscal():

    return {
        "score": 100,
        "risque": "FAIBLE",
        "anomalies": 0
    }


