# Plan de migration du monolithe gestion_ecritures.py

## Diagnostic
Le fichier controllers/gestion_ecritures.py contient encore de nombreuses routes historiques regroupées sous /ecritures.

## Premiers blocs identifiés

### Comptabilité
- /
- /add
- /dashboard
- /dashboard/data
- /grand-livre-professionnel
- /dashboard-pro
- /tva-ca3-auto
- /bilan-automatique

### Fiscal
- /export/fec
- /liasse-fiscale
- /export-fec-dgfip

### OCR / Banque
- /ocr-facture-pdf
- /import-bancaire-intelligent

### Facturation électronique
- /nouvelle-facture-dematerialisee
- /transmettre-facture/<facture_id>
- /changer-statut-facture/<facture_id>/<statut>
- /factur-x
- /generer-pdf-facture/<facture_id>
- /generer-xml-facture/<facture_id>
- /controle-facture-electronique/<facture_id>
- /generer-vrai-factur-x/<facture_id>
- /controle-siret/<client_id>

### PDP
- /workflow-pdp
- /depot-pdp/<facture_id>
- /changer-statut-pdp/<workflow_id>/<statut>
- /reception-pdp-simulation
- /pdp-ready
- /annuaire-pdp
- /ajouter-client-pdp

### Archivage / conformité
- /archivage-probatoire
- /liste-archives-probatoires

### API e-invoicing
- /api/e-invoicing/factures
- /lignes-facture/<facture_id>

## Stratégie
Ne pas déplacer brutalement les routes.
Migrer par petits blocs :
1. créer un module métier cible,
2. recopier une route simple,
3. tester,
4. désactiver l'ancienne route seulement si absence de conflit,
5. committer.

## Priorité
Commencer par les routes non critiques et déjà doublonnées dans le nouveau socle.
