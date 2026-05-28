from app_refonte.services.pcg_service import (
    lister_pcg_base,
    rechercher_compte,
    comptes_par_classe,
    generer_sql_insert_pcg,
)

pcg = lister_pcg_base()
assert len(pcg) >= 40
assert any(c["numero"] == "512000" for c in pcg)
assert any("TVA collectée" in c["libelle"] for c in pcg)

banques = rechercher_compte("banque")
assert any(c["numero"] == "512000" for c in banques)

classes = comptes_par_classe()
assert "1" in classes
assert "4" in classes
assert "6" in classes
assert "7" in classes

sql = generer_sql_insert_pcg()
assert "INSERT INTO ref_plan_comptable" in sql
assert "ON CONFLICT" in sql
assert "512000" in sql

print("TESTS PCG SERVICE OK")
