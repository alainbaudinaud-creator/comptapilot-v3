from decimal import Decimal

from repositories.ecritures.ecriture_repository import (
    get_precompta_for_ecriture,
    create_ecriture_lines
)

from services_v3.history.history_service import (
    log_action
)


def convert_precompta_to_ecriture(precompta_id):

    precompta = get_precompta_for_ecriture(precompta_id)

    if not precompta:

        log_action(
            module="ecritures",
            action="conversion_precompta_ecriture",
            statut="erreur",
            reference_type="precompta",
            reference_id=precompta_id,
            message="Précompta introuvable"
        )

        return {
            "success": False,
            "message": "Précompta introuvable"
        }

    if precompta.get("statut_validation") not in [
        "validee",
        "transformee_ecriture"
    ]:

        log_action(
            module="ecritures",
            action="conversion_precompta_ecriture",
            statut="erreur",
            societe_id=precompta.get("societe_id"),
            reference_type="precompta",
            reference_id=precompta_id,
            message="Précompta non validée"
        )

        return {
            "success": False,
            "message": "Précompta non validée"
        }

    if precompta.get("statut_validation") == "transformee_ecriture":

        log_action(
            module="ecritures",
            action="conversion_precompta_ecriture",
            statut="erreur",
            societe_id=precompta.get("societe_id"),
            reference_type="precompta",
            reference_id=precompta_id,
            message="Précompta déjà transformée en écriture"
        )

        return {
            "success": False,
            "message": "Précompta déjà transformée en écriture"
        }

    lines = build_purchase_ecriture_lines(precompta)

    create_ecriture_lines(
        precompta,
        lines
    )

    log_action(
        module="ecritures",
        action="conversion_precompta_ecriture",
        statut="ok",
        societe_id=precompta.get("societe_id"),
        reference_type="precompta",
        reference_id=precompta_id,
        message="Écriture comptable générée depuis précompta",
        metadata={
            "lines_count": len(lines),
            "document_id": precompta.get("document_id"),
            "montant_ttc": str(precompta.get("montant_ttc"))
        }
    )

    return {
        "success": True,
        "precompta_id": precompta_id,
        "lines_count": len(lines),
        "lines": lines,
        "message": "Écriture comptable générée"
    }


def build_purchase_ecriture_lines(precompta):

    fournisseur = precompta.get("fournisseur") or "Fournisseur"
    libelle = f"Facture {fournisseur}"

    montant_ht = to_decimal(precompta.get("montant_ht"))
    montant_tva = to_decimal(precompta.get("montant_tva"))
    montant_ttc = to_decimal(precompta.get("montant_ttc"))

    if montant_ttc == 0 and montant_ht > 0 and montant_tva > 0:
        montant_ttc = montant_ht + montant_tva

    return [
        {
            "compte": precompta.get("compte_charge") or "607000",
            "libelle": libelle,
            "debit": float(montant_ht),
            "credit": 0
        },
        {
            "compte": precompta.get("compte_tva") or "445660",
            "libelle": libelle,
            "debit": float(montant_tva),
            "credit": 0
        },
        {
            "compte": precompta.get("compte_fournisseur") or "401000",
            "libelle": libelle,
            "debit": 0,
            "credit": float(montant_ttc)
        }
    ]


def to_decimal(value):

    if value is None:
        return Decimal("0.00")

    return Decimal(str(value)).quantize(
        Decimal("0.01")
    )

