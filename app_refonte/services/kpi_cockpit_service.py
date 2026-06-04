from sqlalchemy import text
from database import engine

def charger_kpis():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT module, score, statut
            FROM kpis_cabinet_v3
        """)).mappings().all()
    return rows
