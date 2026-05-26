from database import engine
from database import SessionLocal

def get_engine():
    return engine

def get_session():
    return SessionLocal()


