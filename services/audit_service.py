from datetime import datetime
from services.db import get_connection


def initialiser_audit_log():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            detail TEXT,
            date_action TEXT
        )
    """)

    conn.commit()
    conn.close()


def ajouter_log(action, detail):
    initialiser_audit_log()

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO audit_log (action, detail, date_action)
        VALUES (?, ?, ?)
    """, (
        action,
        detail,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def lister_logs(limit=100):
    initialiser_audit_log()

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT id, action, detail, date_action
        FROM audit_log
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    logs = c.fetchall()
    conn.close()

    return logs


