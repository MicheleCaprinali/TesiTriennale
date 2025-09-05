# ChatBot Segreteria Studenti UniBG

Sistema intelligente RAG per l'assistenza automatizzata agli studenti dell'Università di Bergamo.  
**Tesi Triennale - Ingegneria Informatica - A.A. 2024/2025**

## Stack Tecnologico

| Componente | Tecnologia | Versione | Note |
|------------|------------|----------|------|
| **LLM** | Mistral 7B (Ollama) | Latest | Ottimizzato per velocità |
| **Embeddings** | SentenceTransformers | all-MiniLM-L6-v2 | Embedding locali |
| **Vector DB** | ChromaDB | 0.5.0+ | Database ottimizzato |
| **Text Splitting** | LangChain | 0.3.x | Chunking intelligente |
| **UI** | Streamlit | 1.38+ | Interfaccia web moderna |
| **Processing** | PyPDF2 + Custom | Latest | Link extraction avanzata |

## 📊 **Architettura Database**

### **Dataset Ottimizzato (Settembre 2025)**
- **FAQ Files**: 16 file (.txt) - ~50KB totali
- **PDF Enhanced**: 4 guide principali - ~352KB totali
  - `futuri_studenti_enhanced.txt` - 128KB
  - `laureati_enhanced.txt` - 132KB  
  - `studenti_enhanced.txt` - 64KB
  - `guide_2025-2026_enhanced.txt` - 26KB
- **Vector Database**: ChromaDB ottimizzato per velocità
- **Chunking**: Intelligente con preservazione link

## 🚀 Setup per PC Nuovo (Zero Install)

### ⚠️ **PREREQUISITI OBBLIGATORI**

