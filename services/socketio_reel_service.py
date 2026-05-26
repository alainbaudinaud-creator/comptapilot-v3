from sqlalchemy import text
from database import engine
from datetime import datetime


def initialiser_socketio_reel():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS socketio_reel_v3 (
                id SERIAL PRIMARY KEY,
                evenement VARCHAR(255),
                utilisateur VARCHAR(255),
                payload TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM socketio_reel_v3
        """)).scalar() or 0

        if existing == 0:

            conn.execute(text("""
                INSERT INTO socketio_reel_v3
                (evenement, utilisateur, payload)
                VALUES
                (
                    'SOCKETIO_READY',
                    'SYSTEM',
                    'Mode compatible Flask actif'
                )
            """))


def enregistrer_evenement(event_name, utilisateur, payload):

    initialiser_socketio_reel()

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO socketio_reel_v3
            (
                evenement,
                utilisateur,
                payload
            )
            VALUES
            (
                :event_name,
                :utilisateur,
                :payload
            )
        """), {
            "event_name": event_name,
            "utilisateur": utilisateur,
            "payload": str(payload)
        })


def stats_socketio_reel():

    initialiser_socketio_reel()

    with engine.connect() as conn:

        total = conn.execute(text("""
            SELECT COUNT(*) FROM socketio_reel_v3
        """)).scalar() or 0

    return {
        "events": total,
        "mode": "COMPATIBLE_FLASK",
        "status": "READY",
        "server_time": datetime.utcnow().isoformat(),
    }


def push_dashboard_event():

    payload = {
        "event": "DASHBOARD_REFRESH",
        "message": "Push live compatible Flask",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "LIVE_READY"
    }

    enregistrer_evenement(
        "DASHBOARD_REFRESH",
        "LIVE_USER",
        payload
    )

    return payload


def push_ocr_event(filename="facture_live.pdf"):

    payload = {
        "event": "OCR_ANALYSIS",
        "message": "Analyse OCR live compatible Flask",
        "filename": filename,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "OCR_READY"
    }

    enregistrer_evenement(
        "OCR_ANALYSIS",
        "LIVE_USER",
        payload
    )

    return payload


