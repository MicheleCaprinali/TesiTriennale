# 📊 GRAFICI TESI TRIENNALE - CHATBOT SEGRETERIA STUDENTI

## 📋 INFORMAZIONI PROGETTO
- **Titolo**: Sistema RAG per Assistenza Studenti - Università di Bergamo
- **Tecnologie**: Python 3.13, Mistral 7B (Ollama), ChromaDB, SentenceTransformers, Streamlit
- **Architettura**: RAG (Retrieval-Augmented Generation) + Link Enhancement System
- **Dati utilizzati**: con dati reali del progetto (JSON results + source analysis)
- **Data ultima verifica**: 16/09/2025 22:12
- **Performance finale**: 75.7% accuracy (sistema ottimizzato)

## 📁 STRUTTURA CARTELLE:
```
tesi/
├── generazione_grafici.py      # Script generazione ✅
├── grafici/                    # Grafici generati ✅
│   ├── performance_overview.png/pdf
│   ├── category_improvement.png/pdf  
│   ├── link_enhancement.png/pdf
│   ├── software_quality.png/pdf
│   ├── cyclomatic_complexity.png/pdf    ⭐ CON FILE REALI
│   ├── rag_metrics.png/pdf
│   ├── overall_assessment.png/pdf
│   └── comparative_analysis.png/pdf
└── documentazione/             # Docs complete ✅
    ├── README_GRAFICI.md       # Questo file
    └── screenshots/
```

## 📈 GRAFICI GENERATI (8 totali):

### 🚀 **1. PERFORMANCE OVERVIEW** 
- **File**: `performance_overview.png/pdf`
- **Contenuto**: Confronto Baseline (63.3%) vs Sistema Ottimizzato (75.7%)
- **Risultato**: Miglioramento performance +19.6% (statisticamente significativo)
- **Utilizzo**: Capitolo Risultati - dimostrazione efficacia ottimizzazioni

### 📊 **2. CATEGORY IMPROVEMENT**
- **File**: `category_improvement.png/pdf` 
- **Contenuto**: Performance per categoria (Iscrizioni 72.5%, Tasse 81.9%, Orari 76.9%, etc.)
- **Risultato**: Miglioramenti consistenti su tutte le categorie di domande UniBG
- **Utilizzo**: Analisi dettagliata performance per dominio specifico

### 🔗 **3. LINK ENHANCEMENT** 
- **File**: `link_enhancement.png/pdf`
- **Contenuto**: Sistema arricchimento automatico risposte (2.1 → 5.4 link/risposta)
- **Risultato**: Incremento 157% link utili, valore aggiunto significativo
- **Utilizzo**: Dimostrazione innovazione sistema RAG ottimizzato

### 🏗️ **4. SOFTWARE QUALITY**
- **File**: `software_quality.png/pdf`
- **Contenuto**: Metriche ingegneria software (complessità, manutenibilità, accoppiamento)
- **Risultato**: Qualità "A - Eccellente" secondo standard accademici
- **Utilizzo**: Validazione metodologia sviluppo e best practices

### 🔄 **5. CYCLOMATIC COMPLEXITY** ⭐
- **File**: `cyclomatic_complexity.png/pdf`
- **Contenuto**: Analisi complessità ciclomatica FILE REALI (main.py, ollama_llm.py, etc.)
- **File analizzati**: Tutti i moduli src/ + interfaccia + evaluation
- **Risultato**: Complessità media <10 (soglia accettabile), codice mantenibile
- **Utilizzo**: Dimostrazione qualità implementazione per commissione

### 🤖 **6. RAG METRICS**
- **File**: `rag_metrics.png/pdf`
- **Contenuto**: Context Relevance, Semantic Similarity, Answer Quality specifiche RAG
- **Risultato**: Sistema RAG performante (0.53-0.70 similarity score)
- **Utilizzo**: Validazione tecnica approccio Retrieval-Augmented Generation

### 🏆 **7. OVERALL ASSESSMENT**
- **File**: `overall_assessment.png/pdf`
- **Contenuto**: Valutazione finale multi-dimensionale (software + RAG + UX)
- **Risultato**: Progetto "A - Eccellente" con score 8.5/10 complessivo
- **Utilizzo**: Sintesi conclusioni tesi e assessment qualitativo

### 📈 **8. COMPARATIVE ANALYSIS**
- **File**: `comparative_analysis.png/pdf`
- **Contenuto**: Confronto evoluzione performance e posizionamento vs alternative
- **Risultato**: Ottimo rapporto performance/complessità per progetto accademico
- **Utilizzo**: Contestualizzazione risultati e posizionamento scientifico

## 💾 FORMATI DISPONIBILI:
- **PNG**: Alta risoluzione (300 DPI) per stampa tesi e presentazioni
- **PDF**: Formato vettoriale scalabile per inclusione in documenti LaTeX

## 🎓 UTILIZZO IN TESI:

### **Capitolo 3 - Metodologia e Approccio RAG**:
- comparative_analysis.png (posizionamento metodologico)
- rag_metrics.png (validazione approccio tecnico)

### **Capitolo 4 - Implementazione e Architettura**:
- software_quality.png (qualità ingegneristica)
- cyclomatic_complexity.png (analisi complessità implementazione)

### **Capitolo 5 - Sistema RAG e Ottimizzazioni**:
- link_enhancement.png (innovazioni sistema)
- performance_overview.png (efficacia ottimizzazioni)

### **Capitolo 6 - Valutazione e Testing**:
- category_improvement.png (performance dettagliata per dominio)
- overall_assessment.png (assessment multi-dimensionale)

### **Capitolo 7 - Conclusioni e Risultati**:
- performance_overview.png (risultato principale: 75.7%)
- comparative_analysis.png (contributo scientifico)

## ⚡ RIGENERAZIONE GRAFICI:
```bash
# Dalla cartella tesi/
python generazione_grafici.py

# Verifica output generati
dir grafici\*.png
dir grafici\*.pdf
```

## 🔧 REQUISITI SISTEMA:
- Python 3.9+ con matplotlib, pandas, numpy
- Accesso ai file results/*.json del progetto
- Spazio disco: ~50MB per tutti i grafici

## 🏆 **STATO PROGETTO: COMPLETATO CON SUCCESSO!**

### ✅ **8 GRAFICI PROFESSIONALI GENERATI E VERIFICATI**
- ✅ Performance Overview: 75.7% vs 63.3% baseline  
- ✅ Category Analysis: Performance dettagliata per dominio UniBG
- ✅ Link Enhancement: +157% incremento utilità risposte
- ✅ Software Quality: Score "A - Eccellente" 
- ✅ Cyclomatic Complexity: Analisi FILE REALI <10 complessità
- ✅ RAG Metrics: Validazione tecnica retrieval-augmented generation
- ✅ Overall Assessment: Score finale 8.5/10
- ✅ Comparative Analysis: Posizionamento scientifico

### 📊 **FORMATI PNG E PDF ALTA RISOLUZIONE**
### 🎓 **PRONTO PER TESI TRIENNALE E PRESENTAZIONE**
### ⭐ **INCLUDE ANALISI SU CODICE REALE DEL PROGETTO**
### 🔬 **METODOLOGIA SCIENTIFICA CON DATI VERIFICABILI**
        