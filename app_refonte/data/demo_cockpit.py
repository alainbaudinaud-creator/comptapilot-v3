DEMO_COCKPIT_DATA = {
    "societes": [
        {"raison_sociale": "Demo SAS"},
        {"raison_sociale": "Client Premium SARL"},
        {"raison_sociale": "Holding IFG"},
    ],
    "ecritures": [
        {"compte": "606000", "debit": 1200, "credit": 0},
        {"compte": "401000", "debit": 0, "credit": 1200},
        {"compte": "512000", "debit": 2500, "credit": 0},
        {"compte": "706000", "debit": 0, "credit": 2500},
    ],
    "documents": [
        {"fichier": "facture-orange.pdf", "statut": "A_ANALYSER", "montant_ttc": 240},
        {"fichier": "facture-materiel.pdf", "statut": "A_VALIDER", "montant_ttc": 1800},
        {"fichier": "releve-bancaire.pdf", "statut": "TERMINE", "montant_ttc": 0},
    ],
    "taches": [
        {"titre": "Contrôler TVA mai", "priorite": "HAUTE", "statut": "A_TRAITER"},
        {"titre": "Valider dossier Demo SAS", "priorite": "NORMALE", "statut": "EN_COURS"},
        {"titre": "Archivage FEC", "priorite": "INFO", "statut": "TERMINE"},
    ],
    "alertes": [
        {"niveau": "WARNING", "message": "Deux documents sont en attente de validation"},
        {"niveau": "INFO", "message": "Synchronisation bancaire opérationnelle"},
    ],
}
