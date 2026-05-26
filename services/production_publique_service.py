from sqlalchemy import text
from database import engine
from datetime import datetime
import random
import uuid


def initialiser_production_publique():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS production_publique_v3 (
                id SERIAL PRIMARY KEY,
                module VARCHAR(100),
                statut VARCHAR(50),
                charge_cpu NUMERIC(10,2),
                charge_ram NUMERIC(10,2),
                instances INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM production_publique_v3
        """)).scalar() or 0

        if existing == 0:

            modules = [
                ("KUBERNETES_HA", "READY", 32.4, 48.7, 3),
                ("AUTOSCALING", "READY", 41.2, 52.1, 4),
                ("SOCKETIO_NATIVE", "READY", 18.2, 22.5, 2),
                ("BACKUP_DISTRIBUE", "READY", 28.6, 35.1, 2),
                ("FLUTTER_MOBILE", "READY", 12.7, 18.9, 1),
                ("PRODUCTION_PUBLIC", "READY", 38.4, 44.2, 5),
            ]

            for module, statut, cpu, ram, instances in modules:

                conn.execute(text("""
                    INSERT INTO production_publique_v3
                    (
                        module,
                        statut,
                        charge_cpu,
                        charge_ram,
                        instances
                    )
                    VALUES
                    (
                        :module,
                        :statut,
                        :cpu,
                        :ram,
                        :instances
                    )
                """), {
                    "module": module,
                    "statut": statut,
                    "cpu": cpu,
                    "ram": ram,
                    "instances": instances,
                })


def simulation_autoscaling():

    instances = random.randint(3, 12)

    return {
        "autoscaling": "ACTIVE",
        "instances": instances,
        "charge_cluster": random.randint(30, 90),
        "statut": "SCALING_OK",
    }


def simulation_socketio():

    return {
        "socketio": "LIVE",
        "sessions": random.randint(15, 120),
        "events": random.randint(100, 1200),
        "latency_ms": random.randint(18, 65),
        "statut": "SOCKETIO_NATIVE_OK",
    }


def simulation_mobile():

    return {
        "flutter_mobile": "READY",
        "ios": "READY",
        "android": "READY",
        "sessions_mobile": random.randint(10, 200),
        "statut": "MOBILE_READY",
    }


def dashboard_production_publique():

    initialiser_production_publique()

    with engine.connect() as conn:

        rows = conn.execute(text("""
            SELECT *
            FROM production_publique_v3
            ORDER BY id
        """)).mappings().all()

    return {
        "modules": [dict(r) for r in rows],
        "server_time": datetime.utcnow().isoformat(),
        "production": "PUBLIC_READY",
    }

