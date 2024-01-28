while ($true) {
    Write-Host "Menü:"
    Write-Host "1. A* Algorithmus"
    Write-Host "2. Dijkstra Algorithmus"
    Write-Host "3. BFS Algorithmus"
    Write-Host "4. Maze generation Algorithmus"
    Write-Host "5. DFS Algorithmus"
    Write-Host "6. Bidirectional search Algorithmus"
    Write-Host "7. Bellman-Ford Algorithmus"
    Write-Host "8. Floyd-Warshall Algorithmus"
    Write-Host "q. Beenden"

    $choice = Read-Host "Wähle eine Option"

    if ($choice -eq "q" -or $choice -eq "Q") {
        Write-Host "Das Programm wird beendet."
        break
    }

    if ($choice -match "^[1-8]$") {
        python path_finding.py $choice
    } else {
        Write-Host "Ungültige Auswahl. Bitte versuche es erneut."
    }
}