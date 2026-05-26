
import re
import sqlite3
import urllib.request
import ssl
import certifi
from pathlib import Path

import fitz  # PyMuPDF

DB = r"C:\Users\alain\mon-projet-agent\db.sqlite"
PDF_URL = "https://www.anc.gouv.fr/files/anc/files/1_Normes_fran%C3%A7aises/Plans%20comptables/2026/Plan-de-comptes-2026.pdf"
PDF_PATH = Path(r"C:\Users\alain\mon-projet-agent\Plan-de-comptes-2026-ANC.pdf")

print("Telechargement du plan comptable officiel ANC 2026...")
ssl_context = ssl.create_default_context(cafile=certifi.where())

with urllib.request.urlopen(PDF_URL, context=ssl_context) as response:
    with open(PDF_PATH, "wb") as f:
        f.write(response.read())

print("Extraction du PDF...")
doc = fitz.open(PDF_PATH)

texte = ""
for page in doc:
    texte += page.get_text("text") + "\n"

doc.close()

lignes = []
for raw in texte.splitlines():
    line = " ".join(raw.strip().split())
    if not line:
        continue

    # Capture comptes type 101, 1011, 44566, 68112, etc.
    m = re.match(r"^([1-8][0-9]{1,7})[.\s-]+(.+)$", line)
    if m:
        numero = m.group(1).strip()
        libelle = m.group(2).strip()

        if len(numero) >= 2 and libelle and not libelle.lower().startswith("page"):
            lignes.append((numero, libelle))

# Dedoublonnage en conservant le premier libelle
pcg = {}
for numero, libelle in lignes:
    if numero not in pcg:
        pcg[numero] = libelle

if len(pcg) < 100:
    raise SystemExit(f"Extraction insuffisante : seulement {len(pcg)} comptes detectes.")

def type_compte(numero):
    if numero.startswith("1"):
        return "Capitaux"
    if numero.startswith("2"):
        return "Immobilisations"
    if numero.startswith("3"):
        return "Stocks"
    if numero.startswith("4"):
        return "Tiers"
    if numero.startswith("5"):
        return "Financiers"
    if numero.startswith("6"):
        return "Charges"
    if numero.startswith("7"):
        return "Produits"
    if numero.startswith("8"):
        return "Speciaux"
    return "Autre"

conn = sqlite3.connect(DB)
c = conn.cursor()

try:
    c.execute("ALTER TABLE plan_comptable ADD COLUMN dossier_id INTEGER DEFAULT 1")
except Exception:
    pass

c.execute("""
CREATE TABLE IF NOT EXISTS pcg_modele_2026 (
    numero TEXT PRIMARY KEY,
    libelle TEXT,
    type TEXT,
    source TEXT DEFAULT 'ANC 2026'
)
""")

for numero, libelle in pcg.items():
    c.execute("""
        INSERT OR REPLACE INTO pcg_modele_2026 (numero, libelle, type, source)
        VALUES (?, ?, ?, ?)
    """, (numero, libelle, type_compte(numero), "ANC 2026"))

c.execute("SELECT id FROM dossiers_comptables ORDER BY id")
dossiers = [r[0] for r in c.fetchall()]

if not dossiers:
    dossiers = [1]

insertions = 0

for dossier_id in dossiers:
    for numero, libelle in pcg.items():
        c.execute("""
            SELECT id
            FROM plan_comptable
            WHERE numero=?
              AND COALESCE(dossier_id,1)=?
        """, (numero, dossier_id))

        if not c.fetchone():
            c.execute("""
                INSERT INTO plan_comptable (numero, libelle, type, dossier_id)
                VALUES (?, ?, ?, ?)
            """, (numero, libelle, type_compte(numero), dossier_id))
            insertions += 1

conn.commit()
conn.close()

print("Plan comptable ANC 2026 importe.")
print("Comptes modele :", len(pcg))
print("Dossiers alimentes :", len(dossiers))
print("Comptes ajoutes dans plan_comptable :", insertions)

