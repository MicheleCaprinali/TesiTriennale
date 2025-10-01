@echo off
title ChatBot UniBg - Aggiornamento Database Vettoriale
color 0E
echo.
echo ================================================================
echo  CHATBOT SEGRETERIA STUDENTI - UNIVERSITA' DI BERGAMO
echo  Aggiornamento Database Vettoriale
echo ================================================================
echo.

echo FASE 1: VERIFICA AMBIENTE
echo ================================================================

echo 1.1- Controllo ambiente virtuale...
if exist "chatbot_env\Scripts\activate.bat" (
    echo [OK] Ambiente virtuale trovato
    call chatbot_env\Scripts\activate.bat
) else (
    echo [ERRORE] Ambiente virtuale 'chatbot_env' non trovato!
    echo.
    echo SOLUZIONE:
    echo 1. Esegui: setup.bat
    echo 2. Oppure crea manualmente: python -m venv chatbot_env
    echo.
    pause
    exit /b 1
)

echo.
echo 1.2- Verifica file necessari...
if not exist "src\creazione_vectorstore.py" (
    echo [ERRORE] File src\creazione_vectorstore.py non trovato!
    pause
    exit /b 1
) else (
    echo [OK] Script creazione vectorstore presente
)

if not exist "src\testi_estratti.py" (
    echo [WARN] File src\testi_estratti.py non trovato - skip estrazione
    set SKIP_EXTRACTION=1
) else (
    echo [OK] Script estrazione testi presente
    set SKIP_EXTRACTION=0
)

echo.
echo FASE 2: ANALISI DATABASE ESISTENTE
echo ================================================================

echo 2.1- Controllo database attuale...
if exist "vectordb" (
    echo [INFO] Database vettoriale esistente trovato
    
    set /a "db_size=0"
    for /f "tokens=3" %%a in ('dir "vectordb" /s /-c ^| findstr /C:" File(s)"') do set /a "db_size=%%a"
    echo       Dimensione approssimativa: %db_size% bytes
    
    dir "vectordb" /b /s 2>nul | find /c /v "" > temp_count.txt
    set /p file_count=<temp_count.txt
    del temp_count.txt 2>nul
    echo       File nel database: %file_count%
    
    set DB_EXISTS=1
) else (
    echo [INFO] Database vettoriale non presente - creazione ex-novo
    set DB_EXISTS=0
)

echo.
echo 2.2- Controllo documenti sorgente...
if exist "data" (
    echo [OK] Cartella data presente
    
    if exist "data\testi_estratti" (
        dir "data\testi_estratti\*.txt" /b 2>nul | find /c /v "" > temp_count.txt
        set /p txt_count=<temp_count.txt
        del temp_count.txt 2>nul
        echo       Testi estratti: %txt_count% file
    ) else (
        echo [WARN] Cartella testi_estratti non presente
        set txt_count=0
    )
    
    dir "data\*.pdf" /b 2>nul | find /c /v "" > temp_count.txt
    set /p pdf_count=<temp_count.txt
    del temp_count.txt 2>nul
    echo       PDF disponibili: %pdf_count% file
    
) else (
    echo [WARN] Cartella data non presente
    set txt_count=0
    set pdf_count=0
)

echo.
echo FASE 3: CONFERMA OPERAZIONE (IMPORTANTE)
echo ================================================================
echo.

if %DB_EXISTS%==1 (
    echo  Il database vettoriale esistente SARA' COMPLETAMENTE ELIMINATO
    echo.
)

echo PROCESSO DI RICOSTRUZIONE:
if %SKIP_EXTRACTION%==0 (
    echo  1. Estrazione testi da PDF (%pdf_count% file^)
    echo  2. Chunking intelligente documenti
    echo  3. Generazione embeddings vettoriali
    echo  4. Creazione database ChromaDB
) else (
    echo  1. [SKIP] Estrazione PDF (script non disponibile^)
    echo  2. Chunking documenti esistenti
    echo  3. Generazione embeddings vettoriali
    echo  4. Creazione database ChromaDB
)

echo.

set /p confirm="Procedere con l'aggiornamento? (S/N): "
if /i "%confirm%" NEQ "S" (
    echo.
    echo  Operazione annullata
    echo.
    pause
    exit /b 0
)

echo.
echo FASE 4: BACKUP E PULIZIA
echo ================================================================

