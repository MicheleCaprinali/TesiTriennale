@echo off
title ChatBot UniBG - Console
echo.
echo ============================================
echo  ChatBot RAG - Segreteria Studenti UniBG
echo ============================================
echo.
echo Attivazione ambiente virtuale...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Ambiente virtuale attivato
) else (
    echo [ERRORE] Ambiente virtuale non trovato!
    echo Esegui prima: setup.bat
    pause
    exit /b 1
)

echo.
echo Controllo dipendenze...
venv\Scripts\python.exe -c "import sys; print('Python:', sys.executable)"
venv\Scripts\python.exe -c "import sentence_transformers" >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] SentenceTransformers mancante - esegui: pip install -r requirements.txt
    pause
    exit /b 1
) else (
    echo [OK] SentenceTransformers trovato
)

echo.
echo Avvio ChatBot in modalita console...
echo.
echo     Comandi disponibili:
echo    - Scrivi la tua domanda e premi INVIO
echo    - Scrivi 'exit' per uscire
echo.

venv\Scripts\python.exe main.py

echo.
echo ChatBot terminato. Premi un tasto per chiudere...
pause > nul
