#!/usr/bin/env bash
set -e

export PYTHONPATH=.

echo "=== TEST 1 - STABILITE PRODUCTION ==="
bash tests_refonte/check_stability.sh

echo "=== TEST 2 - SERVICES METIER ==="
python3 tests_refonte/test_services_metier.py

echo "=== TEST 3 - FLASK DISPONIBLE DANS DOCKER ==="
docker compose exec -T comptapilot python - <<'PY'
from flask import Flask
print("FLASK DOCKER OK")
PY

echo "=== TEST 4 - MODELES ET VALIDATIONS ==="
python3 tests_refonte/test_models_validation.py

echo "=== TEST 5 - KPI COCKPIT ==="
python3 tests_refonte/test_kpi_cockpit.py

echo "=== TEST 6 - GENERATION COCKPIT DYNAMIQUE ==="
PYTHONPATH=. python3 app_refonte/renderers/render_cockpit_demo.py
test -f previews/refonte/cockpit_kpi_demo.html
grep -q "Cockpit piloté" previews/refonte/cockpit_kpi_demo.html
grep -q "Score production" previews/refonte/cockpit_kpi_demo.html

echo "=== TEST 7 - APP REFONTE ==="
echo "Mini-app Flask créée, test Flask complet différé à l’environnement Docker dédié."


echo "=== TEST 8 - PLAN COMPTABLE FRANCAIS ==="
PYTHONPATH=. python3 tests_refonte/test_pcg_service.py


echo "=== TEST 9 - IMMOBILISATIONS PREMIUM ==="
PYTHONPATH=. python3 tests_refonte/test_amortissement_ecritures.py


echo "=== TEST 10 - EMPRUNTS PREMIUM ==="
PYTHONPATH=. python3 tests_refonte/test_emprunts_premium.py


echo "=== TEST 11 - TVA PREMIUM ==="
PYTHONPATH=. python3 tests_refonte/test_tva_premium.py


echo "=== TEST 12 - FEC PREMIUM ==="
PYTHONPATH=. python3 tests_refonte/test_fec_premium.py


echo "=== TEST 13 - OCR IA PREMIUM ==="
PYTHONPATH=. python3 tests_refonte/test_ocr_ia.py


echo "=== TEST 14 - RAPPROCHEMENT BANCAIRE PREMIUM ==="
PYTHONPATH=. python3 tests_refonte/test_rapprochement_bancaire.py

echo "=== TOUS LES TESTS REFONTE SONT OK ==="
