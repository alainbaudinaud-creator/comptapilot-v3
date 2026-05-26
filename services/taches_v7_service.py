import sqlite3
from datetime import datetime

from services.db import get_connection
from services.audit_service import ajouter_log
from services.log_service import log_info, log_erreur
from services.robots_metiers_service import executer_robot_par_type


def initialiser_taches_v7():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS taches_automatiques_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            type_tache TEXT,
            frequence TEXT,
            statut TEXT,
            date_creation TEXT
        )
    """)

    conn.commit()
    conn.close()


def lister_taches_actives():

    initialiser_taches_v7()

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            nom,
            type_tache,
            frequence,
            statut,
            date_creation
        FROM taches_automatiques_v7
        WHERE statut = 'ACTIVE'
        ORDER BY id DESC
    """)

    taches = c.fetchall()

    conn.close()

    return taches


def executer_taches_actives():

    taches = lister_taches_actives()

    for tache in taches:

        tache_id = tache[0]
        nom = tache[1]
        type_tache = tache[2]

        try:

            message = (
                f"Exécution tâche V7 #{tache_id} "
                f"- {nom} ({type_tache})"
            )

            log_info(message)

            ajouter_log(
                "EXECUTION_TACHE_V7",
                message
            )

            executer_robot_par_type(type_tache)

        except Exception as erreur:

            log_erreur(
                f"Erreur tâche V7 #{tache_id} : {erreur}"
            )
def creer_tache_v7(nom, type_tache, frequence):
    connexion = sqlite3.connect('comptapilot.db')

    curseur = connexion.cursor()

    curseur.execute("""
        INSERT INTO taches_v7 (
            nom,
            type_tache,
            frequence,
            statut,
            date_creation
        )
        VALUES (?, ?, ?, ?, datetime('now'))
    """, (
        nom,
        type_tache,
        frequence,
        'ACTIVE'
    ))

    connexion.commit()

    tache_id = curseur.lastrowid

    connexion.close()

    return tache_id
def recuperer_tache_v7_par_id(tache_id):
    connexion = sqlite3.connect('comptapilot.db')

    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            id,
            nom,
            type_tache,
            frequence,
            statut,
            date_creation
        FROM taches_v7
        WHERE id = ?
    """, (tache_id,))

    tache = curseur.fetchone()

    connexion.close()

    return tache
def modifier_tache_v7(tache_id, nom, type_tache, frequence, statut):
    connexion = sqlite3.connect('comptapilot.db')
    curseur = connexion.cursor()

    curseur.execute("""
        UPDATE taches_v7
        SET
            nom = ?,
            type_tache = ?,
            frequence = ?,
            statut = ?
        WHERE id = ?
    """, (
        nom,
        type_tache,
        frequence,
        statut,
        tache_id
    ))

    connexion.commit()

    lignes_modifiees = curseur.rowcount

    connexion.close()

    return lignes_modifiees

def supprimer_tache_v7(tache_id):
    connexion = sqlite3.connect('comptapilot.db')

    curseur = connexion.cursor()

    curseur.execute("""
        DELETE FROM taches_v7
        WHERE id = ?
    """, (tache_id,))

    connexion.commit()

    lignes_supprimees = curseur.rowcount

    connexion.close()

    return lignes_supprimees

