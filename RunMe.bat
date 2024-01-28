@echo off
:menu
echo Menü:
echo 1. A* Algorithmus
echo 2. Dijkstra Algorithmus
echo 3. BFS Algorithmus
echo 4. Maze generation Algorithmus
echo 5. DFS Algorithmus
echo 6. Bidirectional search Algorithmus
echo 7. Bellman-Ford Algorithmus
echo 8. Floyd-Warshall Algorithmus
echo q. Beenden
echo.
set /p choice="Wähle eine Option: "

if "%choice%"=="q" goto end
if "%choice%"=="Q" goto end

if "%choice%" GEQ "1" if "%choice%" LEQ "8" (
    python path_finding.py %choice%
    goto menu
) else (
    echo Ungültige Auswahl. Bitte versuche es erneut.
    goto menu
)

:end
echo Das Programm wird beendet.

