
import sqlite3

DB = "db.sqlite"

conn = sqlite3.connect(DB)
c = conn.cursor()

def get_compte_id(numero, libelle, type_compte):
    c.execute("SELECT id FROM plan_comptable WHERE numero=?", (numero,))
    row = c.fetchone()

    if row:
        return row[0]

    c.execute("""
        INSERT INTO plan_comptable (numero, libelle, type)
        VALUES (?, ?, ?)
    """, (numero, libelle, type_compte))

    return c.lastrowid


compte_fournisseur_id = get_compte_id("401000", "Fournisseurs", "Passif")

c.execute("""
    SELECT
        piece,
        MIN(date_ecriture),
        MIN(libelle),
        ROUND(SUM(COALESCE(debit, 0)), 2),
        ROUND(SUM(COALESCE(credit, 0)), 2)
    FROM ecritures
    WHERE piece IS NOT NULL
      AND piece <> ''
    GROUP BY piece
    HAVING ROUND(SUM(COALESCE(debit, 0)) - SUM(COALESCE(credit, 0)), 2) <> 0
""")

pieces = c.fetchall()

corrections = 0

for piece, date_ecriture, libelle, total_debit, total_credit in pieces:

    ecart = round((total_debit or 0) - (total_credit or 0), 2)

    if ecart > 0:
        c.execute("""
            INSERT INTO ecritures
            (
                journal,
                date_ecriture,
                compte_id,
                piece,
                libelle,
                debit,
                credit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "OD",
            date_ecriture,
            compte_fournisseur_id,
            piece,
            "Correction ?quilibre automatique - " + str(libelle or piece),
            0,
            ecart
        ))

        corrections += 1

    elif ecart < 0:
        c.execute("""
            INSERT INTO ecritures
            (
                journal,
                date_ecriture,
                compte_id,
                piece,
                libelle,
                debit,
                credit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "OD",
            date_ecriture,
            compte_fournisseur_id,
            piece,
            "Correction ?quilibre automatique - " + str(libelle or piece),
            abs(ecart),
            0
        ))

        corrections += 1

conn.commit()
conn.close()

print(f"{corrections} corrections d'?quilibre cr??es.")

