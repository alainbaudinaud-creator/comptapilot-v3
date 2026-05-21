try {
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/ecritures/relances-auto" -UseBasicParsing
}
catch {
    Write-Output "Erreur relance automatique : $_"
}