**1. Installa Python 3.9+ PRIMA DI TUTTO:**
- Vai su [python.org/downloads](https://www.python.org/downloads/)
- Scarica Python 3.9 o superiore  
- **CRITICO**: Durante l'installazione seleziona "Add Python to PATH"
- Riavvia il terminale dopo l'installazione
- Verifica: `python --version`

**2. Installa Ollama:**
- Vai su [ollama.ai](https://ollama.ai) 
- Scarica e installa Ollama per Windows
- Riavvia il terminale
- Verifica: `ollama --version`

## 🚀 Setup per PC Nuovo (Zero Install)

### ⚠️ **PREREQUISITI OBBLIGATORI**

**1. Installa Python 3.9+ PRIMA DI TUTTO:**
- Vai su [python.org/downloads](https://www.python.org/downloads/)
- Scarica Python 3.9 o superiore  
- **CRITICO**: Durante l'installazione seleziona "Add Python to PATH"
- Riavvia il terminale dopo l'installazione
- Verifica: `python --version`

**2. Installa Ollama:**
- Vai su [ollama.ai](https://ollama.ai) 
- Scarica e installa Ollama per Windows
- Riavvia il terminale
- Verifica: `ollama --version`

### 🎯 **Installazione Automatica**

1. **Scarica e scompatta** il progetto in una cartella
2. **Apri PowerShell/CMD** nella cartella del progetto
3. **Esegui setup automatico:**
   ```cmd
   setup.bat
   ```
4. **Il setup installerà automaticamente:**
   - Ambiente virtuale Python
   - Tutte le dipendenze (ChromaDB, Streamlit, PyPDF2, etc.)
   - Modello Mistral 7B (scaricamento automatico)
   - Database vettoriale ottimizzato

### 🖥️ **Avvio Sistema**

#### Interfaccia Web (Consigliata)
```cmd
start_web.bat
```
→ Vai su: **http://localhost:8501**
- Interfaccia moderna nero/azzurro
- Chat interattiva con link cliccabili
- Esempi di domande nella sidebar

#### Interfaccia Console (CLI)
```cmd
start_chatbot.bat
```

### 🔧 **Manutenzione**
```cmd
update_database.bat  # Rigenera vectorstore ottimizzato
run_tests.bat        # Test completo sistema + performance
```

## 📁 Struttura Progetto

```
ChatBot_SegreteriaStudenti/
├── README.md                 # 📖 Guida principale
├── TECHNICAL_DOCS.md         # � Documentazione tecnica
├── user_manual.md            # 👨‍🎓 Manuale utente
├── setup.bat                 # ⚙️ Setup automatico
├── start_chatbot.bat         # 💬 Avvio CLI
├── start_web.bat            # 🌐 Avvio interfaccia web
├── update_database.bat      # 🔄 Aggiornamento database
├── run_tests.bat           # 🧪 Test completo sistema
├── main.py                 # 🎯 Applicazione CLI principale
├── requirements.txt        # 📦 Dipendenze Python
├── test_dataset.json      # 📊 Dataset valutazione
│
├── data/                   # 📄 Documenti sorgente
│   ├── FAQ/               # ❓ File FAQ (16 argomenti)
│   └── student_guide/     # 📚 Guide PDF originali
│
├── extracted_text/        # 📝 Testi elaborati
│   ├── *_enhanced.txt    # ✨ PDF ottimizzati (4 file, ~352KB)
│   └── *_extract.txt     # 📄 Estratti FAQ elaborati
│
├── src/                   # 💻 Codice sorgente
│   ├── __init__.py      
│   ├── chatbot.py        # 🤖 Sistema RAG principale
│   ├── ollama_llm.py     # 🧠 LLM interface ottimizzata
│   ├── local_embeddings.py # 🎯 Embedding locali
│   ├── create_vectorstore.py # 🗄️ Gestione database vettoriale
│   ├── enhanced_link_extractor.py # 🔗 Estrazione link avanzata
│   ├── split_into_chunks.py # ✂️ Chunking intelligente
│   ├── extract_file.py   # 📑 Estrazione testo
│   ├── quick_responses.py # ⚡ Risposte rapide
│   └── analytics.py      # 📊 Metriche e analisi
│
├── interfaces/           # 🖥️ Interfacce utente  
│   └── streamlit_app.py # 🎨 Interfaccia web moderna
│
├── vectordb/            # 🗄️ Database vettoriale ChromaDB
├── evaluation/          # 📈 Sistema valutazione
├── results/            # 📊 Risultati test e metriche
└── thesis/            # 📚 Documentazione tesi
```

---

## 🔄 **Aggiornamenti Recenti (Settembre 2025)**

### ✅ **Ottimizzazioni Performance**
- **Database ridotto del 60%**: da ~1MB a ~402KB totali
- **Ricerca accelerata**: k=2 invece di k=8 per query rapide
- **Timeout ottimizzati**: 30s invece di 60s per risposta
- **LLM parameters**: num_predict=150 per velocità massima

### ✅ **Interfaccia Migliorata**
- **Design moderno**: Palette nero/azzurro UniBG
- **Link funzionali**: Sistema di validazione intelligente
- **UX ottimizzata**: Esempi nella sidebar, layout pulito
- **Rimossa complessità**: Solo modalità HTML, no scelte multiple

### ✅ **Sistema RAG Potenziato**
- **Ricerca ibrida**: Semantica + keyword per termini critici
- **Validazione link**: Controllo punteggiatura e matching intelligente  
- **Fallback system**: Risposte alternative se timeout LLM
- **PDF processing avanzato**: Link extraction migliorata

### ✅ **Pulizia Codebase**
- **File obsoleti rimossi**: `fix_links.py`, `process_all_pdfs_enhanced.py`
- **Architettura semplificata**: Focus sui componenti essenziali
- **Documentazione aggiornata**: README, TECHNICAL_DOCS, user_manual

### � **Metriche Attuali**
- **Tempo risposta medio**: 15-25 secondi
- **Database size**: 352KB (PDF) + 50KB (FAQ) = ~402KB
- **Accuracy**: ~85% per domande standard UniBG
- **Link validity**: ~95% grazie al sistema di validazione
│
├── results/              # 📊 Report e risultati
│   ├── rag_evaluation_advanced.png # Grafici evaluation
│   ├── rag_evaluation_report.md    # Report dettagliato
│   ├── performance_benchmark.json  # Dati benchmark
│   └── software_metrics_*.{png,md,json} # Analisi codice
│
├── vectordb/             # 🗃️ Database vettoriale ChromaDB
├── extracted_text/       # 📄 Testi estratti preprocessing
├── venv/                 # 🐍 Ambiente virtuale Python
│
└── docs/                 # 📚 Documentazione
    ├── user_manual.md        # 👤 Manuale utente
    ├── TECHNICAL_DOCS.md     # 🔧 Documentazione tecnica
    ├── SETUP_GUIDE.md        # 🛠️ Guida setup dettagliata
    ├── TROUBLESHOOTING.md    # 🆘 Risoluzione problemi
    └── EVALUATION_REPORT.md  # 📊 Report evaluation finale
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

## 📚 Documentazione Completa

| Documento | Descrizione | Link |
|-----------|-------------|------|
| 👤 **Manuale Utente** | Guida utilizzo completa | [docs/user_manual.md](docs/user_manual.md) |
| 🔧 **Docs Tecniche** | Architettura e implementazione | [docs/TECHNICAL_DOCS.md](docs/TECHNICAL_DOCS.md) |
| 🛠️ **Setup Guide** | Installazione dettagliata | [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) |
| 🆘 **Troubleshooting** | Risoluzione problemi | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| 📊 **Evaluation Report** | Performance e metriche | [docs/EVALUATION_REPORT.md](docs/EVALUATION_REPORT.md) |

## Risoluzione problemi

| Problema | Soluzione |
|----------|-----------|
| Ollama non risponde | `ollama serve` |
| Modello mancante | `ollama pull mistral:7b` |
| Memoria insufficiente | Chiudi altre applicazioni |
| Database corrotto | `python src/create_vectorstore.py` |
| Errori dipendenze | `pip install -r requirements.txt --force-reinstall` |

## Specifiche Tecniche

**Requisiti minimi:**
- **Python 3.9+ (OBBLIGATORIO - da installare per primo)**
- 8GB RAM
- 10GB storage libero

---

**Autore:** Michele Caprinali  
**Università:** Università degli Studi di Bergamo  
**Corso:** Ingegneria Informatica  
**Anno Accademico:** 2024/2025