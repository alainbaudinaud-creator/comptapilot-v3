
import smtplib
import sqlite3
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def envoyer_email(destinataire, sujet, contenu, piece_jointe=None):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    smtp = cur.execute("""
        SELECT smtp_host, smtp_port, smtp_user, smtp_password
        FROM smtp_settings
        WHERE actif=1
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    if not smtp:
        return "SMTP NON CONFIGURE"

    host, port, user, password = smtp

    msg = EmailMessage()
    msg["Subject"] = sujet
    msg["From"] = user
    msg["To"] = destinataire
    msg.set_content(contenu)

    if piece_jointe:
        p = Path(piece_jointe)
        if p.exists():
            with open(p, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=p.name
                )

    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)

        statut = "ENVOYE"

    except Exception as e:
        statut = str(e)

    cur.execute("""
        INSERT INTO mail_queue
        (destinataire, sujet, contenu, piece_jointe, statut)
        VALUES (?, ?, ?, ?, ?)
    """, (
        destinataire,
        sujet,
        contenu,
        str(piece_jointe),
        statut
    ))

    con.commit()
    con.close()

    return statut

