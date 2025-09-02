# RAG SYSTEM EVALUATION REPORT

**Data Evaluation**: 2025-09-02T11:12:28.266435
**Queries Testate**: 25

## 🚀 PERFORMANCE METRICS

| Metrica | Valore | Benchmark |
|---------|--------|-----------|
| Tempo Medio Risposta | 30.74s | < 10s (Ottimo) |
| Tempo Mediano | 33.80s | < 5s (Ottimo) |
| Tasso Successo | 4.0% | > 90% (Ottimo) |
| Tasso Timeout | 96.0% | < 10% (Ottimo) |

## 📝 QUALITÀ RISPOSTE

| Metrica | Score | Descrizione |
|---------|-------|-------------|
| Specificità | 0.11 | Presenza info specifiche (link, numeri, date) |
| Completezza | 0.69 | Lunghezza appropriata della risposta |
| Chiarezza | 0.76 | Assenza errori e ridirection inutili |
| Lunghezza Media | 19.0 parole | 20-100 parole ottimale |

## 🎯 ROUTING ACCURACY

| Metrica | Valore |
|---------|--------|
| Accuratezza Routing | 64.0% |

## 📊 RETRIEVAL QUALITY

## 🎖️ CLASSIFICAZIONE PERFORMANCE

**Valutazione Complessiva**: ❌ DA MIGLIORARE

## 💡 RACCOMANDAZIONI

- ⚡ **Ottimizzare Performance**: Ridurre timeout LLM e parametri generazione
- 🔧 **Migliorare Stabilità**: Gestire meglio timeout e errori
- 📝 **Migliorare Prompt**: Ottimizzare istruzioni per LLM
- 🎯 **Calibrare Routing**: Migliorare logica di redirection
