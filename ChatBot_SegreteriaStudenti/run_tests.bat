@echo off
title ChatBot UniBG - Test & Valutazione Completa
echo.
echo ============================================
echo  ChatBot RAG - Test e Valutazione Avanzata
echo ============================================
echo.
echo Verifica ambiente virtuale...
if not exist "venv\Scripts\python.exe" (
    echo [ERRORE] Ambiente virtuale non trovato!
    echo Esegui prima: setup_auto.bat
    pause
    exit /b 1
)

echo.
echo 1- Test sistema base...
venv\Scripts\python.exe main.py --check
if errorlevel 1 (
    echo [ERRORE] Sistema base non funzionante
    pause
    exit /b 1
)

echo.
echo 2- Test retrieval e ricerca...
venv\Scripts\python.exe tests\test_retrieval.py

echo.
echo 3- Validazione link e connettività...
venv\Scripts\python.exe tests\test_links.py

echo.
echo 4- Analisi metriche software...
venv\Scripts\python.exe evaluation\software_metrics.py

echo.
echo 5- *** EVALUATION RAG AVANZATA ***
echo Questo test richiede 5-10 minuti...
venv\Scripts\python.exe evaluation\rag_evaluation.py

echo.
echo 6- Evaluation tesi standard...
venv\Scripts\python.exe evaluation\thesis_evaluation.py

echo.
echo ============================================
echo  TEST COMPLETATI!
echo ============================================
echo.
echo REPORT GENERATI:
echo   - results/rag_evaluation_advanced.png
echo   - results/rag_evaluation_report.md  
echo   - results/software_metrics_analysis.png
echo   - results/thesis_performance_charts.png
echo.
echo Controlla la cartella results/ per tutti i report.
echo.
echo Premi un tasto per chiudere...
pause > nul

echo.
echo [OK] Tutti i test completati!
echo I risultati sono salvati nella cartella 'results\'
echo.
echo Premi un tasto per chiudere...
pause > nul
