@echo off
title ChatBot UniBG - Setup Ambiente
echo.
echo ============================================
echo  ChatBot RAG - Setup Ambiente di Sviluppo
echo ============================================
echo.

echo 1- Controllo ambiente virtuale...
if not exist "venv\Scripts\activate.bat" (
    echo [ERRORE] Ambiente virtuale non trovato!
    echo Creazione nuovo ambiente virtuale...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRORE] Errore nella creazione dell'ambiente virtuale
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtuale creato
)

echo.
echo 2- Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo.
echo 3- Aggiornamento pip...
venv\Scripts\python.exe -m pip install --upgrade pip

echo.
echo 4- Installazione dipendenze...
venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo 5- Test configurazione...
venv\Scripts\python.exe -c "import torch, transformers, chromadb, streamlit; print('[OK] Tutte le dipendenze installate correttamente')"

echo.
echo 6- Controllo Ollama...
ollama --version > nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama non trovato. Installalo da: https://ollama.ai
) else (
    echo [OK] Ollama installato
    echo Verifica modello Mistral...
    ollama list | findstr mistral > nul
    if errorlevel 1 (
        echo [WARN] Modello Mistral non trovato. Installalo con: ollama pull mistral:7b
    ) else (
        echo [OK] Modello Mistral disponibile
    )
)

echo.
echo [OK] Setup completato!
echo.
echo     Comandi disponibili:
echo    - start_chatbot.bat    : Avvia chatbot console
echo    - start_web.bat        : Avvia interfaccia web
echo    - run_tests.bat        : Esegui tutti i test
echo    - update_database.bat  : Aggiorna database
echo.
echo Premi un tasto per chiudere...
pause > nul