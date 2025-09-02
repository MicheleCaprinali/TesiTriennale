# 🎓 ChatBot RAG - Segreteria Studenti UniBG

Sistema di Question Answering automatico per assistenza studenti universitari basato su tecnologia RAG (Retrieval-Augmented Generation).

## 🚀 **Setup Rapido per PC Pulito**

### **📋 Prerequisiti**
- **Python 3.8+** ([Download qui](https://www.python.org/downloads/))
- **Git** (opzionale, per clonare il repository)
- **10GB spazio libero** (per modelli AI)
- **Connessione internet** (per download iniziale modelli)

### **⚡ Installazione Automatica**

1. **Scarica il progetto** e scompattalo in una cartella
2. **Apri PowerShell/CMD** nella cartella del progetto
3. **Esegui setup automatico**:
   ```cmd
   setup.bat
   ```
4. **Segui le istruzioni** del setup guidato

Il setup installerà automaticamente:
- ✅ Ambiente virtuale Python
- ✅ Tutte le dipendenze Python
- ✅ Guida installazione Ollama
- ✅ Download modello Mistral 7B
- ✅ Configurazione environment

### **🔧 Setup Manuale (se automatico fallisce)**

1. **Crea ambiente virtuale**:
   ```cmd
   python -m venv venv
   call venv\Scripts\activate.bat
   ```

2. **Installa dipendenze**:
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Installa Ollama**:
   - Vai su [ollama.ai](https://ollama.ai)
   - Scarica e installa Ollama per Windows
   - Apri nuovo terminale e installa Mistral:
     ```cmd
     ollama pull mistral:7b
     ```

4. **Configura environment**:
   ```cmd
   copy .env.example .env
   ```

## 🏃‍♂️ **Avvio Sistema**

### **💬 Interfaccia Console**
```cmd
start_chatbot.bat
```

### **🌐 Interfaccia Web**
```cmd
start_web.bat
```
- Apri browser su: http://localhost:8501

### **🔄 Aggiorna Database Documenti**
```cmd
update_database.bat
```

### **🧪 Esegui Test**
```cmd
run_tests.bat
```

## 📁 **Struttura Progetto**

```
ChatBot_SegreteriaStudenti/
├── 📁 src/                    # Codice sorgente principale
├── 📁 data/                   # Documenti PDF da processare
├── 📁 interfaces/             # Interfacce utente (Streamlit)
├── 📁 tests/                  # Test automatici
├── 📁 vectordb/               # Database vettoriale (auto-generato)
├── 📁 extracted_text/         # Testi estratti (auto-generato)
├── 📄 requirements.txt        # Dipendenze Python
├── 📄 .env                   # Configurazione (da creare)
└── 📄 setup.bat              # Setup automatico
```

## ⚙️ **Configurazione Avanzata**

### **Modifica Configurazioni**
Edita il file `.env` per personalizzare:
- Modello di embedding
- Parametri di chunking
- Temperatura del LLM
- URL Ollama

### **Aggiungi Nuovi Documenti**
1. Copia file PDF in `data/FAQ/` o `data/student_guide/`
2. Esegui `update_database.bat`
3. I documenti saranno automaticamente processati

## 🔧 **Risoluzione Problemi**

### **❌ "Python non trovato"**
- Installa Python da python.org
- Durante installazione, seleziona "Add Python to PATH"
- Riavvia terminale

### **❌ "Ollama non risponde"**
- Verifica che Ollama sia in esecuzione
- Riavvia Ollama: chiudi e riapri l'applicazione
- Verifica modello: `ollama list`

### **❌ "ChromaDB/Sentence Transformers errore"**
- Problema compilazione C++: installa [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Oppure usa Conda invece di pip

### **❌ "Streamlit non si avvia"**
- Verifica porta 8501 libera
- Controlla firewall/antivirus
- Prova porta diversa: `streamlit run interfaces/streamlit_app.py --server.port 8502`

### **⚠️ Performance lente**
- Assicurati di avere almeno 8GB RAM
- Chiudi applicazioni non necessarie
- Il primo avvio è più lento (download modelli)

## 📊 **Funzionalità Sistema**

- 🤖 **LLM Locale**: Mistral 7B via Ollama (completamente offline)
- 🔍 **Embedding Locali**: SentenceTransformers (nessun API key)
- 💾 **Vector Store**: ChromaDB per ricerca semantica
- 📄 **Elaborazione PDF**: Estrazione automatica testo
- 🌐 **Multi-interfaccia**: Console + Web Streamlit
- 📈 **Analytics**: Metriche performance e qualità
- 🧪 **Testing**: Suite test automatici

## 🔒 **Privacy e Sicurezza**

- ✅ **100% Locale**: Nessun dato inviato a servizi esterni
- ✅ **Offline**: Funziona senza connessione internet (dopo setup)
- ✅ **Open Source**: Codice completamente ispezionabile
- ✅ **GDPR Compliant**: Dati rimangono sul device locale

## 📚 **Documentazione Tecnica**

- **Architettura**: Sistema RAG con pipeline ETL
- **Modelli AI**: 
  - Embedding: all-MiniLM-L6-v2 (384 dim)
  - LLM: Mistral 7B (quantized)
- **Stack Tecnologico**: Python + PyTorch + ChromaDB + Streamlit
- **Performance**: ~2-5s per risposta su hardware moderno

## 🎯 **Contatti e Supporto**

- **Tesi**: Ingegneria Informatica - Università di Bergamo
- **Documentazione**: Consulta `technical_docs.md`
- **Issues**: Controlla `guide_files_bat.md` per troubleshooting

---

**💡 Suggerimento**: Per la prima installazione, assicurati di avere una buona connessione internet per il download dei modelli AI (~4-6GB totali).
