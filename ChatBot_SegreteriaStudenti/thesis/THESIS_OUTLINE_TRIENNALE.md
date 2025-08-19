# 📚 STRUTTURA TESI TRIENNALE: "Sviluppo di un ChatBot RAG per il Supporto agli Studenti Universitari"

## 🎯 **OUTLINE OTTIMIZZATA (50-60 pagine)**

### **CAPITOLO 1: INTRODUZIONE** *(6-8 pagine)*
#### 1.1 Motivazione e Contesto *(2-3 pagine)*
- Problematiche attuali servizi universitari: code, orari limitati, ripetitività
- Opportunità AI conversazionale nel settore educativo
- Focus su soluzioni gratuite per università pubbliche

#### 1.2 Obiettivi della Tesi *(1-2 pagine)*
- **Obiettivo Principale**: Chatbot RAG completamente gratuito per studenti UniBG
- **Obiettivi Specifici**: 
  - Implementare architettura RAG locale (no API keys)
  - Sistema routing intelligente query personali
  - Valutazione performance e usabilità

#### 1.3 Contributi e Struttura *(1 pagina)*
- Prima implementazione RAG per UniBG con tecnologie free
- Framework replicabile per altre università italiane

---

### **CAPITOLO 2: BACKGROUND TECNOLOGICO** *(8-10 pagine)*
#### 2.1 Retrieval-Augmented Generation *(3-4 pagine)*
- Principi fondamentali RAG vs LLM puri
- Architettura: Retrieval + Generation pipeline
- Vantaggi per domini specifici (documenti universitari)

#### 2.2 Tecnologie Utilizzate *(3-4 pagine)*
##### 2.2.1 Large Language Models Locali
- Ollama + Mistral 7B: deployment locale vs cloud
- Quantizzazione e ottimizzazione risorse

##### 2.2.2 Sentence Embeddings e Vector Search
- SentenceTransformers: all-MiniLM-L6-v2
- ChromaDB per semantic search

#### 2.3 Chatbot Universitari: Stato dell'Arte *(2 pagine)*
- Casi studio: ASU, Georgia State University
- Gap identificati: costi, privacy, personalizzazione

---

### **CAPITOLO 3: PROGETTAZIONE E IMPLEMENTAZIONE** *(15-18 pagine)*
#### 3.1 Analisi Requisiti *(2-3 pagine)*
##### Requisiti Funzionali:
- RF1: Rispondere FAQ studenti con accuratezza >80%
- RF2: Routing automatico per query personali
- RF3: Interfacce multiple (CLI + Web)

##### Requisiti Non Funzionali:
- RNF1: Zero dipendenze da API commerciali
- RNF2: Deployment completamente locale
- RNF3: Tempo risposta accettabile (<10s)

#### 3.2 Architettura del Sistema *(3-4 pagine)*
```
[Documenti UniBG] → [Preprocessing] → [Embeddings] → [ChromaDB]
                                                          ↓
[Query Studente] → [Embedding] → [Semantic Search] → [LLM] → [Risposta]
```

**Componenti Principali:**
- **Document Processor**: Estrazione da PDF/TXT
- **Embedding Service**: SentenceTransformers locale
- **Vector Store**: ChromaDB persistente
- **Language Model**: Ollama + Mistral 7B
- **Routing Logic**: Classificazione query personali

#### 3.3 Implementazione *(6-8 pagine)*
##### 3.3.1 Preprocessing Documenti
```python
# Statistiche implementazione:
# - 20 documenti UniBG processati
# - 113 chunks generati (avg 400 token)
# - Metadata per categorizzazione
```

##### 3.3.2 Sistema RAG
- Configurazione embeddings: 384-dim vectors
- Retrieval strategy: top-k=5, cosine similarity
- Prompt engineering per contesto universitario

##### 3.3.3 Interfacce Utente
- **CLI**: Interfaccia command-line per test/debug
- **Web**: Streamlit con UI responsive e colori UniBG

##### 3.3.4 Sistema di Routing Intelligente
```python
# Logic per query personali:
personal_keywords = ["mio", "mia", "non riesco", "personale"]
# Redirect automatico a sistema ticketing
```

