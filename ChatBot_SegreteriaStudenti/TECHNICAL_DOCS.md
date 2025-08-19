# Documentazione Tecnica
## ChatBot RAG per Supporto Studenti UniBG


## 1. Panoramica Sistema

Sistema di chatbot basato su architettura RAG (Retrieval-Augmented Generation) per l'assistenza automatizzata agli studenti dell'Università di Bergamo.

**Caratteristiche principali:**
- Implementazione completamente locale (zero costi API)
- Tecnologie open-source
- Privacy-first (dati non condivisi esternamente)
- Supporto multimodale (CLI + Web)

---

## 2. Architettura

### 2.1 Componenti Core

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

### 3.1 Preprocessing Documenti

**Input:** 20 file (PDF/TXT) dalla documentazione UniBG
**Output:** 113 chunk semantici nel database vettoriale

**Processo:**
1. Estrazione testo automatica
2. Chunking intelligente (1000 caratteri, overlap 200)
3. Generazione embeddings (384 dimensioni)
4. Indicizzazione in ChromaDB

### 3.2 Sistema RAG

**Modello Embedding:** all-MiniLM-L6-v2
- Dimensioni vettore: 384
- Performance: ~100 doc/sec
- Esecuzione: Locale su CPU

**Database Vettoriale:** ChromaDB
- Indice: HNSW
- Storage: ~2GB
- Capacità: 113 documenti

**LLM:** Mistral 7B
- Memoria richiesta: 4GB RAM
- Deployment: Ollama locale
- Contesto massimo: 8192 token

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
python main.py
```
- Sessione interattiva
- Debug mode disponibile
- Help contestuale

### 5.2 Interfaccia Web
```bash
streamlit run interfaces/streamlit_app.py --server.port 8501
```
- URL: http://localhost:8501
- Design responsivo
- Tema scuro UniBG

### 5.3 API Programmatica
```python
from src.chatbot import setup_chatbot

chatbot = setup_chatbot()
result = chatbot.chat("Orari segreteria?")

# Output:
{
    'response': str,           # Risposta generata
    'redirect_to_ticket': bool, # Necessita assistenza umana
    'confidence_score': float, # Livello confidenza
    'processing_time': float   # Tempo elaborazione
}
```

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

### 6.3 Utilizzo Risorse
- **RAM durante funzionamento:** 6-8GB
- **CPU durante inferenza:** 70-90%
- **Storage database:** 2GB

---

## 7. Deployment e Manutenzione

### 7.1 Setup Iniziale
```bash
# Installazione dipendenze
pip install -r requirements.txt

# Setup Ollama
ollama pull mistral:7b

# Inizializzazione sistema
python main.py
```

### 7.2 Operazioni Routine

**Aggiornamento documenti:**
```bash
python src/extract_and_save.py
python src/create_vectorstore.py
```

**Backup database:**
```bash
cp -r vectordb vectordb_backup
```

**Health check:**
```bash
python tests/test_retrieval.py
```

### 7.3 Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| Ollama non risponde | `ollama serve` |
| Modello mancante | `ollama pull mistral:7b` |
| Database corrotto | Ricreare con `create_vectorstore.py` |
| Memoria insufficiente | Ridurre `CHUNK_SIZE` |

---

## 8. Sicurezza e Privacy

### 8.1 Privacy
- Elaborazione completamente locale
- Nessuna trasmissione dati esterni
- Query utenti non loggate permanentemente
- Compliance GDPR by design

### 8.2 Controllo Accessi
- Permessi filesystem per database
- Validazione input utente
- Sanitizzazione output risposte

---

## 9. Estensioni Future

### 9.1 Miglioramenti Pianificati
- Supporto file aggiuntivi (DOCX, HTML)
- Integrazione API REST
- Interfaccia mobile
- Sistema di feedback utenti

### 9.2 Scalabilità
- Deployment Docker
- Load balancing per multiple istanze
- Database distribuito
- Cache intelligente risposte

---

## 10. Informazioni Progetto

**Versione:** 1.0.0  
**Data:** Agosto 2025  
**Autore:** Michele Caprinali  
**Corso:** Ingegneria Informatica  
**Università:** Università degli Studi di Bergamo

**Repository:** `ChatBot_SegreteriaStudenti/`  
**Linguaggi:** Python 3.13+  
**Licenza:** Open Source