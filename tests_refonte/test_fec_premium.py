from app_refonte.services.fec_premium_service import (
    FEC_COLUMNS,
    valider_structure_fec,
    controler_lignes_fec,
    exporter_fec_txt,
    generer_ligne_fec_demo,
)

structure = valider_structure_fec(FEC_COLUMNS)
assert structure["conforme"] is True

ligne = generer_ligne_fec_demo()

controle = controler_lignes_fec([ligne])
assert controle["conforme"] is True

bad = dict(ligne)
bad["Debit"] = "10"
bad["Credit"] = "5"

controle_bad = controler_lignes_fec([bad])
assert controle_bad["conforme"] is False

txt = exporter_fec_txt([ligne])
assert "JournalCode" in txt
assert "AC000001" in txt
assert txt.endswith("\n")

print("TESTS FEC PREMIUM OK")
