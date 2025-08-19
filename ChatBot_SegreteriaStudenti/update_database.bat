@echo off
title ChatBot UniBG - Aggiornamento Database
echo.
echo ============================================
echo  ChatBot RAG - Aggiornamento VectorDB
echo ============================================
echo.
echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo.
echo ⚠️  ATTENZIONE: Questo processo ricreerà completamente il database vettoriale
echo    Tutti i dati esistenti saranno sovrascritti.
echo.
set /p confirm="Vuoi continuare? (S/N): "
if /i "%confirm%" NEQ "S" (
    echo Operazione annullata.
    pause
    exit /b
)

echo.
echo 1- Estrazione testo da documenti...
python src\extract_and_save.py

echo.
echo 2- Creazione nuovo database vettoriale...
python src\create_vectorstore.py

echo.
echo ✅ Database aggiornato con successo!
echo.
echo Premi un tasto per chiudere...
pause > nul
