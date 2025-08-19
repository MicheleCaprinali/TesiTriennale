@echo off
title ChatBot UniBG - Console
echo.
echo ============================================
echo  ChatBot RAG - Segreteria Studenti UniBG
echo ============================================
echo.
echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo Avvio ChatBot in modalità console...
echo.
echo     Comandi disponibili:
echo    - Scrivi la tua domanda e premi INVIO
echo    - Scrivi 'exit' per uscire
echo.

python main.py

echo.
echo ChatBot terminato. Premi un tasto per chiudere...
pause > nul
