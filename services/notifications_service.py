
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def notifier(message, type_notif="INFO"):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO notifications_centre
    (type_notif, message)
    VALUES (?, ?)
    """, (type_notif, message))

    con.commit()
    con.close()

    return "NOTIFICATION_OK"
