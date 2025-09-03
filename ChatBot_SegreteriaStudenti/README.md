# ChatBot Segreteria Studenti UniBG

Sistema intelligente per l'assistenza automatizzata agli studenti dell'Università di Bergamo.  
**Tesi Triennale - Ingegneria Informatica - A.A. 2024/2025**

## Stack Tecnologico

| Componente | Tecnologia | Versione |
|------------|------------|----------|
| **LLM** | Mistral 7B (Ollama) | Latest |
| **Embeddings** | SentenceTransformers | all-MiniLM-L6-v2 |
| **Vector DB** | ChromaDB | 0.5.0+ |
| **Framework** | LangChain | 0.3.x |
| **UI** | Streamlit + CLI | 1.38+ |

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
4. **Il setup installerà tutto automaticamente:**
   - Ambiente virtuale Python
   - Tutte le dipendenze
   - Modello Mistral 7B
   - Database vettoriale

### 🖥️ **Avvio Sistema**

#### Interfaccia Console (CLI)
```cmd
start_chatbot.bat
```

#### Interfaccia Web
```cmd
start_web.bat
```
Poi vai su: http://localhost:8501

### Manutenzione
```cmd
update_database.bat  # Aggiorna vectorstore
run_tests.bat        # Test sistema completo
```

## 📁 Struttura Progetto

```
ChatBot_SegreteriaStudenti/
├── README.md                 # 📖 Guida principale
├── setup_auto.bat           # 🚀 Setup automatico PC nuovo
├── setup.bat                # ⚙️ Setup standard
├── setup.py                 # 🐍 Setup avanzato Python
├── start_chatbot.bat        # 💬 Avvio CLI
├── start_web.bat           # 🌐 Avvio web interface
├── run_tests.bat           # 🧪 Test sistema completo
├── main.py                 # 🎯 Applicazione principale CLI
├── requirements.txt        # 📦 Dipendenze Python
├── test_dataset.json      # 📊 Dataset test evaluation
│
├── data/                   # 📄 Documenti UniBG
│   ├── FAQ/               # ❓ File FAQ (16 argomenti)
│   └── student_guide/     # 📚 Guide studenti
│
├── src/                   # 💻 Codice sorgente
│   ├── chatbot.py        # 🤖 Sistema RAG principale
│   ├── ollama_llm.py     # 🧠 Interfaccia LLM ottimizzata
│   ├── local_embeddings.py # 🔗 Gestione embedding
│   ├── create_vectorstore.py # 📚 Database vettoriale
│   ├── quick_responses.py # ⚡ Risposte rapide
│   └── analytics.py      # 📈 Analytics sistema
│
├── interfaces/            # 🖥️ Interfacce utente
│   └── streamlit_app.py  # 🎨 UI web avanzata
│
├── evaluation/           # 📊 Sistema evaluation
│   ├── rag_evaluation.py        # 🎯 Evaluation RAG avanzata
│   ├── performance_benchmark.py # ⚡ Benchmark velocità
│   ├── software_metrics.py      # 📐 Metriche codice
│   └── thesis_evaluation.py     # 📋 Evaluation tesi
│
├── tests/                # 🧪 Test automatici
│   ├── test_retrieval.py # 🔍 Test ricerca
│   ├── test_links.py     # 🔗 Validazione link
│   └── generate_test_data.py # 📝 Generazione dati test
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