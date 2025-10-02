# CHATBOT SEGRETERIA STUDENTI - GUIDA UTENTE# CHATBOT SEGRETERIA STUDENTI - GUIDA UTENTE



Sistema RAG per assistenza automatica agli studenti universitari.Sistema RAG per assistenza automatica agli studenti universitari.



## FUNZIONALITÀ## FUNZIONALITÀ



Il chatbot risponde a domande su:Il chatbot risponde a domande su:

- Iscrizioni agli esami- Iscrizioni agli esami

- Tasse e pagamenti- Tasse e pagamenti

- Certificati e documenti- Certificati e documenti

- Orari e contatti segreteria- Orari e contatti segreteria

- Servizi per studenti- Servizi per studenti

- Carriera universitaria- Carriera universitaria

- Orientamento e tirocini- Orientamento e tirocini



------



# GUIDA RAPIDA# GUIDA RAPIDA



## IMPORTANTE - REQUISITO FONDAMENTALE## IMPORTANTE - REQUISITO FONDAMENTALE



**Ogni comando Python richiede l'attivazione dell'ambiente virtuale `chatbot_env/`.****Ogni comando Python richiede l'attivazione dell'ambiente virtuale `chatbot_env/`.**  

Senza questo passaggio il progetto non funzionerà.

---

---

## STEP 0: ATTIVAZIONE AMBIENTE VIRTUALE

## STEP 0: ATTIVAZIONE AMBIENTE VIRTUALE

```bash

cd C:\Users\miche\Desktop\TesiTriennale2025\Chatbot_SegreteriaStudenti### Sempre prima di ogni operazione

```

```bash

**Windows CMD:**# Naviga nella cartella principale

```cmdcd C:\Users\miche\Desktop\TesiTriennale2025\Chatbot_SegreteriaStudenti

chatbot_env\Scripts\activate.bat```

```

**Windows CMD:**

**Windows PowerShell:**```cmd

```powershellchatbot_env\Scripts\activate.bat

.\chatbot_env\Scripts\Activate.ps1```

```

**Windows PowerShell:**

**Linux/Mac:**```powershell

```bash.\chatbot_env\Scripts\Activate.ps1

source chatbot_env/bin/activate```

```

**Linux/Mac:**

### Verifica attivazione```bash

source chatbot_env/bin/activate

Il prompt deve mostrare `(chatbot_env)`:```

```

(chatbot_env) C:\Users\miche\...\Chatbot_SegreteriaStudenti>### Verifica attivazione

```

Il prompt deve mostrare `(chatbot_env)` all'inizio della riga:

---```

(chatbot_env) C:\Users\miche\Desktop\TesiTriennale2025\Chatbot_SegreteriaStudenti>

## STEP 1: VERIFICA DIPENDENZE```



**Verifica pacchetti:**Se non vedi `(chatbot_env)`, l'ambiente non è attivo e i comandi Python falliranno

```powershell

pip list---

```

## STEP 1: VERIFICA DIPENDENZE

**Test librerie:**

Assicurati che l'ambiente virtuale sia attivo (vedi `(chatbot_env)` nel prompt).

**CMD:**

```cmd**Verifica pacchetti installati:**

python -c "import chromadb, sentence_transformers, streamlit; print('OK')"

```**CMD/PowerShell:**

```powershell

**PowerShell:**pip list

```powershell```

python -c "import chromadb, sentence_transformers, streamlit; print('OK')"

```**Test librerie principali:**



**Se mancano dipendenze:****CMD:**

```powershell```cmd

pip install -r requirements.txtpython -c "import chromadb, sentence_transformers, streamlit; print('Dipendenze OK')"

``````



---**PowerShell:**

```powershell

## STEP 2: AVVIA IL CHATBOTpython -c "import chromadb, sentence_transformers, streamlit; print('Dipendenze OK')"

```

### Checklist pre-avvio

- Ambiente virtuale attivo? `(chatbot_env)` visibile**Se mancano dipendenze:**

- Dipendenze installate? `pip list` mostra chromadb, streamlit

- Ollama avviato? Vedi sezione Ollama sotto**CMD/PowerShell:**

```powershell

### Modalità 1: Consolepip install -r requirements.txt

```

**CMD/PowerShell:**

