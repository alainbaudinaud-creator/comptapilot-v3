
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def notifier(utilisateur, titre, message):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO notifications_realtime
    (utilisateur, titre, message)
    VALUES (?, ?, ?)
    """, (utilisateur, titre, message))

    con.commit()
    con.close()

def journaliser(module, evenement, niveau="INFO"):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO supervision_events
    (niveau, module, evenement)
    VALUES (?, ?, ?)
    """, (niveau, module, evenement))

    con.commit()
    con.close()