#### 3.4 Scelte Tecnologiche *(2 pagine)*
| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| LLM | Mistral 7B | Gratuito, multilingue, buone performance |
| Embeddings | all-MiniLM-L6-v2 | Veloce, accurato, dimensione contenuta |
| Vector DB | ChromaDB | Locale, semplice, persistente |
| Framework | LangChain | Ecosistema maturo, documentazione |

---

### **CAPITOLO 4: VALUTAZIONE SPERIMENTALE** *(12-15 pagine)*
#### 4.1 Metodologia *(2-3 pagine)*
##### 4.1.1 Dataset di Test
- 100 query realistiche generate
- Categorizzazione: esami, tasse, certificati, servizi, contatti
- Ground truth per redirect classification

##### 4.1.2 Metriche di Valutazione
- **Performance**: Tempo di risposta, throughput
- **Accuratezza**: Redirect classification accuracy  
- **Qualità**: Rilevanza risposte, completezza
- **Usabilità**: User study con studenti UniBG

#### 4.2 Setup Sperimentale *(1-2 pagine)*
- **Hardware**: [Specs del tuo PC]
- **Software**: Python 3.13, Windows 11, Ollama
- **Configurazione**: Mistral 7B quantizzato Q4_0

#### 4.3 Risultati Performance *(3-4 pagine)*
##### Test Automatizzati (30 query):
- **Tempo medio risposta**: 44.29s ± 20s
- **Accuratezza routing**: 80.0%
- **Completezza risposte**: 60 token medi
- **Tasso successo**: 90% query risolte

##### Analisi Performance:
- **Bottleneck identificato**: Caricamento ripetuto modelli
- **Variabilità**: 16-65s range (da ottimizzare)
- **Resource usage**: ~4GB RAM durante inferenza

#### 4.4 User Study *(3-4 pagine)*
##### Partecipanti:
- 15-20 studenti UniBG (diversi anni/corsi)
- Metodologia: task-based evaluation + questionario

##### Risultati Usabilità:
- **SUS Score**: [Target >70]
- **Soddisfazione globale**: [1-5 Likert]
- **Preferenza vs contatto umano**: [Percentuale]

##### Feedback Qualitativo:
- **Punti di forza**: Velocità, disponibilità 24/7
- **Aree miglioramento**: Personalizzazione, integrazione sistemi
- **Use cases preferiti**: Info veloci su scadenze/procedure

#### 4.5 Discussione Risultati *(2-3 pagine)*
##### Punti di Forza:
- Accuratezza routing soddisfacente (80%)
- Sistema completamente autonomo
- Costo zero per l'università

##### Limitazioni:
- Performance da ottimizzare (44s vs target 5s)
- Corpus documentale limitato
- Mancanza integrazione con sistemi esistenti

##### Confronto Stato dell'Arte:
- Costi: €0 vs €100s/mese API commerciali
- Privacy: Totalmente locale vs cloud
- Personalizzazione: Specifica UniBG vs generica

---

### **CAPITOLO 5: CONCLUSIONI E LAVORI FUTURI** *(4-6 pagine)*
#### 5.1 Riassunto Contributi *(1-2 pagine)*
- Primo chatbot RAG completo per UniBG con architettura gratuita
- Validazione empirica su dataset realistico e user study
- Framework replicabile per altre università italiane

#### 5.2 Obiettivi Raggiunti *(1-2 pagine)*
- ✅ Sistema RAG funzionante con tecnologie gratuite
- ✅ Routing intelligente implementato (80% accuratezza)
- ✅ Interfacce multiple sviluppate e testate
- ✅ Valutazione quantitativa e qualitativa completata

#### 5.3 Lavori Futuri *(1-2 pagine)*
##### Ottimizzazioni Tecniche:
- Cache embeddings per performance
- Fine-tuning modello su documenti UniBG
- Integrazione con sistemi universitari esistenti

##### Espansioni Funzionali:
- Supporto multilingue (inglese per studenti internazionali)
- Voice interface per accessibilità
- Dashboard analytics per amministratori

