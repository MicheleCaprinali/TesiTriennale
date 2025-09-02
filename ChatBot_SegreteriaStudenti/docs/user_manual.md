# MANUALE UTENTE - ChatBot UniBG

## 🎯 INTRODUZIONE

Questo ChatBot RAG (Retrieval-Augmented Generation) fornisce assistenza automatizzata agli studenti dell'Università di Bergamo utilizzando tecnologie completamente gratuite e locali.

**Stack tecnologico:**
- **Mistral 7B** (tramite Ollama) - Modello di linguaggio
- **SentenceTransformers** - Embedding semantici  
- **ChromaDB** - Database vettoriale
- **Streamlit** - Interfaccia web
- **Python 3.9+** - Linguaggio di programmazione

## 🚀 INSTALLAZIONE PC NUOVO

### Prerequisiti Obbligatori

**1. Installa Python 3.9+**
- Vai su: https://www.python.org/downloads/
- Scarica versione 3.9 o superiore
- **CRITICO**: Seleziona "Add Python to PATH"
- Riavvia terminale dopo installazione

**2. Installa Ollama**  
- Vai su: https://ollama.ai
- Scarica per Windows e installa
- Riavvia terminale

### Setup Automatico

1. **Scompatta** il progetto in una cartella
2. **Apri PowerShell/CMD** nella cartella  
3. **Esegui:**
   ```cmd
   setup_auto.bat
   ```
4. **Segui** le istruzioni a schermo
5. **Attendi** il completamento (5-10 minuti)

## 💻 UTILIZZO

### Avvio Console
```cmd
start_chatbot.bat
```

### Avvio Web  
```cmd
start_web.bat
```
Poi vai su: http://localhost:8501

### Comandi di Manutenzione
```cmd
run_tests.bat        # Test sistema
update_database.bat  # Aggiorna dati
setup.bat           # Re-setup se problemi
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

