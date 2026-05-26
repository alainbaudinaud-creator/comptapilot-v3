from datetime import datetime

def notifier(message, type_notif="INFO"):
    print(f"[{type_notif}] {message}")
    return "NOTIFICATION_OK"


def creer_notification(message, type_notif="INFO", utilisateur_id=None):
    print(f"[{datetime.now().isoformat()}] [{type_notif}] {message}")
    return {
        "status": "NOTIFICATION_OK",
        "message": message,
        "type_notif": type_notif,
        "utilisateur_id": utilisateur_id
    }

