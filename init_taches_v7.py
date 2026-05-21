import sqlite3

connexion = sqlite3.connect("comptapilot.db")
curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS taches_v7 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    type_tache TEXT NOT NULL,
    frequence TEXT NOT NULL,
    statut TEXT NOT NULL DEFAULT 'ACTIVE',
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

connexion.commit()
connexion.close()

print("Table taches_v7 créée ou déjà existante.")
