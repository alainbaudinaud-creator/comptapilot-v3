# Roadmap officielle ComptaPilot V3

## Phase 1 - Stabilisation du socle
Statut : en cours / très avancé

Objectifs :
- Nettoyer les anciennes versions
- Archiver les prototypes
- Conserver un seul noyau actif
- Valider Docker + Gunicorn + PostgreSQL
- Documenter l’architecture officielle

## Phase 2 - Audit fonctionnel
Objectifs :
- Tester les routes principales
- Identifier les modules actifs
- Identifier les modules dormants
- Corriger les routes cassées
- Vérifier les templates réellement utilisés

## Phase 3 - Sécurisation
Objectifs :
- Finaliser authentification
- Vérifier rôles et permissions
- Réactiver rate limiting si pertinent
- Durcir les cookies en production
- Vérifier variables sensibles

## Phase 4 - Industrialisation
Objectifs :
- Sauvegardes PostgreSQL propres
- Tests automatisés
- CI/CD
- Déploiement VPS
- HTTPS / Nginx
- Monitoring

## Phase 5 - Produit
Objectifs :
- Import FEC robuste
- Balance / Grand livre / Bilan fiables
- GED documentaire
- OCR comptable
- IA d’aide à la révision
- Exports PDF et fiscalité
- Parcours utilisateur clair

## Règle prioritaire
Avant toute nouvelle fonctionnalité, vérifier si elle existe déjà dans controllers, services ou templates.
