# Session de reprise ComptaPilot V3

Date : Fri May 29 2026

## Serveur actif
IP : 57.130.60.80
URL refonte : http://57.130.60.80/refonte/

## Infrastructure validée
- Nginx OK
- Docker OK
- PostgreSQL OK
- Gunicorn refonte OK sur 5099
- /refonte/ OK
- /refonte-static/ OK

## Socle comptable validé
- Plan comptable PostgreSQL : plan_comptable
- Écritures : ecritures_v3
- Lignes : lignes_ecritures_v3
- Pièces : pieces_v3

## Modules opérationnels
- Cockpit réel
- Plan comptable
- Immobilisations + amortissements + écritures OD
- Emprunts + échéanciers + écritures BQ
- OCR texte → écriture comptable
- OCR PDF → extraction texte
- Validation OCR humaine
- Journal général
- Grand livre
- Balance générale
- Compte de résultat
- Bilan
- Export FEC

## URLs validées
- /refonte/
- /refonte/pcg
- /refonte/immobilisations
- /refonte/emprunts
- /refonte/tva
- /refonte/fec
- /refonte/balance
- /refonte/grand-livre
- /refonte/journal
- /refonte/compte-resultat
- /refonte/bilan
- /refonte/fec-export
- /refonte/ocr
- /refonte/ocr-pdf
- /refonte/validation-ocr

## Workflow OCR validé
PDF facture
→ upload
→ extraction texte PDFPlumber / PyMuPDF / Tesseract
→ analyse IA
→ proposition d’écriture
→ statut A_VALIDER
→ validation humaine
→ comptabilisation PostgreSQL
→ journal / grand livre / balance / FEC

## Fichiers principaux modifiés
- app_refonte/app_refonte.py
- app_refonte/routes/api_metier_demo.py
- app_refonte/services/cockpit_reel_service.py
- app_refonte/services/comptabilisation_ocr_service.py
- app_refonte/services/ocr_pdf_service.py
- app_refonte/templates/*.html

## Attention
Les fichiers app_refonte sont copiés manuellement dans le conteneur avec :
docker cp app_refonte/. comptapilot-v3-comptapilot:/app/app_refonte/

Si le conteneur est reconstruit, vérifier que app_refonte est bien inclus dans l’image.

## Prochaine étape recommandée
1. Sauvegarde Git complète
2. Commit clair
3. Push GitHub
4. Puis seulement : industrialiser Dockerfile pour inclure app_refonte proprement

## Règle de travail
Ne plus modifier docker-compose.yml, app.py, Dockerfile ou Nginx sans sauvegarde et test de retour arrière.
