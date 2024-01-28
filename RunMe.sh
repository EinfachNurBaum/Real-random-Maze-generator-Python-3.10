#!/bin/bash

# Hauptprogramm
while true; do
    # Menü anzeigen
    echo "Menü:"
    echo "1. A* Algorithmus"
    echo "2. Dijkstra Algorithmus"
    echo "3. BFS Algorithmus"
    echo "4. Maze generation Algorithmus"
    echo "5. DFS Algorithmus"
    echo "6. Bidirectional search Algorithmus"
    echo "7. Bellman-Ford Algorithmus"
    echo "8. Floyd-Warshall Algorithmus"
    echo "q. Beenden"

    # Benutzereingabe lesen
    read -p "Wähle eine Option: " choice

    # Check für Beenden
    if [[ "$choice" == "q" || "$choice" == "Q" ]]; then
        echo "Das Programm wird beendet."
        exit 0
    fi

    # Ausgewählten Befehl ausführen
    if [[ "$choice" =~ ^[1-8]$ ]]; then
        python path_finding.py "$choice"
    else
        echo "Ungültige Auswahl. Bitte versuche es erneut."
    fi
done
