from sqlalchemy import text
from database import engine

def charger_pdp(client_id=None):
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT * FROM pdp_v3 WHERE client_id=:cid"),
            {"cid": client_id or 0}
        ).mappings().all()
    return rows
