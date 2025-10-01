# Test Suite - Chatbot Segreteria Studenti

## Panoramica

Questa directory contiene una suite completa di test per validare il funzionamento, le performance e la qualità del chatbot per la segreteria studenti. I test sono organizzati in tre categorie principali:

## Struttura dei Test

```
test/
├── unit/                     # Test unitari per componenti base
│   └── test_components.py    # Test embeddings, vectorstore, text processing
├── functional/               # Test funzionali end-to-end
│   └── test_user_experience.py  # Test esperienza utente
├── performance/              # Test prestazionali
│   └── test_performance.py   # Test tempi di risposta e throughput
├── results/                  # Risultati e report
│   ├── graphs/              # Grafici generati
│   ├── *.json               # File risultati in formato JSON
│   └── consolidated_test_report.json  # Report finale
├── run_tests.py             # Script principale per eseguire i test
├── generate_visualizations.py  # Generatore grafici e report
└── README.md                # Questa documentazione
```

## Tipi di Test

### 1. Test Unitari (`unit/`)
**Obiettivo**: Verificare che i componenti base funzionino correttamente

**Componenti testati**:
- Sistema di embedding (SentenceTransformers)
- Elaborazione testi e chunking
- Connessione e ricerca nel vector database
- Funzioni di utilità

**Esempio**:
```python
# Test inizializzazione embeddings
def test_embeddings_initialization():
    embedder = LocalEmbeddings()
    return hasattr(embedder, 'model') and embedder.model is not None
```

### 2. Test Funzionali (`functional/`)
**Obiettivo**: Validare l'esperienza utente end-to-end

**Scenari testati**:
- Query informazioni generali (iscrizioni, tasse, esami)
- Flusso conversazione multi-turno
- Gestione casi limite (query vuote, testo nonsense)
- Qualità delle risposte

**Metriche valutate**:
- Lunghezza appropriata della risposta
- Presenza di termini attesi
- Struttura della risposta
- Assenza di errori evidenti

### 3. Test Prestazionali (`performance/`)
**Obiettivo**: Misurare performance e scalabilità del sistema

**Test eseguiti**:
- **Sequenziale**: 25 query in sequenza per misurare tempo medio
- **Concorrente**: 20 query parallele per testare throughput
- **Pattern di carico**: Test con diversi livelli di carico
- **Memoria**: Verifica stabilità nel tempo

**Metriche raccolte**:
- Tempo medio di risposta
- Throughput (query/secondo)
- Percentili di latenza
- Tasso di successo
- Efficienza concorrenza

## Esecuzione dei Test

### Esecuzione Completa
```bash
# Esegue tutti i test e genera visualizzazioni
python run_tests.py

# Equivalente a:
python run_tests.py all
```

### Esecuzione Specifica
```bash
# Solo test unitari
python run_tests.py unit

# Solo test funzionali  
python run_tests.py functional

# Solo test prestazionali
python run_tests.py performance

# Solo generazione grafici
python run_tests.py visualizations
```

## Risultati e Report

### File JSON Generati
- `unit_tests_results.json`: Risultati dettagliati test unitari
- `functional_tests_results.json`: Risultati test funzionali con quality score
- `performance_tests_results.json`: Metriche complete di performance
- `consolidated_test_report.json`: Report finale per la tesi

### Grafici Generati
- `test_summary_complete.png`: Panoramica generale di tutti i test
- `performance_details.png`: Analisi dettagliata delle performance

### Struttura Report JSON
```json
{
  "metadata": {
    "generated_at": "2025-01-01T12:00:00",
    "test_suite_version": "1.0"
  },
  "executive_summary": {
    "overall_success_rate": 0.95,
    "system_ready_for_production": true,
    "key_metrics": {
      "avg_response_time": 0.8,
      "max_throughput": 12.5,
      "functional_quality_avg": 85.2
    }
  },
  "recommendations": [
    "Sistema performante e pronto per deployment"
  ]
}
```

## Interpretazione Risultati

### Criteri di Successo

**Test Unitari**:
- ✅ Tutti i componenti base funzionano
- ✅ Tasso successo > 90%

**Test Funzionali**:
- ✅ Quality score medio > 70/100
- ✅ Gestione corretta casi limite
- ✅ Conversazioni multi-turno fluide

**Test Prestazionali**:
- ✅ Tempo medio risposta < 2 secondi
- ✅ Tasso successo > 95%
- ✅ Throughput > 5 QPS
- ✅ Performance stabile nel tempo

### Grading Performance
- **A**: Tempo medio < 1.0s
- **B**: Tempo medio < 2.0s  
- **C**: Tempo medio < 5.0s
- **D**: Tempo medio ≥ 5.0s

## Utilizzo per la Tesi

### Documentazione Automatica
I test generano automaticamente:
1. **Grafici**: Visualizzazioni pronte per inserimento in documenti
2. **Metriche quantitative**: Numeri precisi per tabelle e confronti
3. **Report strutturato**: Analisi completa in formato JSON

### Esempio di Utilizzo in Tesi
```
"Il sistema è stato sottoposto a test completi:
- Test unitari: 6/6 componenti validati (100%)
- Test funzionali: qualità media 85.2/100 
- Test prestazionali: tempo medio 0.8s, throughput 12.5 QPS
- Valutazione complessiva: Grado A, pronto per produzione"
```

## Dipendenze

I test sono progettati per essere il più possibile indipendenti da librerie esterne, utilizzando principalmente:
- Python standard library
- matplotlib/seaborn (solo per grafici)
- Moduli del progetto esistente

## Note Tecniche

- I test simulano componenti quando necessario per garantire esecuzione anche in ambienti limitati
- Risultati salvati in formato JSON per facile integrazione con altri strumenti
- Grafici ottimizzati per stampa e presentazioni (alta risoluzione, colori appropriati)
- Commenti in italiano per facilitare comprensione e manutenzione

## Estensioni Future

La struttura è progettata per essere facilmente estendibile:
- Aggiungere nuovi test unitari in `unit/test_components.py`
- Estendere scenari funzionali in `functional/test_user_experience.py`
- Implementare test di stress in `performance/`
- Personalizzare visualizzazioni in `generate_visualizations.py`