```powershell---

python main.py

```## STEP 2: AVVIA IL CHATBOT



### Modalità 2: Interface Web (Streamlit)### Checklist pre-avvio

- Ambiente virtuale attivo? (`(chatbot_env)` visibile nel prompt)

**CMD/PowerShell:**- Dipendenze installate? (`pip list` mostra chromadb, streamlit)

```powershell- Ollama installato e avviato? (vedi sezione Ollama sotto)

streamlit run interfaccia/streamlit.py

```### Modalità 1: Console



Browser apre su: `http://localhost:8501`**CMD:**

```cmd

### Test rapidopython main.py

```

**CMD/PowerShell:**

```powershell**PowerShell:**

python src/creazione_vectorstore.py```powershell

```python main.py

```

---

Output atteso:

# RISOLUZIONE PROBLEMI```

Chatbot avviato! Digita la tua domanda...

## PROBLEMA 1: "ModuleNotFoundError"> Come mi iscrivo all'esame?

```

**Causa:** Ambiente virtuale non attivo.

### Modalità 2: Interface Web (Streamlit)

**CMD:**

```cmd**CMD:**

chatbot_env\Scripts\activate.bat```cmd

```streamlit run interfaccia/streamlit.py

```

**PowerShell:**

```powershell**PowerShell:**

.\chatbot_env\Scripts\Activate.ps1```powershell

```streamlit run interfaccia/streamlit.py

```

**Linux/Mac:**

```bashBrowser si apre automaticamente su: `http://localhost:8501`

source chatbot_env/bin/activate

```### Test rapido del sistema



---**CMD/PowerShell:**

```powershell

## PROBLEMA 2: "No module named 'chromadb'"python src/creazione_vectorstore.py

python evaluation/metriche_qualita.py

**Causa:** Dipendenze non installate.```

---

**Soluzione:**

```powershell# 🛠️ **RISOLUZIONE PROBLEMI**

pip install -r requirements.txt

```## **❌ PROBLEMI COMUNI E SOLUZIONI:**



**Verifica CMD:**### **� PROBLEMA #1: "ModuleNotFoundError" o "comando python non trovato"**

```cmd

pip list | findstr chromadb**Causa:** Ambiente virtuale NON attivo!

```

**Soluzione:**

**Verifica PowerShell:**```bash

```powershell# Controlla se vedi (chatbot_env) nel prompt

pip list | Select-String chromadb# Se NON lo vedi, attiva l'ambiente:

```

# Windows:

**Verifica Linux/Mac:**chatbot_env\Scripts\activate

```bash

pip list | grep chromadb# Linux/Mac:

```source chatbot_env/bin/activate



---# Ora riprova il comando che dava errore

```

## PROBLEMA 3: Ollama non risponde

---

**Installazione:**

- Windows: https://ollama.ai/download### **� PROBLEMA #2: "No module named 'chromadb'" (o altra libreria)**

- Linux: `curl -fsSL https://ollama.ai/install.sh | sh`

- Mac: `brew install ollama`**Causa:** Dipendenze non installate nell'ambiente virtuale



**Avvia servizio (terminale separato):****Soluzione:**

```bash```bash

ollama serve# 1. PRIMA attiva l'ambiente virtuale (vedi Problema #1)

```# 2. POI installa le dipendenze:



**Scarica modello:**pip install -r requirements.txt

```bash

ollama pull mistral# 3. Verifica installazione:

```pip list | findstr chromadb    # Windows

pip list | grep chromadb       # Linux/Mac

**Test connessione (con ambiente virtuale attivo):**```



**CMD:**---

```cmd

python -c "import requests; print(requests.get('http://localhost:11434').status_code)"### **🔴 PROBLEMA #3: Ollama non risponde o errore connessione**

```

**Causa:** Ollama non installato o servizio non avviato

**PowerShell:**

```powershell**Soluzione:**

python -c "import requests; print(requests.get('http://localhost:11434').status_code)"

```**PASSO 1 - Installa Ollama:**

- **Windows**: Scarica da https://ollama.ai/download

Output atteso: `200`- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

- **Mac**: `brew install ollama`

---

**PASSO 2 - Avvia servizio Ollama:**

## PROBLEMA 4: Database vettoriale corrotto```bash

