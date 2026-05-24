from database import engine
from sqlalchemy import text


sql = """
ALTER TABLE documents
ADD COLUMN IF NOT EXISTS ocr_text TEXT;

ALTER TABLE documents
ADD COLUMN IF NOT EXISTS ocr_error TEXT;

ALTER TABLE documents
ADD COLUMN IF NOT EXISTS ocr_processed_at TIMESTAMP;
"""


with engine.begin() as conn:
    conn.execute(text(sql))

print("Colonnes OCR documents OK")
