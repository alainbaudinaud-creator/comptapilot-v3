from database import engine
from sqlalchemy import text


sql = """
ALTER TABLE precompta_documents
ADD COLUMN IF NOT EXISTS commentaire_validation TEXT;

ALTER TABLE precompta_documents
ADD COLUMN IF NOT EXISTS validated_at TIMESTAMP;

ALTER TABLE precompta_documents
ADD COLUMN IF NOT EXISTS validated_by TEXT;
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Colonnes validation précompta OK")
