@echo off
title ChatBot UniBG - Setup Automatico
color 0A
echo.
echo ================================================================
echo  CHATBOT SEGRETERIA STUDENTI - UNIVERSITA' DI BERGAMO
echo  Setup Automatico Sistema RAG (Settembre 2025)
echo ================================================================
echo.
echo Tecnologie: Mistral 7B + SentenceTransformers + ChromaDB + Ollama
echo.

echo FASE 1: CONTROLLO PREREQUISITI...
echo ================================================================
echo.

echo 1.1- Verifica Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo.
    echo AZIONE RICHIESTA:
    echo 1. Installa Python 3.9+ da: https://www.python.org/downloads/
    echo 2. IMPORTANTE: Seleziona "Add Python to PATH" durante installazione
    echo 3. Riavvia il terminale dopo l'installazione
    echo 4. Riesegui questo script
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Python trovato:
    python --version
)

echo.
echo 1.2- Verifica versione Python compatibile...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Versione rilevata: %PYTHON_VERSION%
python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python 3.9+ richiesto!
    echo Versione corrente troppo vecchia.
    echo Aggiorna Python e riprova.
    pause
    exit /b 1
) else (
    echo [OK] Versione Python compatibile
)

echo.
echo FASE 2: SETUP AMBIENTE VIRTUALE
echo ================================================================
echo.

echo 2.1- Controllo ambiente virtuale...
if not exist "chatbot_env\Scripts\activate.bat" (
    echo [INFO] Creazione ambiente virtuale isolato...
    python -m venv chatbot_env
    if errorlevel 1 (
        echo [ERRORE] Impossibile creare ambiente virtuale
        echo Verifica permessi e spazio disco
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtuale "chatbot_env" creato
) else (
    echo [OK] Ambiente virtuale esistente
)

echo.
echo 2.2- Attivazione ambiente virtuale...
call chatbot_env\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Impossibile attivare ambiente virtuale
    pause
    exit /b 1
)
echo [OK] Ambiente virtuale attivo

echo.
echo FASE 3: INSTALLAZIONE DIPENDENZE
echo ================================================================
echo.

echo 3.1- Aggiornamento pip...
chatbot_env\Scripts\python.exe -m pip install --upgrade pip --quiet
echo [OK] pip aggiornato

echo.
echo 3.2- Installazione pacchetti Python...
echo Questo puo richiedere 5-10 minuti...
if not exist "requirements.txt" (
    echo [ERRORE] File requirements.txt non trovato!
    echo Verifica che il file sia presente nella cartella
    pause
    exit /b 1
)

chatbot_env\Scripts\python.exe -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERRORE] Errore nell'installazione dipendenze
    echo Verifica connessione internet e riprova
    pause
    exit /b 1
)
echo [OK] Dipendenze Python installate

echo.
echo 3.3- Test import moduli core...
chatbot_env\Scripts\python.exe -c "import sentence_transformers; print('[OK] SentenceTransformers')" 2>nul
if errorlevel 1 (
    echo [WARN] SentenceTransformers non disponibile
) 

chatbot_env\Scripts\python.exe -c "import chromadb; print('[OK] ChromaDB')" 2>nul
if errorlevel 1 (
    echo [WARN] ChromaDB non disponibile
)

chatbot_env\Scripts\python.exe -c "import requests; print('[OK] Requests')" 2>nul
echo [OK] Moduli core verificati

echo.
echo FASE 4: SETUP OLLAMA E MODELLO MISTRAL
echo ================================================================
echo.

echo 4.1- Verifica Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama non trovato!
    echo.
    echo INSTALLAZIONE OLLAMA RICHIESTA:
    echo 1. Vai su: https://ollama.ai/download/windows
    echo 2. Scarica e installa Ollama per Windows
    echo 3. Riavvia il terminale
    echo 4. Riesegui questo script
    echo.
    echo Il chatbot NON FUNZIONERA' senza Ollama!
    echo.
    pause
    goto :skip_model
) else (
    echo [OK] Ollama installato:
    ollama --version
)

echo.
echo 4.2- Verifica servizio Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo [INFO] Avvio servizio Ollama...
    start /min ollama serve
    timeout /t 5 /nobreak >nul
)

echo.
echo 4.3- Verifica modello Mistral 7B...
ollama list | findstr "mistral" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Download modello Mistral 7B...
    echo ATTENZIONE: Download di ~4GB - Tempo stimato: 10-20 minuti
    echo NON INTERROMPERE il download!
    echo.
    ollama pull mistral:7b
    if errorlevel 1 (
        echo [ERRORE] Download fallito
        echo Installa manualmente con: ollama pull mistral:7b
        pause
    ) else (
        echo [OK] Modello Mistral 7B installato
    )
) else (
    echo [OK] Modello Mistral 7B disponibile
)

:skip_model

echo.
echo FASE 5: CONFIGURAZIONE PROGETTO
echo ================================================================
echo.

