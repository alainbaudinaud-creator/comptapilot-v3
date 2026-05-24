from database import engine
from sqlalchemy import text


sql = """
CREATE TABLE IF NOT EXISTS relances_client_v3 (
    id SERIAL PRIMARY KEY,
    societe_id INTEGER,
    type_relance TEXT,
    titre TEXT NOT NULL,
    message TEXT,
    reference_type TEXT,
    reference_id INTEGER,
    statut TEXT DEFAULT 'brouillon',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP
);
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Table relances_client_v3 OK")
