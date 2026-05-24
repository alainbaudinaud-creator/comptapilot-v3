from database import engine
from sqlalchemy import text


sql = """
CREATE TABLE IF NOT EXISTS actions_history_v3 (
    id SERIAL PRIMARY KEY,
    module TEXT NOT NULL,
    action TEXT NOT NULL,
    statut TEXT DEFAULT 'ok',
    societe_id INTEGER,
    reference_type TEXT,
    reference_id INTEGER,
    message TEXT,
    metadata TEXT,
    created_by TEXT DEFAULT 'system',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Table actions_history_v3 OK")
