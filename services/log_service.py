from datetime import datetime
import os

LOG_DIR = "C:/Users/alain/mon-projet-agent/logs"
LOG_FILE = os.path.join(LOG_DIR, "application.log")


def ecrire_log(niveau, message):
    os.makedirs(LOG_DIR, exist_ok=True)

    ligne = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
        f"[{niveau}] {message}\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as fichier:
        fichier.write(ligne)


def log_info(message):
    ecrire_log("INFO", message)


def log_erreur(message):
    ecrire_log("ERREUR", message)
