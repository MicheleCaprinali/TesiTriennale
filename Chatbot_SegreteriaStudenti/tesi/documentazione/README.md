# 📋 tesi/documentazione/README.md

# 🤖 **CHATBOT SEGRETERIA STUDENTI - GUIDA UTENTE**

> Sistema intelligente per assistenza automatica agli studenti universitari  
> Tesi Triennale - Caprinali Michele

## 🎯 **COSA FA QUESTO CHATBOT?**

Il chatbot risponde automaticamente alle domande più frequenti degli studenti su:
- 📝 **Iscrizioni agli esami**
- 💳 **Tasse e pagamenti**  
- 📄 **Certificati e documenti**
- 🕐 **Orari e contatti segreteria**
- 🎓 **Servizi per studenti**
- 📚 **Carriera universitaria**
- 🎯 **Orientamento e tirocini**

**Esempi di domande:**
- *"Come mi iscrivo all'esame di Analisi?"*
- *"Quando devo pagare le tasse?"*
- *"Come richiedo il certificato di iscrizione?"*

---

# 🚀 **GUIDA RAPIDA - INIZIA SUBITO**

## **STEP 1: PREPARAZIONE AMBIENTE**

### **1️⃣ Verifica il Progetto**
```bash
# Naviga nella cartella principale
cd Chatbot_SegreteriaStudenti

# Verifica struttura progetto
dir  # Windows
ls   # Linux/Mac
```

### **2️⃣ Attiva Ambiente Virtuale (GIÀ ESISTENTE)**
```bash
# L'ambiente virtuale è già configurato in chatbot_env/
# Windows
chatbot_env\Scripts\activate

# Linux/Mac  
source chatbot_env/bin/activate
```

### **3️⃣ Verifica Installazione**
```bash
# Controlla che tutto sia installato
python -c "import chromadb, ollama; print('Dipendenze OK')"
```

## **STEP 2: AVVIA IL CHATBOT**

### **🖥️ Modalità Console (Sistema Principale)**
```bash
# Avvia il chatbot principale
python src/ollama_llm.py
```

### **🌐 Modalità Streamlit (Interface Web)**
```bash
# Avvia interface web moderna
streamlit run interfaccia/streamlit.py
# Apri browser su: http://localhost:8501
```

### **🔧 Test Connessione**
```bash
# Test rapido del sistema
python src/creazione_vectorstore.py
```

---

# 💬 **COME USARE IL CHATBOT**

## **🎯 DOMANDE DI ESEMPIO PER CATEGORIA:**

### **📝 ISCRIZIONI E LEZIONI:**
```
"Come posso iscrivermi all'esame di Matematica?"
"Qual è la scadenza per l'iscrizione agli esami?"
"Come funziona l'iscrizione agli appelli?"
"Dove trovo il calendario degli esami?"
```

### **💳 TASSE E PAGAMENTI:**
```
"Quando devo pagare le tasse universitarie?"
"Quali sono i metodi di pagamento accettati?"
"Come richiedo la riduzione delle tasse?"
"Dove trovo la mia situazione tasse?"
```

### **📄 ATTESTATI E DOCUMENTI:**
```
"Come richiedo il certificato di iscrizione?"
"Quanto tempo ci vuole per il diploma di laurea?"
"Come ottengo la pergamena di laurea?"
"Posso richiedere duplicati di documenti?"
```

### **🎓 CARRIERA E SERVIZI:**
```
"Come accedo ai servizi per studenti disabili?"
"Dove trovo informazioni sui tirocini?"
"Come funziona il servizio orientamento?"
"Come richiedo il riconoscimento crediti?"
```

### **🕐 CONTATTI E INFORMAZIONI:**
```
"Quali sono gli orari della segreteria?"
"Come contatto la segreteria per urgenze?"
"Dove trovo i contatti dell'università?"
"Come accedo al sito web UniBG?"
```

---

# 🛠️ **RISOLUZIONE PROBLEMI**

## **❌ PROBLEMI COMUNI:**

### **🐍 Ambiente virtuale non attivo?**
```bash
# Verifica se l'ambiente è attivo
# Il prompt dovrebbe mostrare (chatbot_env)

# Se non attivo, attivalo:
# Windows
chatbot_env\Scripts\activate

# Linux/Mac
source chatbot_env/bin/activate
```

### **📦 Errore importazione moduli?**
```bash
# Verifica installazioni nel venv
pip list | grep chroma
pip list | grep ollama

# Se mancano, reinstalla
pip install chromadb ollama
```

### **🤖 Ollama non risponde?**
```bash
# Installa Ollama se non presente
# Windows: https://ollama.ai/download
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# Mac: brew install ollama

# Avvia servizio
ollama serve

# Scarica modello (in terminale separato)
ollama pull llama2
```

### **💾 Errori database vectoriale?**
```bash
# Il database vettoriale è in vectordb/
# Se corrotto, elimina e ricrea
rm -rf vectordb/  # Linux/Mac
rmdir /s vectordb  # Windows

# Ricrea database
python src/creazione_vectorstore.py
```

### **📁 File mancanti?**
```bash
# Verifica presenza cartelle principali
ls data/FAQ/                    # Dati FAQ
ls data/guida_dello_studente/   # Guide PDF
ls vectordb/                    # Database vettoriale
ls src/                         # Codice sorgente
```

---

# 🧪 **TESTING E VALIDAZIONE**

## **🔬 TEST AUTOMATICO COMPLETO**
```bash
# Assicurati che l'ambiente sia attivo
chatbot_env\Scripts\activate  # Windows
source chatbot_env/bin/activate  # Linux/Mac

# Esegui test scientifico
cd tesi/testing
python test_scientifico.py
```

