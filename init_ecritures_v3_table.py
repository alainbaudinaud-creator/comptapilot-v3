from database import engine
from sqlalchemy import text


sql = """
CREATE TABLE IF NOT EXISTS ecritures_v3 (
    id SERIAL PRIMARY KEY,
    precompta_id INTEGER NOT NULL,
    document_id INTEGER,
    societe_id INTEGER,
    date_ecriture TEXT,
    libelle TEXT,
    compte TEXT,
    debit NUMERIC(12,2) DEFAULT 0,
    credit NUMERIC(12,2) DEFAULT 0,
    journal TEXT DEFAULT 'ACH',
    source TEXT DEFAULT 'precompta_v3',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Table ecritures_v3 OK")


