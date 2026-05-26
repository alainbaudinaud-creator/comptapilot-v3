import sqlite3

HASH_BCRYPT_ICI = "$2b$12$NT.jQn855SnYXrpsUlN63Oewgo1wU9YjD54tpugtUYqm2u9PxXj7S"

connexion = sqlite3.connect("comptapilot.db")
curseur = connexion.cursor()

curseur.execute("""
    UPDATE utilisateurs
    SET password = ?
    WHERE username = 'admin'
""", (HASH_BCRYPT_ICI,))

connexion.commit()
connexion.close()

print("Mot de passe admin mis à jour.")

