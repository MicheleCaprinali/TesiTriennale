@echo off
title ChatBot UniBG - Setup Automatico
color 0A

REM Inizializzazione variabili
set OLLAMA_MISSING=0

echo.
echo ================================================================
echo  CHATBOT SEGRETERIA STUDENTI - UNIVERSITA' DI BERGAMO
echo  Setup Automatico Sistema RAG
echo ================================================================
echo.
echo [DEBUG] Script avviato correttamente
echo [DEBUG] Variabili inizializzate

echo FASE 1: CONTROLLO PREREQUISITI
echo ================================================================
echo [DEBUG] Inizio Fase 1

echo 1.1- Verifica Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo.
    echo AZIONE RICHIESTA:
    echo 1. Installa Python 3.9+ da python.org
    echo 2. Aggiungi Python al PATH
    echo 3. Riavvia CMD e riesegui setup.bat
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION%
echo [DEBUG] Python versione catturata

echo.
echo 1.2- Verifica versione...
python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python 3.9+ richiesto!
    pause
    exit /b 1
)
echo [OK] Versione compatibile
echo [DEBUG] Fase 1 completata

echo.
echo FASE 2: AMBIENTE VIRTUALE
echo ================================================================
echo [DEBUG] Inizio Fase 2

echo 2.1- Setup ambiente virtuale...
if not exist "chatbot_env\Scripts\python.exe" (
    echo [INFO] Creazione ambiente virtuale...
    python -m venv chatbot_env
    if errorlevel 1 (
        echo [ERRORE] Creazione fallita
        pause
        exit /b 1
    )
    echo [OK] Ambiente creato
) else (
    echo [OK] Ambiente esistente
)

echo.
echo 2.2- Attivazione ambiente...
call chatbot_env\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Attivazione fallita
    pause
    exit /b 1
)
echo [OK] Ambiente attivo
echo [DEBUG] Fase 2 completata

echo.
echo FASE 3: INSTALLAZIONE DIPENDENZE
echo ================================================================
echo [DEBUG] Inizio Fase 3

echo 3.1- Aggiornamento pip...
chatbot_env\Scripts\python.exe -m pip install --upgrade pip --quiet --no-warn-script-location
if errorlevel 1 (
    echo [WARN] Aggiornamento pip fallito
) else (
    echo [OK] pip aggiornato
)

echo.
echo 3.2- Verifica requirements.txt...
if not exist "requirements.txt" (
    echo [ERRORE] File requirements.txt non trovato!
    pause
    exit /b 1
)
echo [OK] requirements.txt trovato

echo.
echo 3.3- Installazione pacchetti (può richiedere alcuni minuti)...
chatbot_env\Scripts\python.exe -m pip install -r requirements.txt --quiet --no-warn-script-location
if errorlevel 1 (
    echo [ERRORE] Installazione fallita
    echo Verifica connessione internet e riprova
    pause
    exit /b 1
)
echo [OK] Dipendenze installate

echo.
echo 3.4- Test moduli essenziali...
echo [INFO] Test SentenceTransformers...
chatbot_env\Scripts\python.exe -c "import sentence_transformers; print('SentenceTransformers OK')"
if errorlevel 1 (
    echo [WARN] SentenceTransformers non disponibile
) else (
    echo [OK] SentenceTransformers verificato
)

echo [INFO] Test ChromaDB...
chatbot_env\Scripts\python.exe -c "import chromadb; print('ChromaDB OK')"
if errorlevel 1 (
    echo [WARN] ChromaDB non disponibile
) else (
    echo [OK] ChromaDB verificato
)
echo [DEBUG] Fase 3 completata

echo.
echo FASE 4: CONFIGURAZIONE OLLAMA
echo ================================================================
echo [DEBUG] Inizio Fase 4

echo 4.1- Verifica Ollama...
echo [DEBUG] Test comando where ollama...
where ollama >nul 2>&1
set OLLAMA_WHERE_RESULT=%errorlevel%
echo [DEBUG] Where ollama result: %OLLAMA_WHERE_RESULT%

if %OLLAMA_WHERE_RESULT% neq 0 (
    echo [WARN] Ollama non installato
    echo.
    echo INSTALLAZIONE MANUALE RICHIESTA:
    echo 1. Vai su https://ollama.ai/download
    echo 2. Scarica e installa Ollama per Windows
    echo 3. Riavvia CMD e riesegui questo script
    echo.
    set OLLAMA_MISSING=1
    echo [DEBUG] Saltando a skip_ollama
    goto skip_ollama
)

echo [DEBUG] Ollama trovato, test version...
ollama --version >nul 2>&1
set OLLAMA_VERSION_RESULT=%errorlevel%
echo [DEBUG] Ollama version result: %OLLAMA_VERSION_RESULT%

if %OLLAMA_VERSION_RESULT% neq 0 (
    echo [WARN] Ollama installato ma non funzionante
    set OLLAMA_MISSING=1
    echo [DEBUG] Saltando a skip_ollama per version error
    goto skip_ollama
)

echo [OK] Ollama installato
echo [DEBUG] Ollama version OK

echo.
echo 4.2- Verifica servizio Ollama...
echo [DEBUG] Test ollama list...
ollama list >nul 2>&1
set OLLAMA_LIST_RESULT=%errorlevel%
echo [DEBUG] Ollama list result: %OLLAMA_LIST_RESULT%

