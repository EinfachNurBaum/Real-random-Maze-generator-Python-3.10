# Funktion zum Ausführen des ausgewählten Befehls
function Run-Command {
    param (
        [string]$choice
    )

    switch ($choice) {
        "1" {
            Write-Host "Du hast Option 1 ausgewählt."
            python path_finding.py "1"
        }
        "2" {
            Write-Host "Du hast Option 2 ausgewählt."
            python path_finding.py "2"
        }
        "3" {
            Write-Host "Du hast Option 3 ausgewählt."
            python path_finding.py "3"
        }
        # Füge hier weitere Optionen hinzu
        "10" {
            Write-Host "Du hast Option 10 ausgewählt."
            python path_finding.py "10"
        }
        "q" {
            Write-Host "Das Programm wird beendet."
            exit 0
        }
        default {
            Write-Host "Ungültige Auswahl. Bitte versuche es erneut."
        }
    }
}

# Hauptprogramm
while ($true) {
    # Menü anzeigen
    Write-Host "Menü:"
    Write-Host "1. Option 1"
    Write-Host "2. Option 2"
    Write-Host "3. Option 3"
    # Füge hier weitere Optionen hinzu
    Write-Host "10. Option 10"
    Write-Host "q. Beenden"

    # Benutzereingabe lesen
    $choice = Read-Host "Wähle eine Option"

    # Ausgewählten Befehl ausführen
    Run-Command -choice $choice
}
