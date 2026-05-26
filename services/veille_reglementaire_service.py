
import sqlite3
import urllib.request
from pathlib import Path
from datetime import datetime

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"
BASE_DOCS = ROOT / "documents_officiels" / "liasse_fiscale_2026"

BASE_DOCS.mkdir(parents=True, exist_ok=True)

SOURCES_DGFIP = [
    {
        "code": "2033-SD",
        "type": "LIASSE_RSI",
        "millesime": "2026",
        "url": "https://www.impots.gouv.fr/sites/default/files/formulaires/2033-sd/2026/2033-sd_5394.pdf",
        "fichier": "2033-SD_Liasse_RSI_2026.pdf",
        "description": "Liasse fiscale régime réel simplifié 2033-A à 2033-G",
    },
    {
        "code": "2033-NOT-SD",
        "type": "NOTICE_RSI",
        "millesime": "2026",
        "url": "https://www.impots.gouv.fr/sites/default/files/formulaires/2033-sd/2026/2033-sd_5395.pdf",
        "fichier": "2033-NOT-SD_Notice_RSI_2026.pdf",
        "description": "Notice officielle liasse régime simplifié",
    },
    {
        "code": "2050-LIASSE",
        "type": "LIASSE_RN",
        "millesime": "2026",
        "url": "https://www.impots.gouv.fr/sites/default/files/formulaires/2050-liasse/2026/2050-liasse_5320.pdf",
        "fichier": "2050-LIASSE_Regime_Reel_Normal_2026.pdf",
        "description": "Liasse fiscale régime réel normal 2050 à 2059-G",
    },
    {
        "code": "2032-NOT-SD",
        "type": "NOTICE_RN",
        "millesime": "2026",
        "url": "https://www.impots.gouv.fr/sites/default/files/formulaires/2032-not-sd/2026/2032-not-sd_5323.pdf",
        "fichier": "2032-NOT-SD_Notice_Regime_Normal_2026.pdf",
        "description": "Notice officielle liasse régime réel normal",
    },
    {
        "code": "2065-SD",
        "type": "IS",
        "millesime": "2026",
        "url": "https://www.impots.gouv.fr/sites/default/files/formulaires/2065-sd/2026/2065-sd_5381.pdf",
        "fichier": "2065-SD_Impot_Societes_2026.pdf",
        "description": "Déclaration impôt sur les sociétés",
    },
    {
        "code": "EDI-TDFC-V4",
        "type": "EDI_TDFC",
        "millesime": "2026",
        "url": "https://www.impots.gouv.fr/sites/default/files/media/1_metier/3_partenaire/edi/cdc_edi_tdfc/2026/volume_iv_tdfc_2026.pdf",
        "fichier": "EDI_TDFC_2026_Volume_IV_Guide_Utilisateur.pdf",
        "description": "Guide utilisateur EDI-TDFC 2026",
    },
]

