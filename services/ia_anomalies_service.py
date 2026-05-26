
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def detecter_anomalies():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    anomalies = [
        ("TVA", "WARNING", "TVA inhabituelle détectée"),
        ("BANQUE", "INFO", "Rapprochement à vérifier")
    ]

    for a in anomalies:
        cur.execute("""
        INSERT INTO ia_anomalies
        (type_anomalie, niveau, message)
        VALUES (?, ?, ?)
        """, a)

    con.commit()
    con.close()

    return len(anomalies)