##### Deployment Produzione:
- Containerizzazione (Docker)
- Load balancing per multiple università
- Monitoring e alerting automatici

---

### **BIBLIOGRAFIA** *(2-3 pagine)*
**Target: 15-20 riferimenti di qualità**

**Paper Fondamentali:**
- Lewis et al. (2020) - "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- Reimers & Gurevych (2019) - "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"

**Chatbot Educativi:**
- Educational chatbot surveys (2023-2024)
- University case studies (ASU, Georgia State)

**Tecnologie:**
- Mistral AI papers
- ChromaDB documentation
- Ollama deployment guides

### **APPENDICI** *(3-5 pagine)*
- **Appendice A**: Esempi query e risposte
- **Appendice B**: Codice sorgente principale
- **Appendice C**: Questionario user study
- **Appendice D**: Risultati dettagliati test

---

## 📊 **DISTRIBUZIONE PAGINE OTTIMIZZATA**

| Capitolo | Pagine | Focus Principale |
|----------|--------|-----------------|
| Cap. 1 | 6-8 | Motivazione + Obiettivi |
| Cap. 2 | 8-10 | Background essenziale |
| Cap. 3 | 15-18 | **Implementazione** (cuore tecnico) |
| Cap. 4 | 12-15 | **Valutazione** (risultati sperimentali) |
| Cap. 5 | 4-6 | Conclusioni + Futuro |
| Bibliografia | 2-3 | 15-20 riferimenti |
| Appendici | 3-5 | Materiali supporto |
| **TOTALE** | **50-65** | Target triennale |

---

## 🎯 **FOCUS TRIENNALE - COSA ENFATIZZARE**

### **✅ PUNTI DI FORZA PER TRIENNALE:**
1. **Implementazione Pratica**: Sistema funzionante end-to-end
2. **Tecnologie Moderne**: RAG, LLM locali, embeddings
3. **Valutazione Empirica**: Test automatici + user study
4. **Impatto Reale**: Soluzione per problema universitario concreto
5. **Innovazione**: Prima implementazione RAG gratuita per UniBG

### **📝 STILE DI SCRITTURA:**
- **Pragmatico**: Focus su "cosa ho fatto" e "come funziona"
- **Diretto**: Meno teoria, più implementazione e risultati
- **Quantitativo**: Metriche concrete, grafici, numeri
- **Applicativo**: Enfasi su utilità pratica e replicabilità

### **🎨 ELEMENTI VISIVI:**
- **3-5 diagrammi** architettura sistema
- **5-8 grafici** risultati performance
- **2-3 screenshot** interfacce
- **1-2 tabelle** comparative tecnologie

---

## ⏰ **TIMELINE TRIENNALE OTTIMIZZATA**

### **📅 PIANO 3 SETTIMANE:**

#### **SETTIMANA 1: Ricerca + Setup**
- **Giorni 1-3**: Bibliografia (10-15 paper essenziali)
- **Giorni 4-5**: User study execution (10-15 partecipanti)
- **Giorni 6-7**: Analisi dati raccolti

#### **SETTIMANA 2: Scrittura Core**
- **Giorni 1-2**: Capitolo 3 (Implementazione) - 15 pagine
- **Giorni 3-4**: Capitolo 4 (Valutazione) - 12 pagine  
- **Giorni 5-7**: Capitolo 2 (Background) - 8 pagine

#### **SETTIMANA 3: Finalizzazione**
- **Giorni 1-2**: Capitolo 1 (Introduzione) + Cap 5 (Conclusioni)
- **Giorni 3-4**: Bibliografia + Appendici
- **Giorni 5-7**: Revisione, formattazione, correzioni

**🎯 Target finale: 50-55 pagine di qualità triennale!**

---

## 🚀 **PROSSIMO STEP IMMEDIATE:**

Vuoi che iniziamo con:
1. **📚 Ricerca bibliografia** (10-15 paper essenziali)
2. **👥 User study rapido** (10-15 studenti in 1 settimana)  
3. **✍️ Scrittura Capitolo 3** (hai già tutto il materiale tecnico)

**Quale preferisci per partire subito?** 🎯
