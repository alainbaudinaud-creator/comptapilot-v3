from flask import Blueprint, render_template, request, redirect, flash
from controllers.auth import login_required
from datetime import datetime
from services.db import get_connection

ia_v7_routes = Blueprint('ia_v7', __name__)

@ia_v7_routes.route('/orchestration-ia-v7')
@login_required
def orchestration_ia_v7():
    return render_template('orchestration_ia_v7.html')


@ia_v7_routes.route('/taches-automatiques-v7', methods=['GET', 'POST'])
@login_required
def taches_automatiques_v7():
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

    if request.method == 'POST':
        nom = request.form.get('nom')
        type_tache = request.form.get('type_tache')
        frequence = request.form.get('frequence')

        c.execute("""
            INSERT INTO taches_automatiques_v7 (
                nom, type_tache, frequence, statut, date_creation
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            nom,
            type_tache,
            frequence,
            "ACTIVE",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()
        flash("Tâche automatique créée")
        return redirect('/ecritures/taches-automatiques-v7')

    c.execute("""
        SELECT id, nom, type_tache, frequence, statut, date_creation
        FROM taches_automatiques_v7
        ORDER BY id DESC
    """)

    taches = c.fetchall()
    conn.close()

    return render_template('taches_automatiques_v7.html', taches=taches)


@ia_v7_routes.route('/notifications-internes-v7', methods=['GET', 'POST'])
@login_required
def notifications_internes_v7():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS notifications_internes_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destinataire TEXT,
            message TEXT,
            statut TEXT,
            date_creation TEXT
        )
    """)

    if request.method == 'POST':
        destinataire = request.form.get('destinataire')
        message = request.form.get('message')

        c.execute("""
            INSERT INTO notifications_internes_v7 (
                destinataire, message, statut, date_creation
            )
            VALUES (?, ?, ?, ?)
        """, (
            destinataire,
            message,
            "NON_LUE",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()
        flash("Notification créée")
        return redirect('/ecritures/notifications-internes-v7')

    c.execute("""
        SELECT id, destinataire, message, statut, date_creation
        FROM notifications_internes_v7
        ORDER BY id DESC
    """)

    notifications = c.fetchall()
    conn.close()

    return render_template(
        'notifications_internes_v7.html',
        notifications=notifications
    )


@ia_v7_routes.route('/previsions-ia-v7')
@login_required
def previsions_ia_v7():
    previsions = []
    return render_template('previsions_ia_v7.html', previsions=previsions)
@ia_v7_routes.route('/supervision-scheduler-v7')
@login_required
def supervision_scheduler_v7():

    logs = []

    try:
        with open(
            "C:/Users/alain/mon-projet-agent/logs/application.log",
            "r",
            encoding="utf-8"
        ) as fichier:
            logs = fichier.readlines()[-50:]
    except FileNotFoundError:
        logs = ["Aucun log disponible"]

    return render_template(
        'supervision_scheduler_v7.html',
        logs=logs
    )
@ia_v7_routes.route('/supervision-robots-v7')
@login_required
def supervision_robots_v7():

    logs = []

    try:
        with open(
            "C:/Users/alain/mon-projet-agent/logs/application.log",
            "r",
            encoding="utf-8"
        ) as fichier:
            lignes = fichier.readlines()
            logs = [
                ligne for ligne in lignes
                if "Robot" in ligne or "IA comptable" in ligne or "Surveillance trésorerie" in ligne
            ][-100:]

    except FileNotFoundError:
        logs = ["Aucun log disponible"]

    return render_template(
        'supervision_robots_v7.html',
        logs=logs
    )

