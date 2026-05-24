from database import engine
from sqlalchemy import text


sql = """
ALTER TABLE relances_client_v3
ADD COLUMN IF NOT EXISTS email_to TEXT;

ALTER TABLE relances_client_v3
ADD COLUMN IF NOT EXISTS email_subject TEXT;

ALTER TABLE relances_client_v3
ADD COLUMN IF NOT EXISTS email_body TEXT;

ALTER TABLE relances_client_v3
ADD COLUMN IF NOT EXISTS email_status TEXT DEFAULT 'non_prepare';
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Colonnes email relances OK")
