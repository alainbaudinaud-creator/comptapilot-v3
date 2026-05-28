# Architecture cible ComptaPilot V3

## Principe
Séparer clairement :
- application Flask principale
- modules métier
- templates premium
- API
- base PostgreSQL
- tests
- documentation
- sauvegardes

## Structure cible
- app_refonte/
  - modules/
    - cockpit.py
    - cabinet.py
    - comptabilite.py
    - fiscal.py
    - immobilisations.py
    - emprunts.py
    - bancaire.py
    - pdp.py
    - ia_documentaire.py
    - portail_client.py
  - templates/
  - static/
- tests_refonte/
- docs/
- backups/

## Sécurité
- Authentification centralisée
- Sessions propres
- Routes publiques limitées
- Routes métier protégées
- Journal d’audit
- RGPD
- Sauvegardes régulières

## Conformité France
- PCG français
- TVA / CA3
- FEC DGFiP
- Archivage probatoire
- Facturation électronique
- PDP / e-reporting
- Traçabilité
