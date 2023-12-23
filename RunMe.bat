@echo off

:menu
cls
echo Menü:
echo 1. Option 1
echo 2. Option 2
echo 3. Option 3
rem Füge hier weitere Optionen hinzu
echo 10. Option 10
echo Q. Beenden

set /p choice=Wähle eine Option:

if "%choice%"=="1" (
    echo Du hast Option 1 ausgewählt.
    python path_finding.py "1"
) else if "%choice%"=="2" (
    echo Du hast Option 2 ausgewählt.
    python path_finding.py "2"
) else if "%choice%"=="3" (
    echo Du hast Option 3 ausgewählt.
    python path_finding.py "3"
) else if "%choice%"=="10" (
    echo Du hast Option 10 ausgewählt.
    python path_finding.py "10"
) else if /i "%choice%"=="Q" (
    echo Das Programm wird beendet.
    exit /b 0
) else (
    echo Ungültige Auswahl. Bitte versuche es erneut.
    pause
    goto menu
)
