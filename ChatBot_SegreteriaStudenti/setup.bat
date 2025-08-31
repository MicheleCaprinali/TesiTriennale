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
echo Controllo compilatori C++...
cl /? > nul 2>&1
if errorlevel 1 (
    echo [WARN] Microsoft C++ Build Tools non trovati
    echo.
    echo Questo potrebbe causare errori nella compilazione di alcune dipendenze.
    echo.
    echo Per installare i Build Tools:
    echo 1. Vai su: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo 2. Scarica "Build Tools for Visual Studio"
    echo 3. Installa con "C++ build tools" selezionato
    echo.
    echo ALTERNATIVA: Prova prima senza Build Tools (useremo wheels pre-compilati)
    echo.
    set /p buildtools_choice=Continuare senza Build Tools? (y/n): 
    if /i not "%buildtools_choice%"=="y" (
        echo Aprendo pagina download Build Tools...
        start https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo Rilancia questo script dopo l'installazione
        pause
        exit /b 1
    )
    echo [INFO] Continuo con installazione usando wheels pre-compilati...
) else (
    echo [OK] Compilatori C++ disponibili
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
venv\Scripts\python.exe -m pip install --upgrade pip wheel setuptools
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
echo [INFO] Installazione semplificata senza versioni specifiche...

REM Installazione step-by-step per evitare conflitti
echo [INFO] Installazione PyTorch (CPU only)...
venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo [WARN] Installazione PyTorch fallita, provo versione standard...
    venv\Scripts\python.exe -m pip install torch
)

echo [INFO] Installazione dipendenze principali...
venv\Scripts\python.exe -m pip install requests PyPDF2 ollama
if errorlevel 1 (
    echo [WARN] Errore in alcune dipendenze base
)

echo [INFO] Installazione Sentence Transformers...
venv\Scripts\python.exe -m pip install sentence-transformers
if errorlevel 1 (
    echo [WARN] Errore installazione Sentence Transformers
)

echo [INFO] Installazione ChromaDB...
venv\Scripts\python.exe -m pip install chromadb
if errorlevel 1 (
    echo [WARN] Errore installazione ChromaDB
)

echo [INFO] Installazione Streamlit...
venv\Scripts\python.exe -m pip install streamlit
if errorlevel 1 (
    echo [WARN] Errore installazione Streamlit
)

echo [INFO] Verifica installazione finale...
venv\Scripts\python.exe -m pip list | findstr -i "torch sentence-transformers chromadb streamlit"

REM Se tutto fallisce, installa da requirements.txt
if errorlevel 1 (
    echo [INFO] Tentativo installazione da requirements.txt...
    venv\Scripts\python.exe -m pip install -r requirements.txt --no-deps --force-reinstall
    if errorlevel 1 (
        echo [ERRORE] Errore nell'installazione delle dipendenze
        echo.
        echo SOLUZIONI POSSIBILI:
        echo 1. Installa Microsoft C++ Build Tools:
        echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo 2. Prova installazione manuale singola:
        echo    venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
        echo    venv\Scripts\python.exe -m pip install sentence-transformers
        echo    venv\Scripts\python.exe -m pip install chromadb
        echo    venv\Scripts\python.exe -m pip install streamlit
        echo 3. Usa conda invece di pip (Anaconda/Miniconda)
        echo.
        echo Vuoi aprire la pagina dei Build Tools? (y/n)
        set /p open_buildtools=
        if /i "%open_buildtools%"=="y" (
            start https://visualstudio.microsoft.com/visual-cpp-build-tools/
        )
        pause
        exit /b 1
    )
)

echo [OK] Dipendenze installate

echo.
echo 6- Test configurazione...
echo [INFO] Verifica dipendenze principali...
venv\Scripts\python.exe -c "import sentence_transformers; print('[OK] Sentence Transformers importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] Sentence Transformers: ERRORE"
)

venv\Scripts\python.exe -c "import chromadb; print('[OK] ChromaDB importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] ChromaDB: ERRORE"
)

venv\Scripts\python.exe -c "import streamlit; print('[OK] Streamlit importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] Streamlit: ERRORE"
)

venv\Scripts\python.exe -c "import torch; print('[OK] PyTorch importato correttamente')" 2>nul
if errorlevel 1 (
    echo [WARN] PyTorch: ERRORE"
)

echo [INFO] Se vedi errori sopra, alcune funzionalità potrebbero non funzionare
echo       Ma il sistema base dovrebbe essere operativo

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