import os
from sqlalchemy import create_engine, text

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    print("\n=== TABLES POSTGRES ===\n")

    rows = conn.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))

    tables = [r[0] for r in rows]

    for t in tables:
        print("-", t)

    print("\n=== COUNTS ===\n")

    for t in tables:
        c = conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar()
        print(f"{t}: {c}")
