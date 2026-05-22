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
Write-Host "Contrôle qualité global OK"
