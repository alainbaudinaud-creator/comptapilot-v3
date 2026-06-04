from sqlalchemy import text
from database import engine

def analyser_pieces_ocr(limit=20):
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM pieces_v3 WHERE ocr_statut='NON_TRAITE' LIMIT :lim"), {"lim": limit}).mappings().all()
    return rows
