param(
    [string]$Python = "C:\Python314\pythonw.exe",
    [string]$Script = "C:\Users\alain\comptapilot-v3_clean\auto_backup_comptapilot.py",
    [string]$RunKeyName = "ComptaPilotAutoBackup"
)

$action = "`"$Python`" `"$Script`""

$runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
New-Item -Path $runKey -Force | Out-Null
Set-ItemProperty -Path $runKey -Name $RunKeyName -Value $action

Write-Host "Demarrage automatique configure : $RunKeyName"
Write-Host "Commande : $action"
