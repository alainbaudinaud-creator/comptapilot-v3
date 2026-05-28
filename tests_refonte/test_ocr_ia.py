from app_refonte.services.ocr_ia_service import (
    detecter_fournisseur,
    extraire_montants,
    analyser_facture,
    generer_ecriture_achat,
)

txt = """
FACTURE ORANGE
Montant HT 100,00
TVA 20,00
TOTAL TTC 120,00
"""

fournisseur = detecter_fournisseur(txt)
assert fournisseur == "orange"

montants = extraire_montants(txt)
assert montants["ttc"] == 120.0

analyse = analyser_facture(txt)

assert analyse["fournisseur"] == "orange"
assert analyse["score_ia"] >= 70
assert analyse["compte_charge"] == "626000"

ecriture = generer_ecriture_achat(analyse)

assert ecriture["journal"] == "AC"
assert len(ecriture["lignes"]) == 3

assert ecriture["lignes"][0]["debit"] == 100.0
assert ecriture["lignes"][1]["debit"] == 20.0
assert ecriture["lignes"][2]["credit"] == 120.0

print("TESTS OCR IA PREMIUM OK")
