import sqlite3

conn = sqlite3.connect("db.sqlite")
c = conn.cursor()

permissions = [

    # DASHBOARD
    (1, "ACCESS_DASHBOARD"),

    # ECRITURES
    (1, "ACCESS_ECRITURES"),
    (2, "ACCESS_ECRITURES"),

    # EXPORT
    (1, "ACCESS_EXPORT"),
    (2, "ACCESS_EXPORT"),

    # TVA
    (1, "ACCESS_TVA"),
    (2, "ACCESS_TVA"),

    # BILAN
    (1, "ACCESS_BILAN"),
    (2, "ACCESS_BILAN"),

    # JOURNAUX
    (1, "ACCESS_JOURNAUX"),
    (2, "ACCESS_JOURNAUX"),
    (4, "ACCESS_JOURNAUX"),

    # IMPORT
    (1, "ACCESS_IMPORT"),
    (2, "ACCESS_IMPORT"),

    # CLOTURE
    (1, "ACCESS_CLOTURE"),

    # RGPD
    (1, "ACCESS_RGPD"),
    (5, "ACCESS_RGPD"),

    # ADMIN
    (1, "ACCESS_ADMIN")
]

for role_id, permission in permissions:

    c.execute("""
        INSERT INTO role_permissions (role_id, permission)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1
            FROM role_permissions
            WHERE role_id = ?
            AND permission = ?
        )
    """, (role_id, permission, role_id, permission))

conn.commit()
conn.close()

print("Permissions injectées")
