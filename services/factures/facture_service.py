def charger_facture_metier(facture_id: int):

    return {
        "id": facture_id,
        "numero": f"FAC-{facture_id}",
        "client": "CLIENT DEMO",
        "montant_ht": 1250.00,
        "tva": 250.00,
        "montant_ttc": 1500.00,
        "devise": "EUR",
        "statut": "VALIDE"
    }
