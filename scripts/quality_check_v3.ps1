Write-Host "=== ComptaPilot V3 - Contrôle qualité global ==="

Write-Host ""
Write-Host "1. Test socle premium HTTP"

powershell -ExecutionPolicy Bypass -File "C:\Users\alain\comptapilot-v3\scripts\test_socle_premium.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR : test socle premium échoué"
    exit 1
}

Write-Host ""
Write-Host "2. Validation SQLAlchemy PDP V3"

docker compose exec comptapilot sh -c "cd /app && PYTHONPATH=/app python /app/scripts/validate_sqlalchemy_pdp_v3.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR : validation SQLAlchemy échouée"
    exit 1
}

Write-Host ""
Write-Host "3. Génération SQL SQLAlchemy PDP V3"

docker compose exec comptapilot sh -c "cd /app && PYTHONPATH=/app python /app/scripts/generate_sqlalchemy_sql_pdp_v3.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR : génération SQL SQLAlchemy échouée"
    exit 1
}

Write-Host ""
Write-Host "4. Validation facture métier PDP V3"

docker compose exec comptapilot sh -c "cd /app && PYTHONPATH=/app python /app/scripts/test_facture_metier_pdp_v3.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR : facture métier PDP V3 échouée"
    exit 1
}

Write-Host ""
Write-Host "5. Validation facture stockée PDP V3"

docker compose exec comptapilot sh -c "cd /app && PYTHONPATH=/app python /app/scripts/test_facture_base_pdp_v3.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR : facture stockée PDP V3 échouée"
    exit 1
}

Write-Host ""
Write-Host "6. Validation Alembic V3"

docker compose exec comptapilot sh -c "cd /app && PYTHONPATH=/app python /app/scripts/validate_alembic_v3.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR : validation Alembic échouée"
    exit 1
}

Write-Host ""
Write-Host "Contrôle qualité global OK"