echo 5.1- Creazione file configurazione...
if not exist ".env" (
    echo # Configurazione ChatBot Segreteria Studenti UniBg > .env
    echo EMBEDDING_MODEL=all-MiniLM-L6-v2 >> .env
    echo OLLAMA_BASE_URL=http://localhost:11434 >> .env
    echo OLLAMA_MODEL=mistral:7b >> .env
    echo TEMPERATURE=0.1 >> .env
    echo VECTORDB_COLLECTION=unibg_docs >> .env
    echo TICKET_URL=https://helpdesk.unibg.it/ >> .env
    echo [OK] File .env creato
) else (
    echo [OK] File .env esistente
)

echo.
echo 5.2- Verifica struttura progetto...
if not exist "src\" (
    echo [ERRORE] Cartella src\ non trovata!
    echo Verifica di essere nella cartella corretta del progetto
    pause
    exit /b 1
)

if not exist "data\" (
    echo [WARN] Cartella data\ non trovata - creazione automatica...
    mkdir data
)

set FILES_OK=1
if not exist "src\local_embeddings.py" (
    echo [ERRORE] File src\local_embeddings.py mancante!
    set FILES_OK=0
)
if not exist "src\ollama_llm.py" (
    echo [ERRORE] File src\ollama_llm.py mancante!
    set FILES_OK=0
)
if not exist "src\creazione_vectorstore.py" (
    echo [ERRORE] File src\creazione_vectorstore.py mancante!
    set FILES_OK=0
)

if %FILES_OK%==0 (
    echo [ERRORE] File del progetto mancanti!
    echo Verifica di aver estratto correttamente il progetto
    pause
    exit /b 1
)

echo [OK] Struttura progetto verificata

echo.
echo FASE 6: PREPARAZIONE DATI
echo ================================================================
echo.

echo 6.1- Verifica documenti estratti...
if not exist "data\testi_estratti\" (
    echo [INFO] Cartella testi estratti non trovata
    if exist "data\" (
        echo Verifica presenza documenti PDF in data\...
        dir /b "data\*.pdf" >nul 2>&1
        if not errorlevel 1 (
            echo [INFO] PDF trovati - estrazione automatica...
            chatbot_env\Scripts\python.exe src\testi_estratti.py
            if errorlevel 1 (
                echo [WARN] Estrazione testi fallita
            ) else (
                echo [OK] Testi estratti dai PDF
            )
        ) else (
            echo [INFO] Nessun PDF trovato in data\
        )
    )
) else (
    echo [OK] Testi estratti presenti
)

echo.
echo 6.2- Verifica database vettoriale...
if not exist "vectordb\" (
    echo [INFO] Database vettoriale non trovato - creazione...
    echo Questo processo puo richiedere 3-5 minuti...
    chatbot_env\Scripts\python.exe src\creazione_vectorstore.py
    if errorlevel 1 (
        echo [WARN] Creazione database fallita
        echo Eseguire manualmente: python src\creazione_vectorstore.py
    ) else (
        echo [OK] Database vettoriale creato
    )
) else (
    echo [OK] Database vettoriale esistente
)

echo.
echo FASE 7: TEST FINALE SISTEMA
echo ================================================================
echo.

echo 7.1- Test moduli Python...
chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from local_embeddings import LocalEmbeddings; print('[OK] LocalEmbeddings importato')" 2>nul
if errorlevel 1 (
    echo [WARN] Problema con LocalEmbeddings
)

chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from ollama_llm import OllamaLLM; print('[OK] OllamaLLM importato')" 2>nul
if errorlevel 1 (
    echo [WARN] Problema con OllamaLLM
)

echo.
echo 7.2- Test connessione Ollama...
chatbot_env\Scripts\python.exe -c "import requests; r=requests.get('http://localhost:11434/api/tags', timeout=3); print('[OK] Ollama raggiungibile')" 2>nul
if errorlevel 1 (
    echo [WARN] Ollama non raggiungibile - verificare che sia in esecuzione
)

echo.
echo ================================================================
echo  SETUP COMPLETATO!
echo ================================================================
echo.
echo [SUCCESS] Sistema ChatBot RAG configurato correttamente!
echo.
echo CARATTERISTICHE INSTALLATE:
echo   - Ambiente virtuale isolato: chatbot_env\
echo   - SentenceTransformers per embedding semantici
echo   - ChromaDB per database vettoriale
echo   - Ollama + Mistral 7B per generazione risposte
echo   - Sistema RAG ottimizzato per performance
echo.
echo COMANDI DISPONIBILI:
echo   - python main.py              : Avvia chatbot CLI
echo   - python main.py --check      : Verifica sistema  
echo   - python main.py --help       : Mostra aiuto
echo.
echo NOTA IMPORTANTE:
echo Per utilizzare il chatbot, SEMPRE attivare l'ambiente virtuale:
echo   chatbot_env\Scripts\activate
echo Poi eseguire: python main.py
echo.

if not exist "vectordb\" (
    echo [ATTENZIONE] Database vettoriale non presente!
    echo Il chatbot non funzionera senza database.
    echo Esegui: python src\creazione_vectorstore.py
    echo.
)

ollama list | findstr "mistral" >nul 2>&1
if errorlevel 1 (
    echo [ATTENZIONE] Modello Mistral non presente!
    echo Il chatbot non funzionera senza il modello LLM.
    echo Installa con: ollama pull mistral:7b
    echo.
)

echo Premi un tasto per chiudere...
pause >nul