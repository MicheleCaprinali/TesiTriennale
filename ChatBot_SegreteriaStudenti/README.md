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
| **UI** | Streamlit + CLI | 1.28+ |

## Setup Rapido

### Windows (Automatico)
```bash
setup.bat          # Installazione completa
start_chatbot.bat   # Avvio interfaccia CLI
start_web.bat       # Avvio interfaccia web (http://localhost:8501)
```

### Setup Manuale
1. **Installa Ollama:** [Download](https://ollama.ai/download)
2. **Dipendenze Python:** `pip install -r requirements.txt`
3. **Modello LLM:** `ollama pull mistral:7b`
4. **Attiva ambiente virtuale:** `.\venv\Scripts\Activate.ps1` (Windows)
5. **Avvio:** `python main.py`

## Utilizzo

### Interfaccia CLI
```bash
# Attiva ambiente virtuale (importante!)
.\venv\Scripts\Activate.ps1

# Avvia chatbot
python main.py

# Alternativa: usa file .bat automatico
.\start_chatbot.bat
```

### Interfaccia Web
```bash
# Attiva ambiente virtuale
.\venv\Scripts\Activate.ps1

# Avvia interfaccia web
streamlit run interfaces/streamlit_app.py --server.port 8501

# Alternativa: usa file .bat automatico
.\start_web.bat
# Browser: http://localhost:8501
```

### Manutenzione
```bash
update_database.bat  # Aggiorna vectorstore
run_tests.bat        # Esegui test sistema
```

## Struttura Progetto

```
ChatBot_SegreteriaStudenti/
├── main.py                    # Applicazione principale CLI
├── setup.bat                  # Setup automatico Windows
├── start_chatbot.bat         # Avvio CLI
├── start_web.bat             # Avvio web interface
├── run_tests.bat             # Test sistema
├── update_database.bat       # Aggiorna database
├── requirements.txt          # Dipendenze Python
├── data/                     # Documenti UniBG (20 file)
├── vectordb/                 # Database vettoriale (113 chunk)
├── src/                      # Codice sorgente
│   ├── chatbot.py           # Sistema RAG principale
│   ├── ollama_llm.py        # Interfaccia LLM
│   └── create_vectorstore.py # Gestione embeddings
├── interfaces/               # UI Streamlit
├── tests/                    # Test suite
└── evaluation/              # Metriche performance
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

| Problema | Soluzione |
|----------|-----------|
| Ollama non risponde | `ollama serve` |
| Modello mancante | `ollama pull mistral:7b` |
| Memoria insufficiente | Chiudi altre applicazioni |
| Database corrotto | `python src/create_vectorstore.py` |
| Errori dipendenze | `pip install -r requirements.txt --force-reinstall` |

## Specifiche Tecniche

**Requisiti minimi:**
- Python 3.13+
- 8GB RAM
- 10GB storage libero

---

**Autore:** Michele Caprinali  
**Università:** Università degli Studi di Bergamo  
**Corso:** Ingegneria Informatica  
**Anno Accademico:** 2024/2025