from sqlalchemy import text
from database import engine

def charger_ged_cabinet():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM pieces_v3 LIMIT 20")).mappings().all()
        kpis = {"total_pieces": len(rows)}
        dossiers = [{"id": r["id"], "client_id": r["client_id"], "statut": r.get("statut","")} for r in rows]
        pieces = rows
    return kpis, dossiers, pieces
