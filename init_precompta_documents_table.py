from database import engine
from sqlalchemy import text


sql = """
CREATE TABLE IF NOT EXISTS precompta_documents (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL,
    societe_id INTEGER,
    fournisseur TEXT,
    type_document TEXT,
    date_document TEXT,
    montant_ht NUMERIC(12,2),
    montant_tva NUMERIC(12,2),
    montant_ttc NUMERIC(12,2),
    compte_charge TEXT,
    compte_tva TEXT,
    compte_fournisseur TEXT,
    confiance NUMERIC(5,2),
    statut_validation TEXT DEFAULT 'a_valider',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Table precompta_documents OK")


