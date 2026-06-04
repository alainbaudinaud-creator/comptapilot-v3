from sqlalchemy import text
from database import engine

def charger_revision_cabinet(limit=20):
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM taches_cabinet_v3 ORDER BY id DESC LIMIT :lim"), {"lim": limit}).mappings().all()
    return rows
