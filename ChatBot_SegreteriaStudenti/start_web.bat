@echo off
title ChatBot UniBG - Interfaccia Web
echo.
echo ============================================
echo  ChatBot RAG - Interfaccia Web Streamlit
echo ============================================
echo.
echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo Avvio interfaccia web...
echo.
echo  L'interfaccia sarà disponibile su: http://localhost:8501
echo  Premi Ctrl+C per fermare il server
echo.

cd interfaces
streamlit run streamlit_app.py --server.port 8501 --server.headless true

echo.
echo Server web terminato. Premi un tasto per chiudere...
pause > nul
