import sqlite3

conn = sqlite3.connect("db.sqlite")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER,
    role_id INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER,
    permission TEXT
)
""")

c.execute("""
INSERT OR IGNORE INTO roles (id, nom)
VALUES
(1, 'ADMIN'),
(2, 'COMPTABLE'),
(3, 'LECTURE'),
(4, 'AUDIT'),
(5, 'RGPD')
""")

c.execute("""
INSERT INTO user_roles (user_id, role_id)
SELECT 1, 1
WHERE NOT EXISTS (
    SELECT 1
    FROM user_roles
    WHERE user_id = 1
    AND role_id = 1
)
""")

conn.commit()
conn.close()

print("Tables rôles créées")
