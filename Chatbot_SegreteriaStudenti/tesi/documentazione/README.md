# 🤖 **CHATBOT SEGRETERIA STUDENTI - GUIDA UTENTE**

> Sistema RAG intelligente per assistenza automatica agli studenti universitari  

## 🎯 **COSA FA QUESTO CHATBOT?**

Il chatbot risponde automaticamente alle domande più frequenti degli studenti su:
- 📝 **Iscrizioni agli esami**
- 💳 **Tasse e pagamenti**  
- 📄 **Certificati e documenti**
- 🕐 **Orari e contatti segreteria**
- 🎓 **Servizi per studenti**
- 📚 **Carriera universitaria**
- 🎯 **Orientamento e tirocini**

---

# 🚀 **GUIDA RAPIDA - INIZIA SUBITO**

## **STEP 1: PREPARAZIONE AMBIENTE**

### **1️⃣ Verifica il Progetto**
```bash
# Naviga nella cartella principale
cd Chatbot_SegreteriaStudenti

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
python main.py
```

### **🌐 Modalità Streamlit (Interface Web)**
```bash
# Avvia interface web 
streamlit run interfaccia/streamlit.py
# Apri browser su: http://localhost:8501
```

### **🔧 Test Connessione**
```bash
# Test rapido del sistema
python src/creazione_vectorstore.py
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
