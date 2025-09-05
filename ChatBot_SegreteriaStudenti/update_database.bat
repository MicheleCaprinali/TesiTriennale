@echo off
title ChatBot UniBG - Aggiornamento Database
echo.
echo ============================================
echo  ChatBot RAG - Aggiornamento VectorDB
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
echo [WARN] ATTENZIONE: Questo processo ricreare' completamente il database vettoriale
echo    Tutti i dati esistenti saranno sovrascritti.
echo.
set /p confirm="Vuoi continuare? (S/N): "
if /i "%confirm%" NEQ "S" (
    echo Operazione annullata.
    pause
    exit /b
)

echo.
echo 1- Ricostruzione completa database vettoriale...
echo    (include estrazione automatica da FAQ + PDF enhanced)
venv\Scripts\python.exe src\create_vectorstore.py

echo.
echo [OK] Database aggiornato con successo!
echo    - FAQ processate automaticamente
echo    - PDF enhanced processati automaticamente  
echo    - Database vettoriale ricreato completamente
echo.
echo Premi un tasto per chiudere...
pause > nul
