@echo off
title ChatBot UniBG - Setup Ambiente
echo.
echo ============================================
echo  ChatBot RAG - Setup Ambiente di Sviluppo
echo ============================================
echo.

echo 1- Controllo prerequisiti...
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
echo 2- Controllo ambiente virtuale...
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
echo 3- Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Errore nell'attivazione dell'ambiente virtuale
    pause
    exit /b 1
)
echo [OK] Ambiente virtuale attivato

echo.
echo 4- Aggiornamento pip...
venv\Scripts\python.exe -m pip install --upgrade pip wheel setuptools
if errorlevel 1 (
    echo [WARN] Errore nell'aggiornamento di pip, continuo...
)

echo.
echo 5- Installazione dipendenze...
echo [INFO] Installazione da requirements.txt...
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRORE] Errore nell'installazione delle dipendenze
    echo.
    echo SOLUZIONI POSSIBILI:
    echo 1. Verifica connessione internet
    echo 2. Prova con: pip install --upgrade pip
    echo 3. Installa manualmente: pip install torch sentence-transformers chromadb streamlit
    echo.
    pause
    exit /b 1
)

echo.
echo 6- Test configurazione...
echo [INFO] Verifica dipendenze principali...

venv\Scripts\python.exe -c "import torch; print('[OK] PyTorch importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] PyTorch: ERRORE
)

venv\Scripts\python.exe -c "import transformers; print('[OK] Transformers importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] Transformers: ERRORE
)

venv\Scripts\python.exe -c "import sentence_transformers; print('[OK] Sentence Transformers importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] Sentence Transformers: ERRORE
)

venv\Scripts\python.exe -c "import chromadb; print('[OK] ChromaDB importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] ChromaDB: ERRORE
)

venv\Scripts\python.exe -c "import streamlit; print('[OK] Streamlit importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] Streamlit: ERRORE
)

venv\Scripts\python.exe -c "import dotenv; print('[OK] Python-dotenv importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] Python-dotenv: ERRORE
)

echo.
echo 7- Controllo file di configurazione...
if not exist ".env" (
    echo [WARN] File .env mancante, copiando da .env.example...
    if exist ".env.example" (
        copy ".env.example" ".env" > nul
        echo [OK] File .env creato da template
    ) else (
        echo [WARN] Anche .env.example mancante - creazione file base...
        echo # Configurazione base ChatBot > .env
        echo EMBEDDING_MODEL=all-MiniLM-L6-v2 >> .env
        echo OLLAMA_BASE_URL=http://localhost:11434 >> .env
        echo OLLAMA_MODEL=mistral:7b >> .env
        echo TEMPERATURE=0.1 >> .env
        echo [OK] File .env base creato
    )
) else (
    echo [OK] File .env presente
)

echo.
echo 8- Controllo Ollama...
echo Verifica installazione Ollama...
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
    echo Vuoi aprire la pagina di download? (y/n)
    set /p ollama_choice=
    if /i "%ollama_choice%"=="y" (
        start https://ollama.ai
    )
) else (
    echo [OK] Ollama installato
    
    REM Verifica se Ollama è in esecuzione
    echo Verifica servizio Ollama...
    timeout /t 2 /nobreak >nul
    ollama list >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Ollama non in esecuzione
        echo Per avviare Ollama:
        echo 1. Cerca "Ollama" nel menu Start e aprilo
        echo 2. Oppure esegui: ollama serve
        echo 3. Poi rilancia questo script
        echo.
        echo Il setup continuerà, ma dovrai avviare Ollama manualmente
    ) else (
        echo [OK] Ollama in esecuzione
        echo Verifica modello Mistral...
        
        REM Controllo più robusto del modello Mistral
        ollama list 2>nul | findstr /i "mistral" >nul 2>&1
        if errorlevel 1 (
            echo [WARN] Modello Mistral non trovato
            echo Modelli disponibili:
            ollama list 2>nul || echo   Nessun modello installato
            echo.
            echo Installalo con: ollama pull mistral:7b
            echo.
            echo Vuoi installarlo ora? (y/n)
            set /p choice=
            if /i "%choice%"=="y" (
                echo Installazione modello Mistral in corso...
                ollama pull mistral:7b 2>nul
                if errorlevel 1 (
                    echo [WARN] Errore nell'installazione del modello
                    echo Prova manualmente: ollama pull mistral:7b
                ) else (
                    echo [OK] Modello Mistral installato
                )
            )
        ) else (
            echo [OK] Modello Mistral disponibile
        )
    )
)

echo.
echo 9- Verifica directory necessarie...
if not exist "data" (
    echo [WARN] Directory 'data' mancante
    mkdir data
    mkdir data\FAQ
    mkdir data\student_guide
    echo [INFO] Directory data create - aggiungi i tuoi documenti PDF
)

if not exist "extracted_text" (
    echo [INFO] Directory 'extracted_text' mancante - verra' creata al primo utilizzo
)

if not exist "vectordb" (
    echo [INFO] Directory 'vectordb' mancante - verra' creata al primo utilizzo
)

echo.
echo ============================================
echo            SETUP COMPLETATO!
echo ============================================
echo.
echo     Comandi disponibili:
echo    - start_chatbot.bat    : Avvia chatbot console
echo    - start_web.bat        : Avvia interfaccia web
echo    - run_tests.bat        : Esegui tutti i test
echo    - update_database.bat  : Aggiorna database
echo.
echo PROSSIMI PASSI:
echo 1. Aggiungi documenti PDF nella cartella 'data'
echo 2. Esegui 'update_database.bat' per processare i documenti
echo 3. Avvia il chatbot con 'start_chatbot.bat' o 'start_web.bat'
echo.
echo Per problemi o supporto, consulta il README.md
echo.
echo Premi un tasto per chiudere...
pause > nul