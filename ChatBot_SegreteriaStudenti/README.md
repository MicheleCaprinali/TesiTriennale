# ChatBot Segreteria Studenti UniBG

Sistema intelligente per l'assistenza automatizzata agli studenti dell'Università di Bergamo.  
**Tesi Triennale - Ingegneria Informatica - A.A. 2024/2025**

## Stack Tecnologico

| Componente | Tecnologia | Versione |
|------------|------------|----------|
| **LLM** | Mistral 7B (Ollama) | Latest |
| **Embeddings** | SentenceTransformers | all-MiniLM-L6-v2 |
| **Vector DB** | ChromaDB | 0.4.0+ |
| **UI** | Streamlit + CLI | 1.25+ |
| **Python** | CPython | 3.8+ |

## Setup Rapido

### ⚡ Windows (Automatico - Raccomandato)
```cmd
setup.bat          # Setup completo guidato (include controllo prerequisiti)
start_chatbot.bat   # Avvio interfaccia CLI
start_web.bat       # Avvio interfaccia web (http://localhost:8501)
```

### 🔧 Setup Manuale (se automatico fallisce)
1. **Prerequisiti:**
   - Python 3.8+ ([Download](https://www.python.org/downloads/))
   - Git (opzionale)
   
2. **Ambiente virtuale:**
   ```cmd
   python -m venv venv
   call venv\Scripts\activate.bat
   pip install --upgrade pip wheel setuptools
   ```

3. **Dipendenze:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Installa Ollama:** 
   - Vai su [ollama.ai](https://ollama.ai)
   - Scarica e installa per Windows
   - Installa modello: `ollama pull mistral:7b`

5. **Configurazione:**
   ```cmd
   copy .env.example .env
   ```

## Utilizzo

### 💬 Interfaccia CLI
```cmd
# Metodo raccomandato (automatico)
start_chatbot.bat

# Metodo manuale
call venv\Scripts\activate.bat
python main.py
```

### 🌐 Interfaccia Web
```cmd
# Metodo raccomandato (automatico)
start_web.bat
# Browser: http://localhost:8501

# Metodo manuale
call venv\Scripts\activate.bat
streamlit run interfaces/streamlit_app.py --server.port 8501
```

### 🔄 Manutenzione
```cmd
update_database.bat  # Aggiorna vectorstore con nuovi documenti
run_tests.bat        # Esegui test sistema completo
```

### 📁 Aggiungere Nuovi Documenti
1. Copia i file PDF in `data/FAQ/` o `data/student_guide/`
2. Esegui `update_database.bat`
3. I documenti saranno automaticamente processati e indicizzati

## Struttura Progetto

```
ChatBot_SegreteriaStudenti/
├── 📄 main.py                 # Applicazione principale CLI
├── 📄 setup.bat              # Setup automatico Windows (★ NUOVO)
├── 📄 start_chatbot.bat      # Avvio CLI rapido
├── 📄 start_web.bat          # Avvio interfaccia web
├── 📄 run_tests.bat          # Test sistema completo
├── 📄 update_database.bat    # Aggiorna database documenti
├── 📄 requirements.txt       # Dipendenze Python (★ AGGIORNATO)
├── 📄 .env                   # Configurazione (auto-creato da setup)
├── 📄 .env.example           # Template configurazione
├── 📄 SETUP_GUIDE.md         # Guida dettagliata installazione
├── 📁 data/                  # Documenti UniBG (PDF originali)
│   ├── FAQ/                  # FAQ e documenti informativi
│   └── student_guide/        # Guide per studenti
├── 📁 vectordb/              # Database vettoriale (auto-generato)
├── 📁 extracted_text/        # Testi estratti dai PDF (auto-generato)
├── 📁 src/                   # Codice sorgente principale
│   ├── chatbot.py           # Sistema RAG core
│   ├── ollama_llm.py        # Interfaccia Ollama
│   ├── local_embeddings.py  # Gestione SentenceTransformers
│   ├── create_vectorstore.py # Gestione ChromaDB
│   └── extract_and_save.py  # Elaborazione documenti
├── 📁 interfaces/            # Interfacce utente
│   └── streamlit_app.py     # Web UI Streamlit
├── 📁 tests/                 # Suite di test
├── 📁 evaluation/            # Metriche e valutazione performance
└── 📁 results/              # Report e analisi generate
```

## Architettura RAG

```
[Query Utente] → [Embedding] → [Ricerca Vettoriale] → [Selezione Top-5] 
    ↓
[Assemblaggio Contesto] → [Mistral 7B] → [Validazione] → [Risposta/Ticket]
```

## Esempi Query

**Supportate dal sistema:**
- "Come iscriversi agli esami?"
- "Scadenze pagamento tasse universitarie?"
- "Documenti necessari per la laurea?"
- "Servizi per studenti con disabilità?"
- "Informazioni sui tirocini?"

**Routing automatico a ticket:**
- Domande personali specifiche
- Richieste di documenti individuali
- Problematiche non documentate

## Risoluzione problemi

### 🚨 Problemi Comuni e Soluzioni

| Problema | Soluzione |
|----------|-----------|
| ❌ Python non trovato | Installa da [python.org](https://python.org), seleziona "Add to PATH" |
| ❌ Setup.bat fallisce | Esegui come amministratore, verifica connessione internet |
| ❌ Ollama non risponde | Verifica installazione: `ollama --version`, riavvia Ollama |
| ❌ Modello mancante | `ollama pull mistral:7b` |
| ❌ Memoria insufficiente | Chiudi app non necessarie, min 8GB RAM |
| ❌ ChromaDB errore | Installa [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) |
| ❌ Porta 8501 occupata | Usa `streamlit run interfaces/streamlit_app.py --server.port 8502` |
| ❌ Database corrotto | Esegui `update_database.bat` per ricreare |
| ❌ Dipendenze mancanti | `pip install -r requirements.txt --force-reinstall` |

### 📞 Supporto Avanzato
- **Setup dettagliato**: Consulta `SETUP_GUIDE.md`
- **Troubleshooting**: Consulta `guide_files_bat.md`
- **Documentazione tecnica**: Consulta `technical_docs.md`

## Specifiche Tecniche

**Requisiti minimi:**
- Python 3.8+ (raccomandato 3.10+)
- 8GB RAM (raccomandato 16GB)
- 10GB storage libero
- Connessione internet (solo per setup iniziale)

**Architettura Sistema:**
- 🤖 **LLM**: Mistral 7B quantized (4-bit)
- 🔢 **Embeddings**: all-MiniLM-L6-v2 (384 dimensioni)
- 💾 **Vector Store**: ChromaDB con persistenza locale
- 🌐 **Interfacce**: CLI nativa + Streamlit web
- 📊 **Analytics**: Metriche real-time e valutazione qualità

**Performance:**
- Risposta media: 2-5 secondi
- Embedding: ~100ms per query
- Retrieval: Top-5 in ~50ms
- Generazione: 1-3s (dipende da lunghezza)

---

**👨‍💻 Autore:** Michele Caprinali  
**🏫 Università:** Università degli Studi di Bergamo  
**📚 Corso:** Ingegneria Informatica  
**📅 Anno Accademico:** 2024/2025  
**🎯 Tesi:** Sistema RAG per Assistenza Studenti Universitari