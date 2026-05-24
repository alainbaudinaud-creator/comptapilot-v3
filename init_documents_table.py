from database import engine
from sqlalchemy import text


sql = """
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    societe_id INTEGER,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    mime_type TEXT,
    file_size INTEGER,
    statut_ocr TEXT DEFAULT 'en_attente',
    statut_precompta TEXT DEFAULT 'en_attente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Table documents OK")
