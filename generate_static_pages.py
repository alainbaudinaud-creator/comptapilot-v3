from pathlib import Path
from html import escape
from sqlalchemy import text
from database import engine

OUT = Path("/var/www/html")

STYLE = """
<style>
body{background:#050816;color:white;font-family:Arial;padding:40px}
h1{font-size:42px}
.card{background:#11182d;border-radius:18px;padding:22px;margin-bottom:24px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-bottom:24px}
.kpi{background:#11182d;border-radius:18px;padding:22px}
.kpi b{font-size:30px}
table{width:100%;border-collapse:collapse;background:#11182d;border-radius:18px;overflow:hidden}
th,td{padding:14px;border-bottom:1px solid #24304f;text-align:left}
th{background:#17203b;color:#8fa3c7}
a{color:#22d3ee}
</style>
"""

def write_page(filename, title, body):
    html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{escape(title)}</title>
{STYLE}
</head>
<body>
<h1>{escape(title)}</h1>
<div class="card">
<p>ComptaPilot V3 — page générée automatiquement depuis PostgreSQL.</p>
<p>
<a href="/public-ecritures-v3">Écritures</a> ·
<a href="/public-balance-v3">Balance</a> ·
<a href="/public-grand-livre-v3">Grand livre</a> ·
<a href="/public-dashboard-v3">Dashboard</a>
</p>
</div>
{body}
</body>
</html>"""
    (OUT / filename).write_text(html, encoding="utf-8")

def ensure_data():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ecritures (
                id SERIAL PRIMARY KEY,
                journal VARCHAR(20),
                compte VARCHAR(20),
                libelle TEXT,
                debit NUMERIC(14,2) DEFAULT 0,
                credit NUMERIC(14,2) DEFAULT 0,
                date_ecriture DATE DEFAULT CURRENT_DATE
            )
        """))
        count = conn.execute(text("SELECT COUNT(*) FROM ecritures")).scalar()
        if count == 0:
            conn.execute(text("""
                INSERT INTO ecritures (journal, compte, libelle, debit, credit)
                VALUES
                ('ACH', '607000', 'Achat marchandises démonstration', 1200.00, 0),
                ('ACH', '445660', 'TVA déductible démonstration', 240.00, 0),
                ('ACH', '401000', 'Fournisseur démonstration', 0, 1440.00)
            """))

def page_ecritures():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, journal, compte, libelle, debit, credit, date_ecriture
            FROM ecritures
            ORDER BY id DESC
            LIMIT 200
        """)).fetchall()

    body = "<table><tr><th>ID</th><th>Journal</th><th>Compte</th><th>Libellé</th><th>Débit</th><th>Crédit</th><th>Date</th></tr>"
    for r in rows:
        body += (
            "<tr>"
            f"<td>{r[0]}</td><td>{escape(str(r[1] or ''))}</td><td>{escape(str(r[2] or ''))}</td>"
            f"<td>{escape(str(r[3] or ''))}</td><td>{r[4] or 0}</td><td>{r[5] or 0}</td><td>{r[6] or ''}</td>"
            "</tr>"
        )
    body += "</table>"
    write_page("ecritures-v3.html", "Écritures Comptables V3", body)

def page_balance():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT compte, SUM(debit) AS debit, SUM(credit) AS credit, SUM(debit-credit) AS solde
            FROM ecritures
            GROUP BY compte
            ORDER BY compte
        """)).fetchall()

    body = "<table><tr><th>Compte</th><th>Débit</th><th>Crédit</th><th>Solde</th></tr>"
    for r in rows:
        body += f"<tr><td>{escape(str(r[0] or ''))}</td><td>{r[1] or 0}</td><td>{r[2] or 0}</td><td>{r[3] or 0}</td></tr>"
    body += "</table>"
    write_page("balance-v3.html", "Balance Comptable V3", body)

def page_grand_livre():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT compte, date_ecriture, journal, libelle, debit, credit
            FROM ecritures
            ORDER BY compte, date_ecriture, id
        """)).fetchall()

    body = "<table><tr><th>Compte</th><th>Date</th><th>Journal</th><th>Libellé</th><th>Débit</th><th>Crédit</th></tr>"
    for r in rows:
        body += (
            f"<tr><td>{escape(str(r[0] or ''))}</td><td>{r[1] or ''}</td><td>{escape(str(r[2] or ''))}</td>"
            f"<td>{escape(str(r[3] or ''))}</td><td>{r[4] or 0}</td><td>{r[5] or 0}</td></tr>"
        )
    body += "</table>"
    write_page("grand-livre-v3.html", "Grand Livre V3", body)

def page_dashboard():
    with engine.begin() as conn:
        k = conn.execute(text("""
            SELECT COUNT(*) nb, COALESCE(SUM(debit),0) debit, COALESCE(SUM(credit),0) credit, COALESCE(SUM(debit-credit),0) solde
            FROM ecritures
        """)).fetchone()

    body = f"""
<div class="grid">
<div class="kpi">Écritures<br><b>{k[0]}</b></div>
<div class="kpi">Total débit<br><b>{k[1]}</b></div>
<div class="kpi">Total crédit<br><b>{k[2]}</b></div>
<div class="kpi">Solde<br><b>{k[3]}</b></div>
</div>
"""
    write_page("dashboard-v3-public.html", "Dashboard ComptaPilot V3", body)

if __name__ == "__main__":
    ensure_data()
    page_ecritures()
    page_balance()
    page_grand_livre()
    page_dashboard()
    print("Pages V3 générées")