def init_tables():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS veille_reglementaire (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        type_document TEXT,
        millesime TEXT,
        description TEXT,
        url TEXT,
        fichier TEXT,
        statut TEXT,
        derniere_verification TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS obligations_fiscales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        libelle TEXT,
        regime TEXT,
        periodicite TEXT,
        obligatoire INTEGER DEFAULT 1,
        source TEXT,
        actif INTEGER DEFAULT 1
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS mapping_liasse_fiscale (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        formulaire TEXT,
        case_fiscale TEXT,
        libelle TEXT,
        comptes TEXT,
        sens TEXT,
        regime TEXT
    )
    """)

    con.commit()
    con.close()

def seed_obligations():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    obligations = [
        ("2033", "Liasse fiscale régime réel simplifié", "RSI", "ANNUELLE", "DGFiP"),
        ("2050", "Liasse fiscale régime réel normal", "RN", "ANNUELLE", "DGFiP"),
        ("2065", "Déclaration impôt sur les sociétés", "IS", "ANNUELLE", "DGFiP"),
        ("FEC", "Fichier des écritures comptables", "TOUS", "A LA DEMANDE", "DGFiP"),
        ("EDI-TDFC", "Télétransmission fiscale EDI-TDFC", "TOUS", "ANNUELLE", "DGFiP"),
    ]

    for code, libelle, regime, periodicite, source in obligations:
        cur.execute("""
        INSERT INTO obligations_fiscales (code, libelle, regime, periodicite, source)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM obligations_fiscales WHERE code=? AND regime=?
        )
        """, (code, libelle, regime, periodicite, source, code, regime))

    mappings = [
        ("2033-A", "ACTIF_IMMO", "Immobilisations", "2", "DEBIT", "RSI"),
        ("2033-A", "ACTIF_CREANCES", "Créances", "411,44566", "DEBIT", "RSI"),
        ("2033-A", "ACTIF_DISPONIBILITES", "Disponibilités", "512,53", "DEBIT", "RSI"),
        ("2033-A", "PASSIF_CAPITAUX", "Capitaux propres", "101,106,120,129", "CREDIT", "RSI"),
        ("2033-A", "PASSIF_DETTES", "Dettes fournisseurs et fiscales", "401,44571", "CREDIT", "RSI"),
        ("2033-B", "PRODUITS_EXPLOITATION", "Produits d'exploitation", "7", "CREDIT", "RSI"),
        ("2033-B", "CHARGES_EXPLOITATION", "Charges d'exploitation", "6", "DEBIT", "RSI"),
        ("2050", "ACTIF_IMMOBILISE", "Actif immobilisé", "2", "DEBIT", "RN"),
        ("2051", "PASSIF_CAPITAUX", "Capitaux propres", "1", "CREDIT", "RN"),
        ("2052", "RESULTAT_PRODUITS", "Produits", "7", "CREDIT", "RN"),
        ("2052", "RESULTAT_CHARGES", "Charges", "6", "DEBIT", "RN"),
    ]

    for formulaire, case_fiscale, libelle, comptes, sens, regime in mappings:
        cur.execute("""
        INSERT INTO mapping_liasse_fiscale
        (formulaire, case_fiscale, libelle, comptes, sens, regime)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM mapping_liasse_fiscale
            WHERE formulaire=? AND case_fiscale=? AND regime=?
        )
        """, (
            formulaire, case_fiscale, libelle, comptes, sens, regime,
            formulaire, case_fiscale, regime
        ))

    con.commit()
    con.close()

def verifier_et_telecharger():
    init_tables()
    seed_obligations()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    resultats = []

    for src in SOURCES_DGFIP:
        cible = BASE_DOCS / src["fichier"]
        statut = "DEJA_PRESENT"

        if not cible.exists() or cible.stat().st_size == 0:
            try:
                urllib.request.urlretrieve(src["url"], cible)
                statut = "TELECHARGE"
            except Exception as e:
                statut = "ERREUR: " + str(e)

        cur.execute("""
        INSERT INTO veille_reglementaire
        (code, type_document, millesime, description, url, fichier, statut, derniere_verification)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            src["code"],
            src["type"],
            src["millesime"],
            src["description"],
            src["url"],
            str(cible),
            statut,
            datetime.now().isoformat(timespec="seconds")
        ))

        resultats.append((src["code"], statut, str(cible)))

    con.commit()
    con.close()

    return resultats

def remplir_liasse_depuis_comptabilite(exercice="2026", regime="RSI"):
    init_tables()
    seed_obligations()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    mappings = cur.execute("""
        SELECT formulaire, case_fiscale, libelle, comptes, sens, regime
        FROM mapping_liasse_fiscale
        WHERE regime=?
        ORDER BY formulaire, case_fiscale
    """, (regime,)).fetchall()

    cur.execute("DELETE FROM liasse_fiscale WHERE exercice=?", (exercice,))

    for formulaire, case_fiscale, libelle, comptes, sens, regime in mappings:
        prefixes = [c.strip() for c in comptes.split(",") if c.strip()]
        total = 0.0

        for prefix in prefixes:
            rows = cur.execute("""
                SELECT pc.numero, SUM(e.debit) AS debit, SUM(e.credit) AS credit
                FROM ecritures e
                LEFT JOIN plan_comptable pc ON pc.id=e.compte_id
                WHERE pc.numero LIKE ?
                GROUP BY pc.numero
            """, (prefix + "%",)).fetchall()

            for numero, debit, credit in rows:
                debit = float(debit or 0)
                credit = float(credit or 0)

                if sens == "DEBIT":
                    total += debit - credit
                else:
                    total += credit - debit

        cur.execute("""
        INSERT INTO liasse_fiscale (exercice, formulaire, case_fiscale, valeur)
        VALUES (?, ?, ?, ?)
        """, (exercice, formulaire, case_fiscale, round(total, 2)))

    con.commit()
    con.close()

    return True

if __name__ == "__main__":
    print("VEILLE REGLEMENTAIRE")
    for r in verifier_et_telecharger():
        print(r)

    print("REMPLISSAGE LIASSE")
    remplir_liasse_depuis_comptabilite("2026", "RSI")
    print("OK")


