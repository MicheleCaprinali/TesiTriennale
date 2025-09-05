@echo off
title ChatBot UniBG - Setup Ambiente
echo.
echo ============================================
echo  ChatBot RAG - Setup Ambiente di Sviluppo
echo ============================================
echo.

echo CONTROLLO PREREQUISITI...
echo.

echo 1- Verifica Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo INSTALLARE PYTHON 3.9+ da: https://www.python.org/downloads/
    echo IMPORTANTE: Selezionare "Add Python to PATH" durante installazione
    pause
    exit /b 1
) else (
    echo [OK] Python trovato
    python --version
)

echo.
echo 2- Controllo ambiente virtuale...
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Ambiente virtuale non trovato - creazione in corso...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRORE] Errore nella creazione dell'ambiente virtuale
        echo Verificare che Python sia installato correttamente
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtuale creato
) else (
    echo [OK] Ambiente virtuale esistente
)

echo.
echo 3- Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Impossibile attivare ambiente virtuale
    pause
    exit /b 1
)

echo.
echo 4- Aggiornamento pip...
venv\Scripts\python.exe -m pip install --upgrade pip

echo.
echo 5- Installazione dipendenze...
echo Questo potrebbe richiedere diversi minuti...
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRORE] Errore nell'installazione delle dipendenze
    echo Verificare connessione internet e riprovare
    pause
    exit /b 1
)

echo.
echo 6- Test configurazione...
venv\Scripts\python.exe -c "import sentence_transformers, chromadb, streamlit; print('[OK] Dipendenze core installate correttamente')"
if errorlevel 1 (
    echo [WARN] Alcune dipendenze potrebbero non essere installate correttamente
)

echo.
echo 7- Controllo Ollama...
ollama --version > nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama non trovato!
    echo.
    echo INSTALLAZIONE OLLAMA RICHIESTA:
    echo 1. Vai su: https://ollama.ai
    echo 2. Scarica Ollama per Windows
    echo 3. Installa e riavvia il terminale
    echo 4. Esegui: ollama pull mistral:7b
    echo.
    echo Premi un tasto per continuare senza Ollama...
    pause
) else (
    echo [OK] Ollama installato
    echo Verifica modello Mistral...
    ollama list | findstr mistral > nul
    if errorlevel 1 (
        echo [WARN] Modello Mistral non trovato!
        echo Installazione automatica del modello...
        ollama pull mistral:7b
        if errorlevel 1 (
            echo [WARN] Installazione fallita - installa manualmente: ollama pull mistral:7b
        ) else (
            echo [OK] Modello Mistral installato
        )
    ) else (
        echo [OK] Modello Mistral disponibile
    )
)

echo.
echo 8- Verifica dati...
if not exist "data\FAQ" (
    echo [WARN] Cartella dati FAQ non trovata
) else (
    echo [OK] Dati FAQ presenti
)

if not exist "vectordb" (
    echo [INFO] Database vettoriale non trovato - creazione automatica...
    venv\Scripts\python.exe src\create_vectorstore.py
    if errorlevel 1 (
        echo [WARN] Creazione database fallita - esegui: python src/create_vectorstore.py
    ) else (
        echo [OK] Database vettoriale creato
    )
) else (
    echo [OK] Database vettoriale esistente
)

echo.
echo [SUCCESS] Setup completato!
echo.
echo     COMANDI DISPONIBILI:
echo    - start_chatbot.bat    : Avvia chatbot console
echo    - start_web.bat        : Avvia interfaccia web
echo    - run_tests.bat        : Esegui tutti i test
echo    - update_database.bat  : Aggiorna database
echo.
echo     NOTE:
echo    - Se Ollama non è installato, installalo da https://ollama.ai
echo    - Dopo aver installato Ollama: ollama pull mistral:7b
echo.
echo Premi un tasto per chiudere...
pause > nul
