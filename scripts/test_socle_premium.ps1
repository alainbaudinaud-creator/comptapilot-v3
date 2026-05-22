$routes = @(
"http://localhost:5001/",
"http://localhost:5001/ged",
"http://localhost:5001/ocr",
"http://localhost:5001/supervision",
"http://localhost:5001/production",
"http://localhost:5001/pdp-v3",
"http://localhost:5001/balance",
"http://localhost:5001/grand-livre",
"http://localhost:5001/bilan",
"http://localhost:5001/compte-resultat"
)

foreach ($route in $routes) {
    try {
        $r = Invoke-WebRequest $route -UseBasicParsing
        Write-Host "$route -> $($r.StatusCode)"
    }
    catch {
        Write-Host "$route -> ERREUR"
        exit 1
    }
}