# Apri un NUOVO terminale separato (senza ambiente virtuale)

**CMD:**ollama serve

```cmd

rmdir /s /q vectordb# Tieni questo terminale aperto mentre usi il chatbot

python src/creazione_vectorstore.py```

```

**PASSO 3 - Scarica il modello:**

**PowerShell:**```bash

```powershell# In un ALTRO terminale separato

Remove-Item -Recurse -Force vectordbollama pull mistral

python src/creazione_vectorstore.py

```# Oppure (modello alternativo):

ollama pull llama2

**Linux/Mac:**```

```bash

rm -rf vectordb/**PASSO 4 - Testa connessione:**

python src/creazione_vectorstore.py```bash

```# Nel terminale CON ambiente virtuale attivo:

python -c "import requests; print(requests.get('http://localhost:11434').status_code)"

---

# Output atteso: 200

## PROBLEMA 5: Port 8501 già in uso```



**Usa porta diversa:**---

```powershell

streamlit run interfaccia/streamlit.py --server.port 8502### **� PROBLEMA #4: Database vettoriale corrotto o errore ChromaDB**

```

**Causa:** Database vectordb/ danneggiato

**Chiudi processo CMD:**

```cmd**Soluzione:**

netstat -ano | findstr :8501```bash

taskkill /F /PID <PID_NUMBER># ⚠️ PRIMA attiva ambiente virtuale!

```

# 1. Elimina database corrotto

**Chiudi processo PowerShell:**# Windows:

```powershellrmdir /s /q vectordb

Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess | Stop-Process -Force

```# Linux/Mac:

rm -rf vectordb/

**Chiudi processo Linux/Mac:**

```bash# 2. Ricrea database da zero

lsof -ti:8501 | xargs kill -9python src/creazione_vectorstore.py

```

# 3. Attendi completamento (~2-3 minuti)

---```



## PROBLEMA 6: Ambiente virtuale non si attiva (Windows)---



**PowerShell (esegui una volta):**### **🔴 PROBLEMA #5: Port 8501 già in uso (Streamlit)**

```powershell

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser**Causa:** Un'altra istanza di Streamlit è già in esecuzione

```

**Soluzione:**

**Poi riprova:**```bash

```powershell# Opzione A - Usa porta diversa:

.\chatbot_env\Scripts\Activate.ps1streamlit run interfaccia/streamlit.py --server.port 8502

```

# Opzione B - Chiudi processo esistente:

---# Windows:

netstat -ano | findstr :8501

# STRUTTURA PROGETTOtaskkill /F /PID <PID_NUMBER>



```# Linux/Mac:

Chatbot_SegreteriaStudenti/lsof -ti:8501 | xargs kill -9

├── chatbot_env/              Ambiente virtuale - ATTIVARE SEMPRE```

│   ├── Scripts/              

│   │   ├── activate.bat      Attivazione CMD---

│   │   ├── Activate.ps1      Attivazione PowerShell

│   │   └── python.exe        Interprete Python isolato### **🔴 PROBLEMA #6: Ambiente virtuale non si attiva**

│   └── Lib/site-packages/    Dipendenze installate

│**Causa:** Permessi di esecuzione (Windows) o path errato

├── src/                      Codice sorgente

│   ├── ollama_llm.py         Engine LLM (Mistral 7B)**Soluzione Windows:**

│   ├── creazione_vectorstore.py  Database vettoriale```powershell

│   ├── local_embeddings.py   Embeddings (all-MiniLM-L6-v2)# Se PowerShell blocca l'attivazione:

│   ├── link_enhancer.py      Link automaticiSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

│   ├── prompt_templates.py   Template prompt

│   ├── dividi_chunks.py      Chunking documenti# Poi riprova:

│   └── testi_estratti.py     Estrazione PDFchatbot_env\Scripts\activate

│```

├── interfaccia/

│   └── streamlit.py          Web app (localhost:8501)**Soluzione Linux/Mac:**

│```bash

├── data/# Verifica che il file activate esista

│   ├── FAQ/                  15 file FAQls chatbot_env/bin/activate

│   ├── guida_dello_studente/ 4 PDF guide UniBG

│   └── testi_estratti/       Testi processati# Se manca, ricrea ambiente:

│python3 -m venv chatbot_env

├── vectordb/                 Database ChromaDBsource chatbot_env/bin/activate

│   ├── chroma.sqlite3        Database SQLitepip install -r requirements.txt

│   └── d55e47f0.../          Embeddings (384 dim)```

│---

├── evaluation/               Sistema valutazione

│   ├── metriche_avanzate.py  Metriche RAG# 📁 **STRUTTURA REALE PROGETTO**

│   ├── metriche_qualita.py   Qualità risposte

│   └── metriche_software.py  Metriche codice```

│📂 Chatbot_SegreteriaStudenti/

├── results/                  Risultati testing├── � chatbot_env/                 # ⭐ AMBIENTE VIRTUALE - ATTIVARE SEMPRE! ⭐

│   ├── metriche_rag_results.json│   ├── Scripts/                   # Eseguibili Python e script attivazione

│   ├── confronto_qualita_rag.png│   │   ├── activate.bat          # Attivazione Windows CMD

│   └── metriche_software_*.png│   │   ├── Activate.ps1          # Attivazione Windows PowerShell

││   │   └── python.exe            # Interprete Python isolato

├── test/                     Suite test│   ├── Lib/site-packages/        # Tutte le dipendenze installate

│   ├── unit/                 Test unitari moduli src/│   └── pyvenv.cfg                # Configurazione ambiente

│   ├── performance/          Test prestazionali│

│   ├── results/              Risultati + grafici PNG├── �📁 src/                         # Codice sorgente principale

│   └── run_tests.py          Runner test│   ├── ollama_llm.py              # Engine LLM (Mistral 7B) ⭐

││   ├── creazione_vectorstore.py   # Setup database vettoriale ChromaDB

├── documentazione/│   ├── local_embeddings.py        # Gestione embeddings (all-MiniLM-L6-v2)

│   ├── README.md             Questa guida│   ├── link_enhancer.py           # Sistema link automatici nelle risposte

│   ├── TECHNICAL_GUIDE.md    Guida tecnica│   ├── prompt_templates.py        # Template ottimizzati per prompt

│   ├── QUICK_START.md        Guida semplificata│   ├── dividi_chunks.py           # Chunking intelligente documenti

│   └── INDICE.md             Indice documentazione│   └── testi_estratti.py          # Estrazione testi da PDF

││

├── main.py                   Entry point - ChatbotRAG├── 📁 interfaccia/                 # Interface utente

├── requirements.txt          Dipendenze Python│   └── streamlit.py               # Web app moderna (localhost:8501) ⭐

├── start_chatbot.bat         Avvio rapido console│

└── start_web.bat             Avvio rapido web├── 📁 data/                        # Database conoscenza

```│   ├── FAQ/                       # 15 file FAQ categorizzati

│   ├── guida_dello_studente/      # 4 PDF guide ufficiali UniBG

### File chiave│   └── testi_estratti/            # Testi estratti e processati

│

1. `main.py` - Classe `ChatbotRAG` con metodo `chat()`├── 📁 vectordb/                    # Database vettoriale ChromaDB

2. `interfaccia/streamlit.py` - Interface web│   ├── chroma.sqlite3             # Database SQLite principale

3. `src/ollama_llm.py` - Comunicazione Mistral 7B│   └── d55e47f0.../              # Embeddings vettoriali (384 dim)

4. `src/creazione_vectorstore.py` - Vector database│

5. `requirements.txt` - Dipendenze├── 📁 evaluation/                  # Sistema valutazione automatica

6. `test/run_tests.py` - Esegui test│   ├── metriche_avanzate.py       # Metriche RAG (context/answer relevancy)

│   ├── metriche_qualita.py        # Qualità risposte (completezza/utilità)

---│   └── metriche_software.py       # Metriche codice (WMC, LCOM, CBO)

│

# ESEGUIRE I TEST├── 📁 results/                     # Risultati testing e grafici

│   ├── metriche_rag_results.json  # Risultati metriche RAG

**Prerequisito:** Ambiente virtuale attivo.│   ├── confronto_qualita_rag.png  # Grafico confronto qualità

│   └── metriche_software_*.png    # Grafici metriche software

## Test unitari│

├── 📁 test/                        # Suite di test

Verifica moduli in `src/` senza errori logici.│   ├── unit/                      # Test unitari moduli src/

│   ├── performance/               # Test prestazionali chatbot reale

**CMD/PowerShell:**│   ├── results/                   # Risultati test + grafici PNG

```powershell│   └── run_tests.py               # Runner principale test

python test/run_tests.py --unit│

```├── 📁 documentazione/              # Guide e documentazione

│   ├── README.md                  # Questa guida! 📖

Risultati: `test/results/unit_tests_results.json`│   ├── TECHNICAL_GUIDE.md         # Guida tecnica dettagliata

│   └── README_GRAFICI.md          # Documentazione grafici tesi

**Moduli testati:**│

- `local_embeddings.py`├── 📄 main.py                      # ⭐ ENTRY POINT PRINCIPALE - ChatbotRAG ⭐

- `dividi_chunks.py`├── 📄 requirements.txt             # Lista dipendenze Python

- `ollama_llm.py`├── 📄 setup.py                     # Script setup automatico

- `prompt_templates.py`├── � start_chatbot.bat            # Avvio rapido console (Windows)

- `creazione_vectorstore.py`├── 📄 start_web.bat                # Avvio rapido web interface (Windows)

└── 📄 aggiornamento_db.bat         # Aggiorna database vettoriale (Windows)

## Test prestazionali```



Testa chatbot con 25 query in sequenza. Richiede Ollama attivo.### **📌 File Chiave da Conoscere:**



**CMD/PowerShell:**1. **`main.py`** - Il cuore del chatbot, classe `ChatbotRAG` con metodo `chat()`

```powershell2. **`interfaccia/streamlit.py`** - Interface web per utenti finali

python test/run_tests.py --performance3. **`src/ollama_llm.py`** - Comunicazione con Mistral 7B via Ollama

```4. **`src/creazione_vectorstore.py`** - Creazione e ricerca nel vector database

5. **`requirements.txt`** - Tutte le dipendenze da installare nell'ambiente virtuale

Risultati: `test/results/real_performance_results.json`6. **`test/run_tests.py`** - Esegui tutti i test del progetto



**Metriche:**---

- Tempo medio risposta

- Throughput (query/secondo)# 🧪 **ESEGUIRE I TEST**

- Percentili (P50, P95, P99)

- Tasso successoIl progetto include una suite completa di test per validare il funzionamento del sistema.



## Test completi + grafici## **⚠️ PRIMA DI ESEGUIRE I TEST:**



**CMD/PowerShell:**```bash

```powershell# 1. Attiva l'ambiente virtuale (OBBLIGATORIO!)

python test/run_tests.pychatbot_env\Scripts\activate    # Windows

python test/generate_performance_charts.pysource chatbot_env/bin/activate # Linux/Mac

```

# 2. Verifica che (chatbot_env) sia visibile nel prompt

**Grafici generati:**```

- `response_time_distribution.png`

- `performance_overview.png`## **🔬 Test Disponibili:**

- `performance_comparison.png`

- `performance_dashboard.png`### **1️⃣ Test Unitari (Validazione Moduli)**



### Visualizza risultatiVerifica che tutti i moduli in `src/` funzionino correttamente senza errori logici.



**CMD:**```bash

```cmd# ⚠️ Ambiente virtuale DEVE essere attivo!

type test\results\unit_tests_results.json

type test\results\real_performance_results.json# Esegui solo i test unitari

start test\results\performance_dashboard.pngpython test/run_tests.py --unit

```

# Output: Risultati salvati in test/results/unit_tests_results.json

**PowerShell:**```

```powershell

Get-Content test\results\unit_tests_results.json**Cosa viene testato:**

Get-Content test\results\real_performance_results.json- ✅ `local_embeddings.py` - Generazione embeddings

Invoke-Item test\results\performance_dashboard.png- ✅ `dividi_chunks.py` - Chunking testi

```- ✅ `ollama_llm.py` - Connessione LLM

- ✅ `prompt_templates.py` - Template prompt

**Linux/Mac:**- ✅ `creazione_vectorstore.py` - Database vettoriale

```bash

cat test/results/unit_tests_results.json---

cat test/results/real_performance_results.json

xdg-open test/results/performance_dashboard.png### **2️⃣ Test Prestazionali (Performance Reali)**

```

Testa il chatbot reale con 25 query in rapida sequenza, misurando tempi di risposta e throughput.

---

```bash

# RISULTATI RAGGIUNTI# ⚠️ Ambiente virtuale DEVE essere attivo!

# ⚠️ Ollama DEVE essere in esecuzione (ollama serve)

- Database: 15 FAQ + 4 PDF guide ufficiali

- Vector DB: ChromaDB con embeddings ottimizzati# Esegui solo i test prestazionali

- Testing: Sistema scientifico implementatopython test/run_tests.py --performance

- Grafici: 12 visualizzazioni professionali

- Interface: Web app Streamlit moderna# Output: Risultati salvati in test/results/real_performance_results.json

```

## Validazione

**Metriche misurate:**

- Metriche Software: WMC, LCOM, CBO, Complessità- ⏱️ Tempo medio risposta

- Metriche RAG: Context, Answer, Retrieval Relevancy- 📊 Throughput (query/secondo)

- Testing automatizzato: Framework scientifico- 📈 Percentili (P50, P95, P99)

- Ambiente completo: Virtual env con dipendenze- ✅ Tasso successo



------



# SUPPORTO### **3️⃣ Tutti i Test + Grafici**



**Studente:** Caprinali Michele  Esegui suite completa e genera grafici professionali per documentazione tesi.

**Email:** m.caprinali@studenti.unibg.it

```bash

## Risorse# ⚠️ Ambiente virtuale DEVE essere attivo!

# ⚠️ Ollama DEVE essere in esecuzione

- Guida tecnica: `documentazione/TECHNICAL_GUIDE.md`

- Guida rapida: `documentazione/QUICK_START.md`# Esegui tutti i test

- Indice: `documentazione/INDICE.md`python test/run_tests.py


# Genera grafici dai risultati
python test/generate_performance_charts.py

# Output grafici salvati in: test/results/*.png
```

**Grafici generati:**
- 📊 `response_time_distribution.png` - Distribuzione tempi risposta
- 📈 `performance_overview.png` - Overview metriche principali
- 🔍 `performance_comparison.png` - Confronto percentili
- 📉 `performance_dashboard.png` - Dashboard completa

---

### **🔍 Visualizzare Risultati Test:**

```bash
# Visualizza JSON risultati test unitari
type test\results\unit_tests_results.json       # Windows
cat test/results/unit_tests_results.json        # Linux/Mac

# Visualizza JSON risultati performance
type test\results\real_performance_results.json # Windows
cat test/results/real_performance_results.json  # Linux/Mac

# Apri grafici PNG generati
start test\results\performance_dashboard.png    # Windows
open test/results/performance_dashboard.png     # Mac
xdg-open test/results/performance_dashboard.png # Linux
```

---

# 📊 **RISULTATI RAGGIUNTI (REALI)**

## **🏆 PERFORMANCE SISTEMA:**
- ✅ **Database**: 15 FAQ + 4 PDF guide ufficiali
- ✅ **Vector DB**: ChromaDB con embeddings ottimizzati
- ✅ **Testing**: Sistema scientifico implementato
- ✅ **Grafici**: 12 visualizzazioni professionali (PNG+PDF)
- ✅ **Interface**: Web app Streamlit moderna

## **🎯 VALIDAZIONE:**
- ✅ **Metriche Software**: WMC, LCOM, CBO, Complessità
- ✅ **Metriche RAG**: Context, Answer, Retrieval Relevancy  
- ✅ **Testing Automatizzato**: Framework scientifico
- ✅ **Ambiente Completo**: Virtual env con tutte le dipendenze

---

# 🆘 **SUPPORTO**

## **📞 CONTATTI:**
- 🎓 **Studente**: Caprinali Michele  
- 📧 **Email**: m.caprinali@studenti.unibg.it
- 📚 **Documentazione**: `tesi/documentazione/`
- 🐛 **Issue**: Repository GitHub

## **📖 RISORSE:**
- **Guida Tecnica**: `tesi/documentazione/TECHNICAL_GUIDE.md`
- **Testing Report**: `tesi/testing/grafici_testing/TESTING_FINAL_REPORT.md`  
- **Grafici Tesi**: `tesi/grafici/`
