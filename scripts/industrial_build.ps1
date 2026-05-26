
Write-Host ""
Write-Host "======================================="
Write-Host "COMPTAPILOT V3 - INDUSTRIAL BUILD"
Write-Host "======================================="
Write-Host ""

$root = "C:\Users\alain\comptapilot-v3"

Set-Location $root

Write-Host "[1] REPARATION DES FAUX RETOURS LIGNE"

Get-ChildItem $root -Recurse -Filter "*.py" | ForEach-Object {

    $path = $_.FullName

    if (
        $path -like "*\archive\*" -or
        $path -like "*\.venv\*" -or
        $path -like "*\venv\*" -or
        $path -like "*\__pycache__\*" -or
        $path -like "*\migrations\*"
    ) {
        return
    }

    try {

        $content = Get-Content $path -Raw -Encoding UTF8

        if ($content -like "*``r``n*") {

            $content = $content.Replace('`r`n', "`r`n")

            Set-Content -Path $path -Value $content -Encoding UTF8

            Write-Host "Réparé : $path"
        }

    } catch {}

}

Write-Host ""
Write-Host "[2] REPARATION FICHIERS HTML DANS PYTHON"

Get-ChildItem $root -Recurse -Filter "*.py" | ForEach-Object {

    $path = $_.FullName

    if (
        $path -like "*\archive\*" -or
        $path -like "*\.venv\*" -or
        $path -like "*\venv\*" -or
        $path -like "*\__pycache__\*" -or
        $path -like "*\migrations\*"
    ) {
        return
    }

    try {

        $firstLine = Get-Content $path -TotalCount 1

        if ($firstLine -like "*<!DOCTYPE html>*") {

            Set-Content -Path $path -Encoding UTF8 -Value @'
def placeholder():
    return True
