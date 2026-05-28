from app_refonte.services.immobilisations_service import amortissement_lineaire
from app_refonte.services.emprunts_service import tableau_amortissement_emprunt
from app_refonte.services.tva_service import calcul_tva
from app_refonte.services.fec_service import controle_colonnes_fec, REQUIRED_FEC_COLUMNS

def test_immobilisation():
    lignes = amortissement_lineaire(1200, 12)
    assert len(lignes) == 12
    assert round(lignes[-1]["vnc"], 2) == 0

def test_emprunt():
    lignes = tableau_amortissement_emprunt(12000, 3, 12)
    assert len(lignes) == 12
    assert round(lignes[-1]["capital_restant"], 2) == 0

def test_tva():
    r = calcul_tva(1000, 300)
    assert r["tva_a_payer"] == 700
    assert r["statut"] == "A_PAYER"

def test_fec():
    r = controle_colonnes_fec(REQUIRED_FEC_COLUMNS)
    assert r["conforme"] is True

if __name__ == "__main__":
    test_immobilisation()
    test_emprunt()
    test_tva()
    test_fec()
    print("TESTS SERVICES METIER OK")
