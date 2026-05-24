from database import engine
from sqlalchemy import text


sql = """
CREATE TABLE IF NOT EXISTS notifications_v3 (
    id SERIAL PRIMARY KEY,
    societe_id INTEGER,
    type_notification TEXT,
    niveau TEXT,
    titre TEXT NOT NULL,
    message TEXT,
    reference_type TEXT,
    reference_id INTEGER,
    statut TEXT DEFAULT 'non_lue',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Table notifications_v3 OK")
