from sqlalchemy import text
from database import engine

def lire_notifications(user_id):
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT message, type, date_creation, lu
            FROM notifications_cabinet_v3
            WHERE user_id = :uid
            ORDER BY date_creation DESC
            LIMIT 20
        """), {"uid": user_id}).mappings().all()
    return rows
