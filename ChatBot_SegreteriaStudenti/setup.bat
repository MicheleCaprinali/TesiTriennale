@echo off
title ChatBot UniBG - Setup Ambiente
echo.
echo ============================================
echo  ChatBot RAG - Setup Ambiente di Sviluppo
echo ============================================
echo.

echo 0- Controllo prerequisiti...
echo Verifica installazione Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo.
    echo Per installare Python:
    echo 1. Vai su https://www.python.org/downloads/
    echo 2. Scarica Python 3.8 o superiore
    echo 3. Durante l'installazione, seleziona "Add Python to PATH"
    echo 4. Riavvia il terminale e rilancia questo script
    echo.
    echo Premi un tasto per aprire la pagina di download...
    pause > nul
    start https://www.python.org/downloads/
    exit /b 1
)

python --version
echo [OK] Python installato

echo.
echo Verifica versione Python (richiesta 3.8+)...
python -c "import sys; assert sys.version_info >= (3, 8), 'Python 3.8+ richiesto'; print(f'[OK] Python {sys.version_info.major}.{sys.version_info.minor} compatibile')" 2>nul
if errorlevel 1 (
    echo [ERRORE] Versione Python non compatibile!
    echo E' richiesto Python 3.8 o superiore
    echo Aggiorna Python da: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 1- Controllo ambiente virtuale...
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Ambiente virtuale non trovato, creazione in corso...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRORE] Errore nella creazione dell'ambiente virtuale
        echo Possibili cause:
        echo - Permessi insufficienti
        echo - Spazio disco esaurito
        echo - Python non correttamente installato
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtuale creato
) else (
    echo [OK] Ambiente virtuale esistente trovato
)

echo.
echo 2- Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Errore nell'attivazione dell'ambiente virtuale
    pause
    exit /b 1
)
echo [OK] Ambiente virtuale attivato

echo.
echo 3- Aggiornamento pip...
venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARN] Errore nell'aggiornamento di pip, continuo...
)

echo.
echo 4- Controllo file requirements.txt...
if not exist "requirements.txt" (
    echo [ERRORE] File requirements.txt non trovato!
    echo Assicurati di essere nella directory corretta del progetto
    pause
    exit /b 1
)

echo [OK] File requirements.txt trovato
echo 5- Installazione dipendenze...
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRORE] Errore nell'installazione delle dipendenze
    echo Controlla la connessione internet e riprova
    pause
    exit /b 1
)

echo.
echo 6- Test configurazione...
venv\Scripts\python.exe -c "import torch, transformers, chromadb, streamlit; print('[OK] Tutte le dipendenze installate correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] Alcune dipendenze potrebbero non essere installate correttamente
    echo Verifica manualmente con: pip list
)

echo.
echo 7- Controllo Ollama...
ollama --version > nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama non trovato
    echo.
    echo Per installare Ollama:
    echo 1. Vai su https://ollama.ai
    echo 2. Scarica e installa Ollama per Windows
    echo 3. Riavvia il terminale
    echo 4. Installa il modello con: ollama pull mistral:7b
    echo.
) else (
    echo [OK] Ollama installato
    echo Verifica modello Mistral...
    ollama list | findstr mistral > nul 2>&1
    if errorlevel 1 (
        echo [WARN] Modello Mistral non trovato
        echo Installalo con: ollama pull mistral:7b
        echo.
        echo Vuoi installarlo ora? (y/n)
        set /p choice=
        if /i "%choice%"=="y" (
            echo Installazione modello Mistral in corso...
            ollama pull mistral:7b
            if errorlevel 1 (
                echo [WARN] Errore nell'installazione del modello
            ) else (
                echo [OK] Modello Mistral installato
            )
        )
    ) else (
        echo [OK] Modello Mistral disponibile
    )
)

echo.
echo ============================================
echo            SETUP COMPLETATO!
echo ============================================
echo.
echo Comandi disponibili:
echo  - start_chatbot.bat    : Avvia chatbot console
echo  - start_web.bat        : Avvia interfaccia web  
echo  - run_tests.bat        : Esegui tutti i test
echo  - update_database.bat  : Aggiorna database
echo.
echo Per problemi o supporto, consulta il README.md
echo.
echo Premi un tasto per chiudere...
pause > nul