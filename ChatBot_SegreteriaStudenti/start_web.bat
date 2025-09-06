@echo off
title ChatBot UniBG - Interfaccia Web
echo.
echo ============================================
echo  ChatBot RAG - Interfaccia Web Streamlit
echo ============================================
echo.

echo Verifica ambiente virtuale...
if not exist "venv\Scripts\activate.bat" (
    echo [ERRORE] Ambiente virtuale non trovato!
    echo Esegui prima: setup_auto.bat
    pause
    exit /b 1
)

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo Verifica dipendenze...
venv\Scripts\python.exe -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Streamlit non installato!
    echo Esegui: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Avvio interfaccia web...
echo.
echo  URL: http://localhost:8501
echo  Per fermareː Ctrl+C
echo  Per aprire browser automaticamenteː aggiungi --browser
echo.

venv\Scripts\python.exe -m streamlit run interfaces\streamlit_app.py --server.port 8501 --server.headless true --browser.serverAddress localhost

echo.
echo Server web terminato. Premi un tasto per chiudere...
pause > nul
