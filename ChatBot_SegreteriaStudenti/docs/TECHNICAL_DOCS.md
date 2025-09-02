# Documentazione Tecnica
## ChatBot RAG per Supporto Studenti UniBG


## 1. Panoramica Sistema

Sistema di chatbot basato su architettura RAG (Retrieval-Augmented Generation) per l'assistenza automatizzata agli studenti dell'Università di Bergamo.

**Caratteristiche principali:**
- Implementazione completamente locale
- Tecnologie open-source
- Dati non condivisi esternamente
---

## 2. Architettura

### 2.1 Componenti 

| Componente | Tecnologia | Funzione |
|------------|------------|----------|
| **LLM** | Mistral 7B + Ollama | Generazione risposte |
| **Embeddings** | SentenceTransformers | Vettorizzazione testi |
| **Vector DB** | ChromaDB | Ricerca semantica |
| **Interface** | Streamlit + CLI | Interazione utente |

### 2.2 Flusso Elaborazione

```
[Query Utente] 
    ↓
[Embedding Query]
    ↓
[Ricerca Similarità]
    ↓
[Selezione Top-5 Documenti]
    ↓
[Assemblaggio Contesto]
    ↓
[Generazione LLM]
    ↓
[Validazione + Routing]
    ↓
[Risposta Finale]
```

---

## 3. Implementazione

### 3.1 Struttura Progetto Aggiornata

```
ChatBot_SegreteriaStudenti/
├── 🎯 APPLICAZIONE PRINCIPALE
│   ├── main.py                    # Entry point CLI
│   ├── start_chatbot.bat         # Launcher console
│   └── start_web.bat             # Launcher web
│
├── ⚙️ SETUP E CONFIGURAZIONE
│   ├── setup_auto.bat            # Setup automatico PC nuovo
│   ├── setup.bat                 # Setup Windows standard
│   ├── setup.py                  # Setup Python avanzato
│   └── requirements.txt          # Dipendenze ottimizzate
│
├── 💻 CORE SYSTEM (src/)
│   ├── chatbot.py               # 🤖 Sistema RAG principale
│   ├── ollama_llm.py            # 🧠 LLM ottimizzato (10s medi)
│   ├── local_embeddings.py     # 🔗 SentenceTransformers
│   ├── create_vectorstore.py   # 📚 ChromaDB management
│   ├── quick_responses.py      # ⚡ Cache risposte frequenti
│   └── analytics.py            # 📊 Monitoraggio sistema
│
├── 🎨 INTERFACCE (interfaces/)
│   └── streamlit_app.py         # UI web avanzata con CSS
│
├── 📊 EVALUATION SYSTEM (evaluation/)
│   ├── rag_evaluation.py        # 🎯 Metriche RAG specializzate
│   ├── performance_benchmark.py # ⚡ Test velocità (5-25 query)
│   ├── software_metrics.py      # 📐 CC, WMC, LCOM analysis
│   └── thesis_evaluation.py     # 📋 Evaluation standard
│
├── 🧪 TESTING (tests/)
│   ├── test_retrieval.py       # 🔍 Test ricerca semantica
│   ├── test_links.py           # 🔗 Validazione URL
│   └── generate_test_data.py   # 📝 Generazione dataset
│
├── 📊 REPORT E RISULTATI (results/)
│   ├── rag_evaluation_*.{png,md,json}     # Report RAG
│   ├── performance_benchmark.json        # Dati velocità
│   └── software_metrics_*.{png,md,json}  # Analisi codice
│
├── 📚 DOCUMENTAZIONE (docs/)
│   ├── user_manual.md          # 👤 Manuale utente
│   ├── TECHNICAL_DOCS.md       # 🔧 Docs tecniche
│   ├── SETUP_GUIDE.md          # 🛠️ Setup dettagliato
│   ├── TROUBLESHOOTING.md      # 🆘 Risoluzione problemi
│   └── EVALUATION_REPORT.md    # 📊 Report evaluation
│
└── 📄 DATI E DATABASE
    ├── data/FAQ/              # 16 file argomenti UniBG
    ├── vectordb/              # ChromaDB (113 chunk)
    ├── extracted_text/        # Testi preprocessati
    └── test_dataset.json      # 100 query evaluation
```

