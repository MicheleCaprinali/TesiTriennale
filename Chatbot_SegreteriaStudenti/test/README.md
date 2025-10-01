# Test Suite Essenziale - Chatbot Segreteria Studenti

## Panoramica

Suite di test focalizzata sui componenti fondamentali del chatbot per garantire affidabilità e performance in produzione.

## Struttura Semplificata

```
test/
├── unit/                     # Test unitari per moduli src/
│   └── test_components.py    # Test completi di tutti i moduli src/
├── performance/              # Test prestazionali chatbot reale
│   └── test_performance.py   # Test performance con 25 query reali
├── results/                  # Risultati dei test
│   ├── unit_tests_results.json
│   ├── real_performance_results.json
│   └── essential_test_execution.json
├── run_tests.py             # Script principale
└── README.md                # Questa documentazione
```

## Test Implementati

### 1. Test Unitari (`unit/test_components.py`)
**Obiettivo**: Validare che tutti i moduli in `src/` funzionino correttamente

**Moduli testati**:
- `local_embeddings.py`: Inizializzazione, embedding query e documenti
- `dividi_chunks.py`: Divisione testi in chunks appropriati
- `ollama_llm.py`: Inizializzazione classe LLM (no connessione)
- `prompt_templates.py`: Generazione prompt ottimizzati
- `creazione_vectorstore.py`: Funzioni di utility

**Esempio risultato**:
```json
{
  "local_embeddings_module": {
    "status": "PASS",
    "details": {
      "embedding_size": 384,
      "query_test": "OK",
      "documents_test": "OK"
    }
  }
}
```

### 2. Test Prestazionali (`performance/test_performance.py`)
**Obiettivo**: Misurare performance del chatbot reale con query sequenziali

**Caratteristiche**:
- **25 query realistiche** su temi universitari
- **Chatbot reale** (non simulato)
- **Metriche dettagliate**: tempo medio, mediano, percentili
- **Valutazione automatica**: A/B/C/D con raccomandazioni

**Query di esempio**:
- "Come posso iscrivermi all'università?"
- "Quali sono le scadenze per le tasse universitarie?"
- "Come prenotare un esame?"
- "Procedura per il trasferimento da altra università"

## Esecuzione

### Esecuzione Completa
```bash
# Esegue tutti i test essenziali
python run_tests.py

# Equivalente
python run_tests.py all
```

### Esecuzione Specifica
```bash
# Solo test unitari
python run_tests.py unit

# Solo test prestazionali (chatbot reale)
python run_tests.py performance
```

## Risultati

### Test Unitari
- ✅ **Tutti i moduli src/ validati**
- 📊 **Tasso successo per modulo**
- 🔍 **Dettagli su embedding, chunking, prompt**

### Test Prestazionali
- ⏱️ **Tempo medio risposta** (es: 1.2s)
- 📊 **Statistiche complete** (min, max, mediano, 95° percentile)
- 🎯 **Valutazione finale** (A-D) con raccomandazioni
- 📈 **Throughput** (query/minuto)

### Criteri di Valutazione

**Grading Performance**:
- **A**: Tempo medio < 2.0s, successo > 95%
- **B**: Tempo medio < 5.0s, successo > 90%
- **C**: Tempo medio < 10.0s, successo > 80%
- **D**: Superiore ai limiti C

**Raccomandazioni automatiche**:
- Sistema pronto produzione
- Ottimizzare tempi risposta
- Migliorare affidabilità

## Integrazione con Tesi

### Dati Quantitativi Generati
```json
{
  "summary": {
    "performance_grade": "A - Eccellente",
    "avg_response_time": 1.234,
    "success_rate_percent": 96.0,
    "recommendation": "Sistema pronto per produzione"
  }
}
```

### Utilizzo per Documentazione
- **Tabelle performance**: Metriche precise per confronti
- **Grafici**: Dati strutturati per visualizzazioni
- **Validazione tecnica**: Prova che tutti i componenti funzionano

## Note Tecniche

### Dipendenze Minime
- Solo componenti del progetto esistente
- Nessuna libreria esterna aggiuntiva
- Test robusti e autocontenuti

### Design Pragmatico
- **Test unitari**: Rapidi, focalizzati sui blocchi base
- **Test prestazionali**: Realistici, con chatbot effettivo
- **Risultati strutturati**: JSON per facile analisi

### Estensibilità
- Facile aggiungere nuove query di test
- Modifica soglie di valutazione
- Personalizzazione metriche

## Esempi Output

### Console
```
⚡ TEST PRESTAZIONALI CHATBOT REALE
📈 Query totali: 25
✅ Query riuscite: 24
⏱️ Tempo medio risposta: 1.234s
🎯 VALUTAZIONE FINALE
   Voto: A - Eccellente
   Pronto produzione: ✅ SÌ
```

### JSON Results
Dati strutturati salvati automaticamente per:
- Analisi successive
- Confronti temporali
- Documentazione tesi
- Report automatici