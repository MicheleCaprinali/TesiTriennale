# MANUALE UTENTE - ChatBot UniBG

## INTRODUZIONE

Questo documento fornisce le istruzioni per l'utilizzo del sistema ChatBot RAG (Retrieval-Augmented Generation) per l'assistenza agli studenti dell'Università di Bergamo.

Il sistema utilizza tecnologie completamente gratuite e locali:
- Mistral 7B tramite Ollama (LLM)
- SentenceTransformers (embeddings)
- ChromaDB (database vettoriale)
- Streamlit (interfaccia web)

## AVVIO RAPIDO

### Setup Iniziale

Per iniziare, navigare nella cartella del progetto e attivare l'ambiente virtuale:

```powershell
cd "TesiTriennale2025\ChatBot_SegreteriaStudenti"
venv\Scripts\Activate.ps1
```

### Verifica Prerequisiti

Verificare che Ollama sia installato e il modello Mistral disponibile:

```powershell
ollama --version
ollama list
```

Se Mistral non è presente, installarlo con:

```powershell
ollama pull mistral:7b
```

### Avvio del Sistema

#### Interfaccia Console (CLI)
```powershell
python main.py
```

#### Interfaccia Web
```powershell
streamlit run interfaces\streamlit_app.py --server.port 8501
```

L'interfaccia web sarà disponibile su: http://localhost:8501

## UTILIZZO DEL CHATBOT

### Interfaccia Console

Una volta avviato con `python main.py`, il sistema presenta un prompt interattivo:

```
Studente > [inserire domanda]
```

Esempi di domande:
- "Quali sono gli orari della segreteria?"
- "Come mi iscrivo agli esami?"
- "Dove trovo informazioni sulle tasse?"

Per uscire, digitare `exit`.

### Interfaccia Web

L'interfaccia Streamlit fornisce:
- Campo di input per le domande
- Visualizzazione delle risposte
- Cronologia delle conversazioni
- Indicatori di stato del sistema

## COMANDI AVANZATI

### Test e Valutazione

#### Test del Sistema di Retrieval
```powershell
python tests\test_retrieval.py
```

#### Generazione Metriche per Tesi
```powershell
python evaluation\thesis_evaluation.py
python evaluation\software_metrics.py
```

#### Creazione Dataset di Test
```powershell
python tests\generate_test_data.py
```

### Manutenzione Database

#### Aggiornamento Documenti
Se si modificano i documenti sorgente in `data/`, ricreare il database:

```powershell
python src\extract_and_save.py
python src\create_vectorstore.py
```

#### Verifica Database
```powershell
python -c "import chromadb; client = chromadb.PersistentClient(path='vectordb'); print(f'Documenti: {client.get_collection(\"unibg_docs\").count()}')"
```

## CONFIGURAZIONE

### Variabili Ambiente

Il file `.env.example` contiene le configurazioni di default:

- `EMBEDDING_MODEL`: Modello per gli embeddings (default: all-MiniLM-L6-v2)
- `OLLAMA_MODEL`: Modello LLM (default: mistral:7b)
- `CHUNK_SIZE`: Dimensione chunk documenti (default: 1000)
- `RETRIEVAL_K`: Numero documenti recuperati (default: 5)
- `TEMPERATURE`: Creatività del modello (default: 0.1)

### Personalizzazione

Per modificare il comportamento del sistema:

1. **Performance**: Modificare `RETRIEVAL_K` e `TEMPERATURE` in `.env`
2. **Modelli**: Cambiare `EMBEDDING_MODEL` o `OLLAMA_MODEL`
3. **Chunking**: Aggiustare `CHUNK_SIZE` e `CHUNK_OVERLAP`

## DIAGNOSTICA

### Verifica Sistema

Test rapido dello stato del sistema:

```powershell
python -c "
from src.chatbot import setup_chatbot
chatbot = setup_chatbot()
if chatbot:
    print('Sistema operativo')
    result = chatbot.chat('Test')
    print(f'Risposta: {result['response'][:50]}...')
else:
    print('Sistema non pronto')
"
```

### Controllo Componenti

Verifica individuale dei componenti:

```powershell
# Embeddings
python -c "from src.local_embeddings import LocalEmbeddings; LocalEmbeddings()"

# LLM
python -c "from src.ollama_llm import OllamaLLM; llm = OllamaLLM(); print('OK' if llm.is_running() else 'Errore')"

# Database
python -c "from src.create_vectorstore import search_vectorstore; print(len(search_vectorstore('test')['documents'][0]))"
```

## RISOLUZIONE PROBLEMI

### Problemi Comuni

1. **Ollama non risponde**
   - Verificare che sia in esecuzione: `ollama serve`
   - Controllare la porta: http://localhost:11434

2. **Modello Mistral non trovato**
   - Installare: `ollama pull mistral:7b`
   - Verificare: `ollama list`

3. **Database vettoriale vuoto**
   - Ricreare: `python src\create_vectorstore.py`
   - Verificare documenti in `extracted_text/`

4. **Errori di import**
   - Attivare ambiente virtuale: `venv\Scripts\Activate.ps1`
   - Reinstallare dipendenze: `pip install -r requirements.txt`

### Log e Debug

Per informazioni dettagliate durante l'esecuzione:

```powershell
$env:DEBUG="true"
python main.py
```

## FILE DI AUTOMAZIONE

Il progetto include file batch per automatizzare le operazioni comuni:

- `setup.bat`: Setup completo dell'ambiente
- `start_chatbot.bat`: Avvio interfaccia console
- `start_web.bat`: Avvio interfaccia web
- `run_tests.bat`: Esecuzione di tutti i test
- `update_database.bat`: Aggiornamento database

