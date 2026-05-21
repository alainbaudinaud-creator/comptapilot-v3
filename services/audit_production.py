
from datetime import datetime

def audit(action, utilisateur):

    ligne = f"{datetime.now()} | {utilisateur} | {action}\n"

    with open("audit_production.log", "a", encoding="utf-8") as f:
        f.write(ligne)
