from flask import Blueprint, redirect, render_template_string, session
from sqlalchemy import text
from database import engine

bp_socle_donnees = Blueprint("socle_donnees", __name__)


@bp_socle_donnees.route("/socle-donnees-v3")
def socle_donnees_index():

    if not session.get("user_id"):
        return redirect("/login")

    tables = {
        "clients": "clients_v3",
        "exercices": "exercices_v3",
        "journaux": "journaux_v3",
        "ecritures": "ecritures_v3",
        "lignes": "lignes_ecritures_v3",
        "factures": "factures_v3",
        "pieces": "pieces_v3",
        "imports": "imports_v3",
        "workflow": "workflow_cabinet_v3",
        "taches": "taches_cabinet_v3",
    }

    stats = {}

    with engine.connect() as conn:
        for label, table in tables.items():
            try:
                stats[label] = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0
            except Exception:
                stats[label] = 0

    return render_template_string("""
    <!doctype html>
    <html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Socle Données V3 - ComptaPilot</title>
        <style>
            body { margin:0; font-family:Arial, sans-serif; background:#020617; color:#e5e7eb; }
            .page { padding:32px; }
            .hero { background:linear-gradient(135deg,#111827,#2563eb); padding:30px; border-radius:24px; margin-bottom:24px; }
            .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }
            .card { background:#0f172a; border:1px solid #334155; border-radius:18px; padding:20px; }
            .num { font-size:34px; font-weight:bold; color:#93c5fd; }
            a { color:#bfdbfe; }
        </style>
    </head>
    <body>
        <main class="page">
            <section class="hero">
                <h1>Socle Données Comptables V3</h1>
                <p>Base métier centrale : clients, exercices, journaux, écritures, factures, pièces, imports, workflow et tâches cabinet.</p>
            </section>

            <section class="grid">
                {% for label, value in stats.items() %}
                <div class="card">
                    <div>{{ label }}</div>
                    <div class="num">{{ value }}</div>
                </div>
                {% endfor %}
            </section>

            <p style="margin-top:28px;"><a href="/">← Retour accueil</a></p>
        </main>
    </body>
    </html>
    """, stats=stats)

