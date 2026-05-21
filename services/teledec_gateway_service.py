
import sqlite3
from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"
OUTBOX = ROOT / "teledec_outbox"
OUTBOX.mkdir(exist_ok=True)

def init_teledec():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teledec_envois (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_envoi TEXT,
        destinataire TEXT,
        type_envoi TEXT,
        fichier TEXT,
        statut TEXT,
        message TEXT
    )
    """)

    con.commit()
    con.close()

def preparer_dossier_teledec():
    init_teledec()

    fichiers = [
        ROOT / "liasse_complete.pdf",
        ROOT / "bilan.pdf",
        ROOT / "compte_resultat.pdf",
    ]

    fecs = sorted(ROOT.glob("FEC_DGFIP_*.txt"))
    if fecs:
        fichiers.append(fecs[-1])

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    dossier = OUTBOX / f"teledec_{horodatage}"
    dossier.mkdir(exist_ok=True)

    copies = []

    for f in fichiers:
        if f.exists():
            cible = dossier / f.name
            shutil.copy2(f, cible)
            copies.append(str(cible))

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO teledec_envois
    (date_envoi, destinataire, type_envoi, fichier, statut, message)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        "TELEDEC",
        "PREPARATION",
        str(dossier),
        "PRET_A_TRANSMETTRE",
        "Dossier fiscal préparé pour télétransmission"
    ))

    con.commit()
    con.close()

    return dossier, copies

def envoyer_a_teledec_simulation():
    dossier, copies = preparer_dossier_teledec()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO teledec_envois
    (date_envoi, destinataire, type_envoi, fichier, statut, message)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        "TELEDEC",
        "ENVOI_EDI_TDFC",
        str(dossier),
        "SIMULATION_OK",
        "Passerelle prête. Brancher API/certificat Télédec réel pour émission effective."
    ))

    con.commit()
    con.close()

    return {
        "statut": "SIMULATION_OK",
        "dossier": str(dossier),
        "fichiers": copies
    }

def envoyer_client_simulation(email_client, message):
    init_teledec()

    dossier, copies = preparer_dossier_teledec()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO teledec_envois
    (date_envoi, destinataire, type_envoi, fichier, statut, message)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        email_client,
        "ENVOI_CLIENT",
        str(dossier),
        "EMAIL_PREPARE",
        message
    ))

    con.commit()
    con.close()

    return {
        "statut": "EMAIL_PREPARE",
        "client": email_client,
        "dossier": str(dossier),
        "fichiers": copies
    }

def historique():
    init_teledec()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    rows = cur.execute("""
        SELECT date_envoi, destinataire, type_envoi, fichier, statut, message
        FROM teledec_envois
        ORDER BY id DESC
        LIMIT 50
    """).fetchall()

    con.close()
    return rows
