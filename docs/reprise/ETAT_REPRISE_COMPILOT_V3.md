# État de reprise — ComptaPilot V3

## État stable actuel
- VPS OVH opérationnel
- Docker opérationnel
- PostgreSQL opérationnel
- Nginx HTTPS opérationnel
- GitHub synchronisé
- `/login` répond 200 OK
- `/` est protégé et redirige vers `/login`
- Plus de 502 au moment de la reprise

## Décision de méthode
Ne plus modifier directement la production.
Toutes les évolutions doivent passer par :
1. branche Git dédiée
2. backup avant modification
3. test import Python
4. test Docker
5. test HTTP local
6. commit seulement si tout est OK
7. push GitHub seulement après validation

## Travail déjà réalisé à conserver
- Cockpit premium SaaS
- Tables PostgreSQL métier :
  - cabinet_collaborateurs
  - cabinet_permissions
  - cabinet_workflow_taches
  - ecritures_premium
  - immobilisations
  - notifications_workflow
  - rapprochements_bancaires
  - societes_clientes_premium
- Socle workflow cabinet
- Socle permissions
- Socle immobilisations
- Socle rapprochement bancaire
- Socle centre fiscal
- Templates premium existants
- Nginx HTTPS sécurisé
- Sauvegardes locales dans backups/

## Objectif produit
Construire une application SaaS cabinet :
- ultra professionnelle
- ultra moderne
- ultra rapide
- simple d’utilisation
- design premium/futuriste
- conforme à la réglementation française
- orientée cabinet comptable, dirigeant, fiscalité, PDP, FEC, TVA, OCR IA, portail client

## Commandes de reprise
```bash
cd ~/apps/comptapilot-v3
docker compose up -d
git status
docker compose ps
curl -k -I https://127.0.0.1/login
D
