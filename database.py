import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.getenv("POSTGRES_USER", "comptapilot")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "comptapilot")
POSTGRES_DB = os.getenv("POSTGRES_DB", "comptapilot")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@postgres:5432/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Compatibilité API dynamique ComptaPilot V3
def get_db_connection():
    return engine.raw_connection()
