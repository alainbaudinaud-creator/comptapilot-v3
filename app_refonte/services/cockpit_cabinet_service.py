from sqlalchemy import text
from database import engine

def charger_cockpit_reel():
    with engine.connect() as conn:
        kpis = conn.execute(text("SELECT * FROM cockpit_kpi_v3")).mappings().all()
        return kpis
