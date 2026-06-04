def charger_ged_cabinet():
    kpis = {
        "documents": 184,
        "ocr": 151,
        "manquants": 7,
        "a_valider": 12,
        "score": 91,
    }

    dossiers = [
        {
            "nom": "Dossier permanent",
            "description": "Statuts, Kbis, mandats, contrats structurants, informations juridiques.",
            "documents": 34,
            "alertes": 1,
            "statut": "Structuré",
        },
        {
            "nom": "Cycle achats",
            "description": "Factures fournisseurs, justificatifs de charges, rapprochement pièces/écritures.",
            "documents": 52,
            "alertes": 2,
            "statut": "À contrôler",
        },
        {
            "nom": "Cycle ventes",
            "description": "Factures clients, avoirs, justificatifs de chiffre d'affaires.",
            "documents": 41,
            "alertes": 0,
            "statut": "OK",
        },
        {
            "nom": "Banque",
            "description": "Relevés, justificatifs bancaires, rapprochements et emprunts.",
            "documents": 28,
            "alertes": 3,
            "statut": "Incomplet",
        },
        {
            "nom": "Fiscal",
            "description": "TVA, IS, CVAE, liasse fiscale, accusés de réception.",
            "documents": 19,
            "alertes": 1,
            "statut": "À valider",
        },
        {
            "nom": "Social",
            "description": "Bulletins, DSN, charges sociales, contrats de travail.",
            "documents": 10,
            "alertes": 0,
            "statut": "OK",
        },
    ]

    pieces = [
        {
            "nom": "FACT_ORANGE_2025_11.pdf",
            "cycle": "Achats",
            "compte": "626100",
            "statut": "Indexée",
            "controle": "TVA cohérente",
        },
        {
            "nom": "RELEVE_BNP_DECEMBRE.pdf",
            "cycle": "Banque",
            "compte": "512000",
            "statut": "À rapprocher",
            "controle": "Écart détecté",
        },
        {
            "nom": "Kbis_2025.pdf",
            "cycle": "Permanent",
            "compte": "-",
            "statut": "Validé",
            "controle": "Document à jour",
        },
        {
            "nom": "DECLARATION_TVA_CA3.pdf",
            "cycle": "Fiscal",
            "compte": "445670",
            "statut": "Validée",
            "controle": "Accusé manquant",
        },
    ]

    return kpis, dossiers, pieces
