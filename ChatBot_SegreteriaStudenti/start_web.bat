@echo off
title ChatBot UniBG - Interfaccia Web
color 0B
echo.
echo ================================================================
echo  CHATBOT SEGRETERIA STUDENTI - UNIVERSITA' DI BERGAMO
echo  Interfaccia Web Streamlit (Settembre 2025)
echo ================================================================
echo.

echo FASE 1: VERIFICA AMBIENTE
echo ================================================================

echo 1.1- Controllo ambiente virtuale...
if not exist "chatbot_env\Scripts\activate.bat" (
    echo [ERRORE] Ambiente virtuale 'chatbot_env' non trovato!
    echo.
    echo SOLUZIONE:
    echo 1. Esegui: setup.bat
    echo 2. Oppure crea manualmente: python -m venv chatbot_env
    echo 3. Installa dipendenze: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Ambiente virtuale trovato
)

echo.
echo 1.2- Attivazione ambiente virtuale...
call chatbot_env\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Impossibile attivare ambiente virtuale
    pause
    exit /b 1
) else (
    echo [OK] Ambiente virtuale attivo
)

echo.
echo FASE 2: VERIFICA DIPENDENZE
echo ================================================================

echo 2.1- Verifica Streamlit...
chatbot_env\Scripts\python.exe -c "import streamlit; print('[OK] Streamlit v' + streamlit.__version__)" 2>nul
if errorlevel 1 (
    echo [ERRORE] Streamlit non installato!
    echo Installazione automatica...
    chatbot_env\Scripts\python.exe -m pip install streamlit
    if errorlevel 1 (
        echo [ERRORE] Installazione fallita
        echo Esegui manualmente: pip install streamlit
        pause
        exit /b 1
    )
    echo [OK] Streamlit installato
)

echo.
echo 2.2- Verifica file interfaccia...
if not exist "interfaccia\streamlit.py" (
    echo [ERRORE] File interfaccia\streamlit.py non trovato!
    echo Verifica che il file esista nella cartella corretta
    pause
    exit /b 1
) else (
    echo [OK] File interfaccia presente
)

echo.
echo 2.3- Test import moduli core...
chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from local_embeddings import LocalEmbeddings; print('[OK] LocalEmbeddings')" 2>nul
if errorlevel 1 (
    echo [WARN] Problema con LocalEmbeddings - il chatbot potrebbe non funzionare
)

chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from ollama_llm import OllamaLLM; print('[OK] OllamaLLM')" 2>nul
if errorlevel 1 (
    echo [WARN] Problema con OllamaLLM - il chatbot potrebbe non funzionare
)

echo.
echo FASE 3: VERIFICA SERVIZI
echo ================================================================

echo 3.1- Controllo Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama non trovato! Il chatbot NON funzionera
    echo Installa da: https://ollama.ai
) else (
    echo [OK] Ollama disponibile
    
    echo 3.2- Verifica servizio Ollama...
    ollama list >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Avvio servizio Ollama...
        start /min "Ollama Server" ollama serve
        timeout /t 3 /nobreak >nul
    )
    
    echo 3.3- Verifica modello Mistral...
    ollama list | findstr "mistral" >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Modello Mistral non trovato!
        echo Installa con: ollama pull mistral:7b
    ) else (
        echo [OK] Modello Mistral disponibile
    )
)

echo.
echo 3.4- Verifica database vettoriale...
if not exist "vectordb" (
    echo [WARN] Database vettoriale non trovato!
    echo Esegui: python src\creazione_vectorstore.py
) else (
    echo [OK] Database vettoriale presente
)

echo.
echo ================================================================
echo  AVVIO INTERFACCIA WEB
echo ================================================================
echo.
echo  URL Locale:     http://localhost:8501
echo  URL Rete:       http://192.168.1.XXX:8501
echo  Controlli:      Ctrl+C per fermare
echo  Browser:        Si apre automaticamente
echo.
echo  SUGGERIMENTI:
echo  - Se la porta 8501 e occupata, cambiera automaticamente
echo  - Per condividere in rete: --server.address 0.0.0.0
echo  - Per disabilitare browser: --server.headless true
echo.

echo [INFO] Avvio Streamlit...
echo.

chatbot_env\Scripts\python.exe -m streamlit run interfaccia\streamlit.py ^
    --server.port 8501 ^
    --server.address localhost ^
    --browser.gatherUsageStats false ^
    --server.fileWatcherType none ^
    --theme.base dark ^
    --theme.primaryColor "#3b82f6" ^
    --theme.backgroundColor "#1a1a1a" ^
    --theme.secondaryBackgroundColor "#2a2a2a" ^
    --theme.textColor "#ffffff"

echo.
echo ================================================================
echo  SERVER WEB TERMINATO
echo ================================================================
echo.

if errorlevel 1 (
    echo [ERRORE] Errore durante l'esecuzione di Streamlit
    echo.
    echo POSSIBILI CAUSE:
    echo 1. Porta 8501 gia in uso
    echo 2. Errore nel codice Python
    echo 3. Dipendenze mancanti
    echo.
    echo SOLUZIONI:
    echo 1. Chiudi altre istanze di Streamlit
    echo 2. Verifica log di errore sopra
    echo 3. Riesegui setup.bat
    echo.
) else (
    echo [SUCCESS] Interfaccia web terminata correttamente
)

echo Premi un tasto per chiudere...
pause >nul