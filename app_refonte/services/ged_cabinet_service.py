from sqlalchemy import text
from database import engine

def charger_ged_cabinet():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM pieces_v3 LIMIT 20")).mappings().all()
    return rows
