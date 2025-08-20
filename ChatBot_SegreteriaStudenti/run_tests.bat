@echo off
title ChatBot UniBG - Test & Valutazione
echo.
echo ============================================
echo  ChatBot RAG - Test e Valutazione
echo ============================================
echo.
echo Attivazione ambiente virtuale...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERRORE] Ambiente virtuale non trovato!
    echo Esegui prima: setup.bat
    pause
    exit /b 1
)

echo.
echo 1- Esecuzione test di retrieval...
python tests\test_retrieval.py

echo.
echo 2- Test validazione link...
python tests\test_links.py

echo.
echo 3- Generazione metriche software...
python evaluation\software_metrics.py

echo.
echo 4- Valutazione performance tesi...
python evaluation\thesis_evaluation.py

echo.
echo [OK] Tutti i test completati!
echo I risultati sono salvati nella cartella 'results\'
echo.
echo Premi un tasto per chiudere...
pause > nul
