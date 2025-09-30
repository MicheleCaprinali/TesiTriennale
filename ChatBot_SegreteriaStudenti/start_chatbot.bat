@echo off
title ChatBot UniBG - Console CLI
color 0A
echo.
echo ================================================================
echo  CHATBOT SEGRETERIA STUDENTI - UNIVERSITA' DI BERGAMO
echo  Modalità Console CLI (Settembre 2025)
echo ================================================================
echo.

echo FASE 1: VERIFICA AMBIENTE
echo ================================================================

echo 1.1- Controllo ambiente virtuale...
if exist "chatbot_env\Scripts\activate.bat" (
    echo [OK] Ambiente virtuale 'chatbot_env' trovato
    call chatbot_env\Scripts\activate.bat
    echo [OK] Ambiente virtuale attivato
) else (
    echo [ERRORE] Ambiente virtuale 'chatbot_env' non trovato!
    echo.
    echo SOLUZIONE:
    echo 1. Esegui: setup.bat
    echo 2. Oppure crea manualmente: python -m venv chatbot_env
    echo 3. Installa dipendenze: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo 1.2- Verifica Python nell'ambiente...
chatbot_env\Scripts\python.exe -c "import sys; print('[OK] Python:', sys.version.split()[0], 'in', sys.executable)"
if errorlevel 1 (
    echo [ERRORE] Python non funzionante nell'ambiente virtuale
    pause
    exit /b 1
)

echo.
echo FASE 2: VERIFICA DIPENDENZE
echo ================================================================

echo 2.1- Controllo SentenceTransformers...
chatbot_env\Scripts\python.exe -c "import sentence_transformers; print('[OK] SentenceTransformers v' + sentence_transformers.__version__)" 2>nul
if errorlevel 1 (
    echo [ERRORE] SentenceTransformers mancante!
    echo Installazione automatica...
    chatbot_env\Scripts\python.exe -m pip install sentence-transformers
    if errorlevel 1 (
        echo [ERRORE] Installazione fallita
        echo Esegui manualmente: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo [OK] SentenceTransformers installato
)

echo.
echo 2.2- Controllo ChromaDB...
chatbot_env\Scripts\python.exe -c "import chromadb; print('[OK] ChromaDB disponibile')" 2>nul
if errorlevel 1 (
    echo [WARN] ChromaDB non trovato - il chatbot potrebbe non funzionare
)

echo.
echo 2.3- Controllo moduli core...
chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from local_embeddings import LocalEmbeddings; print('[OK] LocalEmbeddings')" 2>nul
if errorlevel 1 (
    echo [ERRORE] Modulo LocalEmbeddings non trovato!
    echo Verifica che il file src\local_embeddings.py esista
    pause
    exit /b 1
)

chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from ollama_llm import OllamaLLM; print('[OK] OllamaLLM')" 2>nul
if errorlevel 1 (
    echo [ERRORE] Modulo OllamaLLM non trovato!
    echo Verifica che il file src\ollama_llm.py esista
    pause
    exit /b 1
)

echo.
echo FASE 3: VERIFICA SERVIZI
echo ================================================================

echo 3.1- Controllo file main.py...
if not exist "main.py" (
    echo [ERRORE] File main.py non trovato!
    echo Verifica che main.py sia nella cartella principale
    pause
    exit /b 1
) else (
    echo [OK] File main.py presente
)

echo.
echo 3.2- Controllo database vettoriale...
if not exist "vectordb" (
    echo [WARN] Database vettoriale non trovato!
    echo Per crearlo: aggiornamento_db.bat
    echo Il chatbot funzionerà con capacità limitate
) else (
    echo [OK] Database vettoriale presente
)

echo.
echo 3.3- Test rapido Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama non installato - Risposte limitate!
    echo Installa da: https://ollama.ai
) else (
    echo [OK] Ollama disponibile
    
    ollama list >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Avvio servizio Ollama in background...
        start /min "Ollama Server" ollama serve
        timeout /t 2 /nobreak >nul
    )
    
    ollama list 2>nul | findstr "mistral" >nul
    if errorlevel 1 (
        echo [WARN] Modello Mistral non trovato!
        echo Scarica con: ollama pull mistral:7b
    ) else (
        echo [OK] Modello Mistral disponibile
    )
)

echo.
echo ================================================================
echo  AVVIO CHATBOT CONSOLE
echo ================================================================
echo.

echo 🤖 CHATBOT SEGRETERIA STUDENTI - UniBg
echo 📋 Modalità: Console CLI Interattiva
echo 🔧 Tecnologie: RAG + Mistral 7B + SentenceTransformers
echo.

echo 💡 COMANDI DISPONIBILI:
echo    ▶️  Scrivi una domanda e premi INVIO
echo    ▶️  'exit', 'quit' o 'bye' per uscire
echo    ▶️  'help' per mostrare esempi
echo    ▶️  'status' per info sistema
echo    ▶️  Ctrl+C per interruzione forzata
echo.

echo 🎯 ESEMPI DI DOMANDE:
echo    • "Come iscriversi agli esami?"
echo    • "Orari della segreteria studenti?"  
echo    • "Informazioni su tasse universitarie?"
echo    • "Servizi per studenti con disabilità?"
echo    • "Come richiedere certificati?"
echo.

echo ▶️  Premi un tasto per avviare il chatbot...
pause >nul

echo.
echo ================================================================
echo.

chatbot_env\Scripts\python.exe main.py

echo.
echo ================================================================
echo  SESSIONE CHATBOT TERMINATA
echo ================================================================

if errorlevel 1 (
    echo.
    echo ❌ Il chatbot si è chiuso con errori
    echo.
    echo POSSIBILI CAUSE:
    echo 1. Errore nei moduli Python
    echo 2. Ollama non disponibile  
    echo 3. Database vettoriale corrotto
    echo 4. Memoria insufficiente
    echo.
    echo SOLUZIONI:
    echo 1. Riesegui setup.bat per verifica completa
    echo 2. Verifica log di errore sopra
    echo 3. Prova python main.py --check per diagnostica
    echo 4. Aggiorna database: aggiornamento_db.bat
    echo.
) else (
    echo.
    echo ✅ Chatbot terminato correttamente
    echo.
    echo 📊 ALTRI COMANDI DISPONIBILI:
    echo    • start_web.bat           # Interfaccia web Streamlit
    echo    • aggiornamento_db.bat    # Aggiorna database documenti
    echo    • python main.py --check  # Diagnostica sistema
    echo.
)

echo Premi un tasto per chiudere...
pause >nul