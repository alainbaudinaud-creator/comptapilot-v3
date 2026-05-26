
import sqlite3

from services.veille_reglementaire_service import (
    verifier_et_telecharger,
    remplir_liasse_depuis_comptabilite
)

def cloture_annuelle(db="db.sqlite", exercice="2026", exercice_suivant="2027", regime="RSI"):
    con = sqlite3.connect(db)
    cur = con.cursor()

    verifier_et_telecharger()

    remplir_liasse_depuis_comptabilite(exercice, regime)

    cur.execute("""
        UPDATE ecritures
        SET verrouillee=1,
            valide=1
        WHERE exercice=? OR exercice IS NULL
    """, (exercice,))

    cur.execute("""
        INSERT INTO ecritures (
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            journal,
            exercice,
            valide,
            dossier_id
        )
        SELECT
            ?,
            ?,
            ?,
            0,
            0,
            'AN',
            ?,
            1,
            1
        WHERE NOT EXISTS (
            SELECT 1 FROM ecritures WHERE piece=?
        )
    """, (
        exercice_suivant + "-01-01",
        "AN" + exercice_suivant,
        "À Nouveaux " + exercice_suivant,
        exercice_suivant,
        "AN" + exercice_suivant
    ))

    con.commit()
    con.close()

    return "Clôture terminée avec veille réglementaire et liasse pré-remplie"

