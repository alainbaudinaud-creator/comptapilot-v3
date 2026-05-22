$routes = @(
"http://localhost:5001/",
"http://localhost:5001/ged",
"http://localhost:5001/ocr",
"http://localhost:5001/supervision",
"http://localhost:5001/production",
"http://localhost:5001/pdp-v3",
"http://localhost:5001/pdp-v3/workflow",
"http://localhost:5001/pdp-v3/supervision",
"http://localhost:5001/api/pdp-v3/workflows",
"http://localhost:5001/balance",
"http://localhost:5001/grand-livre",
"http://localhost:5001/bilan",
"http://localhost:5001/compte-resultat"
)

$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$rapport = @()
$rapport += "# Rapport test socle premium V3"
$rapport += ""
$rapport += "Date : $date"
$rapport += ""
$rapport += "## Routes testées"
$rapport += ""

foreach ($route in $routes) {
    try {
        $r = Invoke-WebRequest $route -UseBasicParsing
        $line = "- $route -> $($r.StatusCode)"
        Write-Host $line
        $rapport += $line
    }
    catch {
        $line = "- $route -> ERREUR"
        Write-Host $line
        $rapport += $line
        $rapport | Set-Content -Encoding UTF8 "C:\Users\alain\comptapilot-v3\docs\RAPPORT_TEST_SOCLE_PREMIUM_V3.md"
        exit 1
    }
}

$rapport += ""
$rapport += "## Résultat"
$rapport += "Socle premium V3 opérationnel."

$rapport | Set-Content -Encoding UTF8 "C:\Users\alain\comptapilot-v3\docs\RAPPORT_TEST_SOCLE_PREMIUM_V3.md"
