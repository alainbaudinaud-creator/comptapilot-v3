import sqlite3

from db_core.settings import SQLITE_DB

def get_sqlite_connection():
    return sqlite3.connect(SQLITE_DB)

