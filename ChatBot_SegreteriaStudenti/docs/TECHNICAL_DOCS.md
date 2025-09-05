# Documentazione Tecnica
## ChatBot RAG per Supporto Studenti UniBG
**Versione aggiornata - Settembre 2025**

## 1. Panoramica Sistema

Sistema di chatbot basato su architettura RAG (Retrieval-Augmented Generation) ottimizzato per l'assistenza automatizzata agli studenti dell'Università di Bergamo.

**Caratteristiche principali:**
- Implementazione completamente locale e gratuita
- Tecnologie open-source ottimizzate per velocità
- Dati non condivisi esternamente (privacy completa)
- Database ottimizzato (352KB vs ~1MB originale)
- Ricerca ibrida semantica + keyword
- Sistema di validazione link intelligente
---

## 2. Architettura Ottimizzata

### 2.1 Stack Tecnologico 

| Componente | Tecnologia | Versione | Ottimizzazioni |
|------------|------------|----------|----------------|
| **LLM** | Mistral 7B + Ollama | Latest | Timeout 30s, num_predict 150 |
| **Embeddings** | SentenceTransformers | all-MiniLM-L6-v2 | Modello lightweight locale |
| **Vector DB** | ChromaDB | 0.5.0+ | k=2 per ricerca rapida |
| **Text Splitting** | LangChain | 0.3.x | Chunking intelligente |
| **Interface** | Streamlit | 1.38+ | UI nero/azzurro, link cliccabili |
| **PDF Processing** | PyPDF2 + Custom | Latest | Link extraction avanzata |

### 2.2 Flusso Elaborazione Ibrido

```
[Query Utente] 
    ↓
[Ricerca Rapida k=2] → [Embedding Query] → [Ricerca Semantica ChromaDB]
    ↓                                              ↓
[Keyword Search] ←------ [Termini Critici] ← [Controllo Termini]
    ↓
[Merge Risultati (max 3 documenti)]
    ↓
[Assemblaggio Contesto Ottimizzato]
    ↓
[Generazione LLM (30s timeout)]
    ↓
[Validazione Link Intelligente]
    ↓
[Risposta Finale + Fallback]
```

---

## 3. Database Ottimizzato

### 3.1 Composizione Dataset

**📊 Dimensioni Finali (Settembre 2025):**
```
SORGENTI DATI:
├── 📄 FAQ (16 file)                    ~50KB
│   ├── ✅ contatti_utili_*             # Contatti specifici
│   ├── ✅ messaggi_importanti          # Avvisi aggiornati  
│   ├── ✅ servizio_disabilità_dsa      # Servizi accessibilità
│   ├── ✅ tirocini                     # Info pratiche stage
│   ├── ✅ varie                        # Info uniche
│   └── ...11 altri file essenziali
│
└── 📚 PDF Enhanced (4 guide)          ~352KB
    ├── futuri_studenti_enhanced.txt    128KB (↓ da ~200KB)
    ├── laureati_enhanced.txt           132KB (↓ da ~180KB)  
    ├── studenti_enhanced.txt            64KB (↓ da ~150KB)
    └── guide_2025-2026_enhanced.txt     26KB (↓ da ~40KB)

TOTALE DATASET: ~402KB (vs ~1MB originale)
COMPRESSIONE: ~60% riduzione dimensioni
```

### 3.2 Ottimizzazioni Applicate

**🧹 Pulizia Contenuti:**
- Rimossi header/footer ripetitivi
- Eliminati menu navigazione ridondanti  
- Puliti link decorativi non funzionali
- Mantenuti solo link contestuali essenziali

**⚡ Ottimizzazioni Velocità:**
- k=2 nella ricerca vettoriale (vs k=8 originale)
- max 3 documenti nel contesto (vs 10+ originale)
- Timeout LLM: 30s (vs 60s originale)
- num_predict: 150 (vs 400 originale)

### 3.3 Struttura Progetti

```
ChatBot_SegreteriaStudenti/
├── 🎯 CORE SYSTEM
│   ├── main.py                    # Entry point CLI
│   ├── start_chatbot.bat         # Launcher console  
│   ├── start_web.bat             # Launcher web ottimizzato
│   └── update_database.bat       # Regen DB veloce
│
├── 💻 ENGINE (src/)
│   ├── chatbot.py               # 🤖 RAG ibrido (2-step search)
│   ├── ollama_llm.py            # 🧠 LLM ottimizzato velocità
│   ├── enhanced_link_extractor.py # 🔗 Link processing avanzato
│   ├── create_vectorstore.py   # 📚 ChromaDB ottimizzato
│   ├── local_embeddings.py     # 🎯 SentenceTransformers
│   └── quick_responses.py      # ⚡ Cache risposte frequenti
│
├── 🎨 UI (interfaces/)
│   └── streamlit_app.py         # Interface nero/azzurro moderna
│
├── 📊 DATA (ottimizzati)
│   ├── data/FAQ/               # FAQ essenziali (50KB)
│   ├── extracted_text/         # PDF enhanced (352KB)  
│   └── vectordb/              # ChromaDB ottimizzato
│
├── 🧪 EVALUATION & TESTING
│   ├── evaluation/            # Sistema valutazione completo
│   ├── tests/                # Test funzionali
│   └── results/             # Report e metriche
│
└── 📚 DOCS
    ├── README.md              # Setup e usage
    ├── TECHNICAL_DOCS.md      # Architettura (questo file)
    └── user_manual.md         # Guida utente
```
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