### 3.2 Preprocessing Documenti

**Input:** 20 file (PDF/TXT) dalla documentazione UniBG
**Output:** 113 chunk semantici nel database vettoriale

**Processo:**
1. Estrazione testo automatica
2. Chunking intelligente (1000 caratteri)
3. Generazione embeddings
4. Indicizzazione in ChromaDB

### 3.2 Sistema RAG

**Modello Embedding:** all-MiniLM-L6-v2  
**Database Vettoriale:** ChromaDB  
**LLM:** Mistral 7B (4GB RAM)


### 3.3 Routing Intelligente

Il sistema identifica automaticamente query che richiedono assistenza personalizzata:

```python
# Criteri di routing al ticket system
personal_keywords = ["mio", "mia", "non riesco", "personale"]
low_confidence = ["non sono sicuro", "non posso fornire"]
short_response = len(response) < 50
```

---

## 4. Configurazione

### 4.1 Parametri Sistema

```bash
# Modelli
EMBEDDING_MODEL=all-MiniLM-L6-v2
OLLAMA_MODEL=mistral:7b

# RAG
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=5
TEMPERATURE=0.1

# Sistema
VECTORDB_PATH=vectordb
TICKET_URL=https://www.unibg.it/servizi-studenti/contatti
```

### 4.2 Requisiti Hardware

**Minimo:**
- CPU: 4 core, 2.0GHz
- RAM: 8GB
- Storage: 10GB

**Raccomandato:**
- CPU: 8+ core, 3.0GHz
- RAM: 16GB
- Storage: 20GB SSD

---

## 5. Interfacce

### 5.1 Interfaccia CLI
```bash
# Attiva ambiente virtuale
.\venv\Scripts\Activate.ps1

# Avvia chatbot
python main.py

# Alternativa automatica
.\start_chatbot.bat
```

### 5.2 Interfaccia Web
```bash
# Attiva ambiente virtuale
.\venv\Scripts\Activate.ps1

# Avvia interfaccia web
streamlit run interfaces/streamlit_app.py --server.port 8501

# Alternativa automatica
.\start_web.bat
```
- URL: http://localhost:8501

---

## 6. Performance

### 6.1 Tempi di Risposta
- **Embedding query:** < 1 secondo
- **Ricerca vettoriale:** < 0.1 secondi
- **Generazione LLM:** 40-45 secondi
- **Totale medio:** 44.29 secondi

### 6.2 Accuratezza
- **Retrieval documenti rilevanti:** > 90%
- **Routing decisioni appropriate:** 85%
- **Validazione link:** 80%

---

## 7. Deployment e Manutenzione

### 7.1 Setup Iniziale
```bash
# Setup automatico (raccomandato)
python setup.py

# Setup manuale
pip install -r requirements.txt
ollama pull mistral:7b

```

### 7.2 Operazioni Routine

**Aggiornamento documenti:**
```bash
# Attiva ambiente virtuale
.\venv\Scripts\Activate.ps1

# Aggiorna documenti
python src/extract_and_save.py
python src/create_vectorstore.py

# Alternativa automatica
.\update_database.bat
```

**Backup database:**
```bash
cp -r vectordb vectordb_backup
```

### 7.3 Risoluzione Problemi

| Problema | Soluzione |
|----------|-----------|
| Ollama non risponde | `ollama serve` |
| Modello mancante | `ollama pull mistral:7b` |
| Database corrotto | Ricreare con `create_vectorstore.py` |
| Memoria insufficiente | Ridurre `CHUNK_SIZE` |

---

## 8. Informazioni Progetto
 
**Autore:** Michele Caprinali  
**Corso:** Ingegneria Informatica  
**Università:** Università degli Studi di Bergamo

**Repository:** `ChatBot_SegreteriaStudenti/`  
**Linguaggi:** Python 3.13  
**Licenza:** Open Source