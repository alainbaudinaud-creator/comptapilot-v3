import sqlite3


def recuperer_utilisateur_par_username(username):
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            id,
            username,
            password,
            role,
            actif
        FROM utilisateurs
        WHERE username = ?
    """, (username,))

    utilisateur = curseur.fetchone()

    connexion.close()

    return utilisateur
def recuperer_utilisateur_par_id(utilisateur_id):
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            id,
            username,
            password,
            role,
            actif
        FROM utilisateurs
        WHERE id = ?
    """, (utilisateur_id,))

    utilisateur = curseur.fetchone()

    connexion.close()

    return utilisateur
def creer_utilisateur(username, password_hash, role):
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        INSERT INTO utilisateurs (
            username,
            password,
            role,
            actif
        )
        VALUES (?, ?, ?, ?)
    """, (
        username,
        password_hash,
        role,
        1
    ))

    connexion.commit()

    utilisateur_id = curseur.lastrowid

    connexion.close()

    return utilisateur_id
def lister_utilisateurs():
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            id,
            username,
            role,
            actif,
            date_creation
        FROM utilisateurs
        ORDER BY id DESC
    """)

    utilisateurs = curseur.fetchall()

    connexion.close()

    return utilisateurs
def desactiver_utilisateur(utilisateur_id):
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        UPDATE utilisateurs
        SET actif = 0
        WHERE id = ?
    """, (utilisateur_id,))

    connexion.commit()

    connexion.close()
def modifier_role_utilisateur(utilisateur_id, role):
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        UPDATE utilisateurs
        SET role = ?
        WHERE id = ?
    """, (
        role,
        utilisateur_id
    ))

    connexion.commit()
    connexion.close()
def modifier_password_utilisateur(utilisateur_id, password_hash):
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        UPDATE utilisateurs
        SET password = ?
        WHERE id = ?
    """, (
        password_hash,
        utilisateur_id
    ))

    connexion.commit()
    connexion.close()
def supprimer_utilisateur(utilisateur_id):
    connexion = sqlite3.connect("comptapilot.db")
    curseur = connexion.cursor()

    curseur.execute("""
        DELETE FROM utilisateurs
        WHERE id = ?
    """, (utilisateur_id,))

    connexion.commit()
    connexion.close()