## **📊 GENERA GRAFICI TESI**
```bash
# Grafici principali per tesi
cd tesi
python generazione_grafici.py

# Grafici risultati testing  
cd tesi/testing
python grafici_testing_results.py
```

## **📈 VISUALIZZA RISULTATI**
```bash
# I grafici sono salvati in:
ls tesi/grafici/           # 8 grafici principali
ls tesi/testing/grafici_testing/  # 4 grafici testing

# Tutti disponibili in formato PNG e PDF
```

---

# 📁 **STRUTTURA REALE PROGETTO**

```
📂 Chatbot_SegreteriaStudenti/
├── 📁 src/                         # Codice sorgente principale
│   ├── ollama_llm.py              # Engine LLM principale ⭐
│   ├── creazione_vectorstore.py   # Setup database vettoriale
│   ├── link_enhancer.py           # Sistema link automatici
│   ├── prompt_templates.py        # Template per prompt
│   ├── local_embeddings.py        # Gestione embeddings
│   ├── dividi_chunks.py           # Chunking documenti
│   └── testi_estratti.py          # Estrazione testi PDF
├── 📁 interfaccia/                 # Interface utente
│   └── streamlit.py               # Web interface moderna ⭐
├── 📁 data/                        # Database conoscenza
│   ├── FAQ/                       # 15 file FAQ categorizzati
│   ├── guida_dello_studente/      # 4 PDF guide ufficiali
│   └── testi_estratti/            # Testi estratti da PDF
├── 📁 vectordb/                    # Database vettoriale ChromaDB
│   ├── chroma.sqlite3             # DB principale
│   └── d55e47f0.../              # Embeddings vettoriali
├── 📁 evaluation/                  # Sistema valutazione
│   ├── metriche_avanzate.py       # Metriche RAG
│   ├── metriche_qualità.py        # Qualità risposte
│   └── metriche_software.py       # Metriche software
├── 📁 results/                     # Risultati testing
│   ├── test_results.json          # Risultati base
│   ├── advanced_metrics_report.json # Metriche avanzate
│   └── native_software_metrics.json # Metriche software
├── 📁 tesi/                        # Materiali tesi
│   ├── grafici/                   # 8 grafici tesi (PNG+PDF) ⭐
│   ├── testing/                   # Sistema testing scientifico
│   │   ├── test_scientifico.py    # Engine testing
│   │   ├── grafici_testing_results.py # Grafici testing
│   │   └── grafici_testing/       # 4 grafici output (PNG+PDF)
│   ├── generazione_grafici.py     # Generator grafici principale
│   └── documentazione/            # Guide utente
└── 📁 chatbot_env/                 # Ambiente virtuale configurato ⭐
    ├── Scripts/                   # Eseguibili Python
    ├── Lib/site-packages/        # Tutti i pacchetti installati
    └── pyvenv.cfg                # Configurazione ambiente
```

---

# 🎓 **DIPENDENZE REALI INSTALLATE**

## **📦 PACCHETTI PRINCIPALI (già installati in chatbot_env):**
```
🤖 chromadb==1.0.20           # Database vettoriale
🤖 ollama                     # LLM interface  
📊 streamlit                  # Web interface
🧮 matplotlib                 # Grafici
🧮 seaborn                    # Visualizzazioni
📈 plotly==5.x                # Grafici interattivi
🔢 numpy                      # Calcoli numerici
🐼 pandas                     # Data manipulation
📊 scipy                      # Statistiche
🧠 transformers               # NLP models
🎯 altair==5.5.0              # Visualizzazioni
⚡ uvicorn                    # Server ASGI
🎨 colorama                   # Output colorato
```

---

# 💬 **MODALITÀ DI UTILIZZO**

## **🖥️ MODALITÀ 1: Console Interattiva**
```bash
# Attiva ambiente
chatbot_env\Scripts\activate

# Avvia chatbot
python src/ollama_llm.py

# Interagisci direttamente
```

## **🌐 MODALITÀ 2: Web Interface (CONSIGLIATA)**
```bash
# Attiva ambiente  
chatbot_env\Scripts\activate

# Avvia interface web
streamlit run interfaccia/streamlit.py

# Apri browser: http://localhost:8501
# Interface moderna e user-friendly
```

## **🔧 MODALITÀ 3: Testing Scientifico**
```bash
# Per sviluppatori e valutatori
cd tesi/testing
python test_scientifico.py

# Output: accuracy, grafici, report
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

# 🎉 **INIZIA ORA!**

## **🚀 QUICK START:**
```bash
# 1. Naviga nel progetto
cd Chatbot_SegreteriaStudenti

# 2. Attiva ambiente (già configurato)
chatbot_env\Scripts\activate

# 3. Avvia interface web moderna
streamlit run interfaccia/streamlit.py

# 4. Apri browser su localhost:8501

# 5. Fai la tua prima domanda!
"Ciao, come mi iscrivo agli esami?"
```

## **📱 OPPURE MODALITÀ CONSOLE:**
```bash
# Modalità console diretta
python src/ollama_llm.py
```

**Il sistema è già completo e funzionante! 🤖✨**

---

# 🆘 **SUPPORTO**

## **📞 CONTATTI:**
- 🎓 **Studente**: Caprinali Michele  
- 📧 **Email**: [inserire email]
- 📚 **Documentazione**: `tesi/documentazione/`
- 🐛 **Issue**: Repository GitHub

## **📖 RISORSE:**
- **Guida Tecnica**: `tesi/documentazione/TECHNICAL_GUIDE.md`
- **Testing Report**: `tesi/testing/grafici_testing/TESTING_FINAL_REPORT.md`  
- **Grafici Tesi**: `tesi/grafici/` (8 grafici professionali)

**Buon utilizzo del chatbot UniBG! 🎓🤖**