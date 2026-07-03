# Plan comptable français — ComptaPilot V3

La refonte contient un socle PCG français dans :

- `app_refonte/data/pcg_france.py`
- `app_refonte/services/pcg_service.py`

Fonctions :
- lister les comptes
- rechercher un compte
- regrouper par classe
- générer un SQL d’import par société

Ce socle préparera l’import automatique du plan comptable pour chaque société créée.
