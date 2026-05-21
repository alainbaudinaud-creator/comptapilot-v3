from pathlib import Path
import re

source = Path(r"C:\Users\alain\mon-projet-agent\dump.sql")
target = Path(r"C:\Users\alain\mon-projet-agent\dump_postgres.sql")

sql = source.read_text(encoding="utf-8", errors="ignore")

sql = sql.replace("PRAGMA foreign_keys=OFF;", "")
sql = sql.replace("BEGIN TRANSACTION;", "BEGIN;")
sql = sql.replace("AUTOINCREMENT", "")
sql = sql.replace("INTEGER PRIMARY KEY", "SERIAL PRIMARY KEY")

sql = re.sub(r"CREATE TABLE sqlite_sequence\s*\(.*?\);", "", sql, flags=re.DOTALL)
sql = re.sub(r"INSERT INTO sqlite_sequence VALUES\(.*?\);", "", sql)

target.write_text(sql, encoding="utf-8")

print("Conversion PostgreSQL OK")

