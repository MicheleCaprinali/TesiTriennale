@echo off
title ChatBot UniBG - Interfaccia Web
echo.
echo ============================================
echo  ChatBot RAG - Interfaccia Web Streamlit
echo ============================================
echo.
echo Attivazione ambiente virtuale...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERRORE] Ambiente virtuale non trovato!
    echo Esegui prima: setup.bat
    pause
    exit /b 1
)

echo Avvio interfaccia web...
echo.
echo  L'interfaccia sara' disponibile su: http://localhost:8501
echo  Premi Ctrl+C per fermare il server
echo.

venv\Scripts\python.exe -m streamlit run interfaces\streamlit_app.py --server.port 8501 --server.headless true

echo.
echo Server web terminato. Premi un tasto per chiudere...
pause > nul
