from datetime import date
from decimal import Decimal

from app_refonte.models.entities import Cabinet, Societe, Ecriture, Immobilisation, Emprunt
from app_refonte.services.validation_service import valider_siret, valider_ecriture, controle_equilibre_piece


def run():
    cabinet = Cabinet(nom="IFG Solutions", siret="12345678901234")
    assert cabinet.nom == "IFG Solutions"
    assert valider_siret(cabinet.siret) is True

    societe = Societe(raison_sociale="Demo SAS", regime_tva="REEL_NORMAL")
    assert societe.raison_sociale == "Demo SAS"

    e = Ecriture(
        journal="AC",
        date_ecriture=date.today(),
        compte="606000",
        libelle="Achat fournitures",
        debit=Decimal("120.00"),
        credit=Decimal("0.00"),
    )
    assert e.est_equilibree_ligne() is True

    assert valider_ecriture(120, 0)["valide"] is True
    assert valider_ecriture(120, 50)["valide"] is False

    piece = controle_equilibre_piece([
        {"debit": 120, "credit": 0},
        {"debit": 0, "credit": 120},
    ])
    assert piece["equilibre"] is True

    immo = Immobilisation("Ordinateur", Decimal("1200.00"), 36)
    assert immo.duree_mois == 36

    emprunt = Emprunt("Banque Demo", "Pret equipement", Decimal("10000.00"), Decimal("3.5"), 60)
    assert emprunt.duree_mois == 60

    print("TESTS MODELES VALIDATION OK")


if __name__ == "__main__":
    run()
