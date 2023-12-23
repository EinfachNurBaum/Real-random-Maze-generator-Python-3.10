#!/bin/bash

# Funktion zum Ausführen des ausgewählten Befehls
run_command() {
    case $1 in
        1)
            echo "Du hast Option 1 ausgewählt."
            python path_finding.py "1"
            ;;
        2)
            echo "Du hast Option 2 ausgewählt."
            python path_finding.py "2"
            ;;
        3)
            echo "Du hast Option 3 ausgewählt."
            python path_finding.py "3"
            ;;
        # Füge hier weitere Optionen hinzu
        10)
            echo "Du hast Option 10 ausgewählt."
            python path_finding.py "10"
            ;;
        q|Q)
            echo "Das Programm wird beendet."
            exit 0
            ;;
        *)
            echo "Ungültige Auswahl. Bitte versuche es erneut."
            ;;
    esac
}

# Hauptprogramm
while true; do
    # Menü anzeigen
    echo "Menü:"
    echo "1. Option 1"
    echo "2. Option 2"
    echo "3. Option 3"
    # Füge hier weitere Optionen hinzu
    echo "10. Option 10"
    echo "q. Beenden"

    # Benutzereingabe lesen
    read -p "Wähle eine Option: " choice

    # Ausgewählten Befehl ausführen
    run_command "$choice"
done
