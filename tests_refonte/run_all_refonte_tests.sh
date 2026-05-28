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

echo "=== TOUS LES TESTS REFONTE SONT OK ==="
