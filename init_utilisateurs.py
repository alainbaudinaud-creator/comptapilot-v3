import sqlite3

connexion = sqlite3.connect("comptapilot.db")
curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    actif INTEGER NOT NULL DEFAULT 1,
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

curseur.execute("""
INSERT OR IGNORE INTO utilisateurs (
    username,
    password,
    role,
    actif
)
VALUES (?, ?, ?, ?)
""", (
    "admin",
    "admin123",
    "ADMIN",
    1
))

connexion.commit()
connexion.close()

print("Table utilisateurs créée avec utilisateur admin.")
