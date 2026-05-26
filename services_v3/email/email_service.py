import os
import smtplib
from email.message import EmailMessage


def send_email_smtp(to_email, subject, body):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)

    if not smtp_host or not smtp_user or not smtp_password or not smtp_from:
        return {
            "success": False,
            "status": "smtp_non_configure",
            "message": "SMTP non configuré"
        }

    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return {
            "success": True,
            "status": "envoye",
            "message": "Email envoyé"
        }

    except Exception as exc:
        return {
            "success": False,
            "status": "erreur_smtp",
            "message": str(exc)
        }