if %OLLAMA_LIST_RESULT% neq 0 (
    echo [INFO] Avvio servizio Ollama...
    echo [DEBUG] Starting ollama serve...
    start /B ollama serve >nul 2>&1
    timeout /t 5 /nobreak >nul
    
    echo [DEBUG] Re-testing ollama list...
    ollama list >nul 2>&1
    set OLLAMA_LIST_RESULT2=%errorlevel%
    echo [DEBUG] Ollama list result 2: %OLLAMA_LIST_RESULT2%
    
    if %OLLAMA_LIST_RESULT2% neq 0 (
        echo [WARN] Servizio Ollama non avviato
        set OLLAMA_MISSING=1
        echo [DEBUG] Servizio fallito, saltando
        goto skip_ollama
    )
)

echo [OK] Servizio Ollama attivo
echo [DEBUG] Ollama service OK

echo.
echo 4.3- Verifica modello Mistral...
echo [DEBUG] Cercando modello mistral...
ollama list 2>nul | findstr /i "mistral" >nul
set MISTRAL_FOUND=%errorlevel%
echo [DEBUG] Mistral found result: %MISTRAL_FOUND%

if %MISTRAL_FOUND% neq 0 (
    echo [INFO] Download Mistral 7B (circa 4GB)...
    echo [INFO] ATTENDERE - Non interrompere il download!
    echo [DEBUG] Avvio download mistral...
    ollama pull mistral:7b
    set MISTRAL_PULL_RESULT=%errorlevel%
    echo [DEBUG] Mistral pull result: %MISTRAL_PULL_RESULT%
    
    if %MISTRAL_PULL_RESULT% neq 0 (
        echo [WARN] Download fallito - comando manuale: ollama pull mistral:7b
    ) else (
        echo [OK] Mistral 7B installato
    )
) else (
    echo [OK] Mistral 7B disponibile
)

echo [DEBUG] Fine controlli Ollama
goto continue_setup

:skip_ollama
echo [INFO] Configurazione Ollama saltata
echo [DEBUG] Ollama saltato

:continue_setup
echo [DEBUG] Continuazione setup - Fase 4 completata

echo.
echo FASE 5: CONFIGURAZIONE PROGETTO
echo ================================================================
echo [DEBUG] Inizio Fase 5

echo 5.1- Verifica struttura file...
set FILES_MISSING=0

if not exist "src\local_embeddings.py" (
    echo [ERRORE] File src\local_embeddings.py mancante!
    set FILES_MISSING=1
)

if not exist "src\ollama_llm.py" (
    echo [ERRORE] File src\ollama_llm.py mancante!
    set FILES_MISSING=1
)

if not exist "main.py" (
    echo [ERRORE] File main.py mancante!
    set FILES_MISSING=1
)

if %FILES_MISSING%==1 (
    echo [ERRORE] File essenziali mancanti! Verifica struttura progetto.
    pause
    exit /b 1
)

echo [OK] File principali verificati

echo.
echo 5.2- Creazione configurazione...
if not exist ".env" (
    echo # ChatBot Segreteria Studenti UniBG > .env
    echo EMBEDDING_MODEL=all-MiniLM-L6-v2 >> .env
    echo OLLAMA_BASE_URL=http://localhost:11434 >> .env
    echo OLLAMA_MODEL=mistral:7b >> .env
    echo TEMPERATURE=0.1 >> .env
    echo [OK] File .env creato
) else (
    echo [OK] File .env esistente
)

echo.
echo 5.3- Preparazione cartelle...
if not exist "data" (
    mkdir data
    echo [OK] Cartella data creata
) else (
    echo [OK] Cartella data esistente
)

if not exist "data\testi_estratti" (
    mkdir "data\testi_estratti"
    echo [OK] Cartella testi_estratti creata
) else (
    echo [OK] Cartella testi_estratti esistente
)
echo [DEBUG] Fase 5 completata

echo.
echo FASE 6: TEST FINALE
echo ================================================================
echo [DEBUG] Inizio Fase 6

echo 6.1- Test moduli sistema...
chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from local_embeddings import LocalEmbeddings; print('Moduli OK')" 2>nul
if errorlevel 1 (
    echo [WARN] Test moduli sistema fallito
    echo [INFO] Verifica manualmente: python -c "from src.local_embeddings import LocalEmbeddings"
) else (
    echo [OK] Moduli sistema verificati
)
echo [DEBUG] Fase 6 completata

echo.
echo ================================================================
echo  ✅ SETUP COMPLETATO!
echo ================================================================
echo [DEBUG] Setup completato - tutto OK
echo.
echo [PAUSA FORZATA] Premi un tasto per vedere i risultati finali...
pause

echo ⚠️  CONTROLLI FINALI:
if %OLLAMA_MISSING%==1 (
    echo [!] Ollama non configurato - installa manualmente da ollama.ai
)

if not exist "vectordb" (
    echo [!] Database vettoriale mancante - verrà creato al primo avvio
)

echo.
echo ✅ Il sistema è configurato e pronto per l'uso!
echo.
echo [DEBUG] Arrivato alla fine correttamente
echo [DEBUG] Premere un tasto per chiudere...
pause