if %DB_EXISTS%==1 (
    echo 4.1- Creazione backup database esistente...
    set backup_name=vectordb_backup_%date:~-4%_%date:~3,2%_%date:~0,2%_%time:~0,2%%time:~3,2%
    set backup_name=%backup_name: =0%
    
    if exist "%backup_name%" (
        rmdir /s /q "%backup_name%" 2>nul
    )
    
    xcopy "vectordb" "%backup_name%\" /E /I /Q >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Backup fallito
    ) else (
        echo [OK] Backup creato: %backup_name%
    )
    
    echo 4.2- Rimozione database esistente...
    rmdir /s /q "vectordb" 2>nul
    if exist "vectordb" (
        echo [WARN] Rimozione incompleta
    ) else (
        echo [OK] Database esistente rimosso
    )
) else (
    echo 4.1- Database esistente non presente
)

echo.
echo FASE 5: ESTRAZIONE E PREPARAZIONE DATI
echo ================================================================

if %SKIP_EXTRACTION%==0 (
    if %pdf_count% GTR 0 (
        echo 5.1- Estrazione testi da PDF...
        echo      (Processando %pdf_count% file PDF)
        
        chatbot_env\Scripts\python.exe src\testi_estratti.py
        if errorlevel 1 (
            echo [WARN] Estrazione parzialmente fallita
        ) else (
            echo [OK] Estrazione completata
        )
    ) else (
        echo 5.1- Nessun PDF da estrarre
    )
) else (
    echo 5.1- [SKIP] Estrazione testi (script non disponibile)
)

echo.
echo 5.2- Verifica testi estratti dopo elaborazione...
if exist "data\testi_estratti" (
    dir "data\testi_estratti\*.txt" /b 2>nul | find /c /v "" > temp_count.txt
    set /p final_txt_count=<temp_count.txt
    del temp_count.txt 2>nul
    echo [INFO] Documenti disponibili per vectorstore: %final_txt_count%
    
    if %final_txt_count%==0 (
        echo [ERRORE] Nessun documento da processare!
        echo          Verifica che ci siano file in data\testi_estratti\
        pause
        exit /b 1
    )
) else (
    echo [ERRORE] Cartella testi_estratti non presente dopo estrazione!
    pause
    exit /b 1
)

echo.
echo FASE 6: RICOSTRUZIONE DATABASE VETTORIALE
echo ================================================================

echo 6.1- Avvio creazione nuovo database...
echo.
echo       Attendere... (NON interrompere il processo)

chatbot_env\Scripts\python.exe src\creazione_vectorstore.py
if errorlevel 1 (
    echo.
    echo  ERRORE nella creazione del database vettoriale!
    echo.
    echo SOLUZIONI:
    echo 1. Verifica disponibilità memoria RAM
    echo 2. Controlla integrità documenti in data\testi_estratti\
    echo 3. Reinstalla dipendenze: pip install -r requirements.txt
    echo 4. Riesegui setup.bat per verifica completa
    echo.
    
    if exist "%backup_name%" (
        echo  RIPRISTINO BACKUP:
        echo Per ripristinare il database precedente:
        echo    rmdir /s /q vectordb
        echo    ren %backup_name% vectordb
    )
    
    pause
    exit /b 1
)

echo.
echo FASE 7: VERIFICA E TEST
echo ================================================================

echo 7.1- Verifica database creato...
if exist "vectordb" (
    echo [OK] Database vettoriale ricreato
    
    dir "vectordb" /b /s 2>nul | find /c /v "" > temp_count.txt
    set /p new_file_count=<temp_count.txt
    del temp_count.txt 2>nul
    echo       Nuovi file: %new_file_count%
    
    set /a "new_db_size=0"
    for /f "tokens=3" %%a in ('dir "vectordb" /s /-c ^| findstr /C:" File(s)"') do set /a "new_db_size=%%a"
    echo       Dimensione: %new_db_size% bytes
) else (
    echo [ERRORE] Database non creato!
    pause
    exit /b 1
)

echo.
echo 7.2- Test funzionalità database...
chatbot_env\Scripts\python.exe -c "import sys; sys.path.append('src'); from creazione_vectorstore import search_vectorstore; from local_embeddings import LocalEmbeddings; result = search_vectorstore('test università bergamo', k=1, embedder=LocalEmbeddings()); print('[OK] Test ricerca completato -', len(result.get('documents', [[]])[0]), 'documenti trovati')"

if errorlevel 1 (
    echo [WARN] Test ricerca fallito
) else (
    echo [OK] Database funzionante e testato
)

echo.
echo ================================================================
echo  AGGIORNAMENTO COMPLETATO CON SUCCESSO!
echo ================================================================
echo.
pause