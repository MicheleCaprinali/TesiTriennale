# 🤖 ChatBot RAG - Università di Bergamo
### Sistema di Assistenza Intelligente per Segreteria Studenti

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/LLM-Mistral%207B-green.svg)](https://ollama.ai/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![Streamlit](https://img.shields.io/badge/Interface-Streamlit-red.svg)](https://streamlit.io/)

---

## 📋 **PANORAMICA PROGETTO**

Sistema **RAG (Retrieval-Augmented Generation)** sviluppato per assistere gli studenti dell'**Università di Bergamo** con informazioni su:
- 🎓 **Procedure di iscrizione** esami e corsi
- 💰 **Tasse universitarie** e modalità di pagamento
- 📅 **Orari segreteria** e uffici amministrativi
- 📜 **Certificazioni** e documenti ufficiali
- ♿ **Servizi per studenti** con esigenze speciali

---

## 🏗️ **ARCHITETTURA SISTEMA**

### **Stack Tecnologico**
```
Frontend:     Streamlit Web UI + Console CLI
LLM:          Mistral 7B (via Ollama)
Embeddings:   all-MiniLM-L6-v2 (384 dim)
VectorDB:     ChromaDB 1.0.20
Backend:      Python 3.13 + SentenceTransformers
```

### **Componenti RAG**
- **📁 Document Processing**: Estrazione automatica da PDF e documenti UniBG
- **🔍 Vector Search**: Ricerca semantica con similarity search
- **🤖 LLM Generation**: Generazione risposte contestuali con Mistral 7B
- **🔗 Link Enhancement**: Arricchimento automatico con link utili
- **📊 Quality Assessment**: Valutazione qualità risposte in tempo reale

---

## 🚀 **INSTALLAZIONE E AVVIO**

### **Setup Automatico**
```bash
# 1. Setup completo ambiente
setup.bat

# 2. Avvio interfaccia web
start_web.bat

# 3. Avvio console CLI  
start_chatbot.bat

# 4. Aggiornamento database
aggiornamento_db.bat
```

### **Setup Manuale (Alternativo)**
```bash
# Crea ambiente virtuale
python -m venv chatbot_env
chatbot_env\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Installa e avvia Ollama
# Scarica modello Mistral
ollama pull mistral:7b

# Avvia chatbot
python main.py
```

---

## 🎯 **PERFORMANCE E RISULTATI**

### **Metriche di Qualità** (Test Scientifico su 30+ domande)
| Metrica | Punteggio | Dettaglio |
|---------|-----------|-----------|
| **Accuratezza Complessiva** | **75.7%** | ↗️ +19.6% vs baseline |
| Rilevanza Semantica | 0.53-0.70 | Similarity coseno |
| Completezza Risposte | 0.4-1.0 | Copertura informazioni |
| Tono Professionale | 0.5-0.7 | Appropriato contesto UniBG |
| Tempo Risposta Medio | 132s | Include processing LLM |

### **Performance per Categoria**
- 🎓 **Iscrizioni Esami**: 72.5%
- 💰 **Tasse e Pagamenti**: 81.9%
- 📅 **Orari e Contatti**: 76.9%
- 📜 **Certificati**: 74.5%
- 🫧 **Servizi Studenti**: 72.4%

---

## 🛠️ **ARCHITETTURA TECNICA**

### **Struttura Directory**
```
📁 Chatbot_SegreteriaStudenti/
├── 📄 main.py                 # Entry point sistema
├── 📁 src/                    # Moduli core RAG
│   ├── ollama_llm.py         # Interface Mistral 7B
│   ├── local_embeddings.py   # SentenceTransformers
│   ├── creazione_vectorstore.py # ChromaDB management
│   └── prompt_templates.py   # Template ottimizzati
├── 📁 interfaccia/           # UI Streamlit
├── 📁 data/                  # Documenti e FAQ UniBG
├── 📁 vectordb/              # Database vettoriale
├── 📁 evaluation/            # Sistemi valutazione
├── 📁 results/               # Report test e metriche
└── 🏃‍♂️ *.bat                    # Script automazione
```

### **Workflow RAG**
1. **Query Processing**: Embedding domanda utente (384-dim)
2. **Document Retrieval**: Ricerca similarity in ChromaDB 
3. **Context Augmentation**: Selezione documenti più rilevanti
4. **Response Generation**: Mistral 7B + template ottimizzato
5. **Link Enhancement**: Arricchimento automatico link
6. **Quality Check**: Validazione risposta pre-delivery

---

## 📊 **SISTEMA DI VALUTAZIONE**

### **Metriche Software** (`evaluation/metriche_software.py`)
- **Cyclomatic Complexity**: Analisi AST nativa Python
- **Maintainability Index**: Score 0-10 basato su standard
- **Lines of Code**: Conteggio automatico codice/commenti
- **Class Coupling**: Dipendenze inter-modulari

### **Metriche RAG** (`evaluation/metriche_qualità.py`)  
- **Semantic Similarity**: Coseno embedding query-risposta
- **Content Completeness**: Presenza elementi informativi
- **Context Utilization**: Efficacia uso documenti retrieved
- **Professional Tone**: Appropriatezza linguaggio UniBG

### **Test Scientifici** (`tesi/testing/test_scientifico.py`)
- **30+ Test Cases**: Copertura multi-categoria
- **Statistical Analysis**: Confidence intervals, standard deviation
- **Performance Tracking**: Tempo risposta, lunghezza, qualità
- **Reproducible Results**: JSON timestampati per riproducibilità

---

## 🎨 **INTERFACCE UTENTE**

### **🌐 Web Interface** (Streamlit)
- Design responsive e moderno
- Chat interattiva real-time
- Display arricchito con link
- Feedback qualità risposte

### **💻 Console CLI**
- Interfaccia command-line
- Debug e testing rapido
- Logging dettagliato
- Performance monitoring

---

## 🔧 **CONFIGURAZIONE AVANZATA**

### **Environment Variables** (`.env`)
```bash
OLLAMA_HOST=localhost:11434
CHROMA_PERSIST_DIR=./vectordb
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=mistral:7b
MAX_CONTEXT_LENGTH=4000
TEMPERATURE=0.3
```

### **Personalizzazione Prompt** (`src/prompt_templates.py`)
- Template specifici per categoria domande
- Context injection ottimizzato
- Personality definition per tono UniBG
- Link enhancement patterns

---

## 🧪 **TESTING E QUALITY ASSURANCE**

### **Automated Testing**
```bash
# Test sistema completo
python evaluation/metriche_software.py

# Test qualità risposte  
python evaluation/metriche_qualità.py

# Test scientifico completo
python tesi/testing/test_scientifico.py
```

### **Continuous Integration**
- ✅ **Code Quality**: Metrics automatiche AST
- ✅ **Response Quality**: Valutazione semantica
- ✅ **Performance**: Monitoring tempo risposta
- ✅ **Reliability**: Test scientifici riproducibili

---

## 📈 **RISULTATI FINALI TESI**

### **Achievements**
- 🎯 **75.7% Accuracy** su dataset test completo
- ⚡ **132s Response Time** medio con LLM locale  
- 🔗 **5.4 Link/Response** in media per arricchimento
- 📊 **Statistical Significance** con confidence intervals
- 🏗️ **Professional Deployment** con automazione completa

### **Contributi Scientifici**
1. **RAG Optimization**: Template e context enhancement
2. **Multi-Modal Evaluation**: Software + RAG + UX metrics  
3. **Domain Adaptation**: Specializzazione UniBG context
4. **Deployment Automation**: Sistema .bat professionale
5. **Reproducible Research**: Framework test scientifici

---

## 👨‍💻 **AUTORE**

**Michele Caprinali**  
Tesi Triennale - Università di Bergamo  
*Ingegneria Informatica*

### **Relatori**
- Prof. [Nome Relatore]
- Prof. [Nome Correlatore]

---

## 📜 **LICENZA**

Progetto accademico sviluppato per Università di Bergamo.
© 2025 Michele Caprinali - Tutti i diritti riservati.

---

## 🔗 **LINK UTILI**

- 🏫 [Università di Bergamo](https://www.unibg.it/)
- 📚 [Ollama Documentation](https://ollama.ai/docs)
- 🗄️ [ChromaDB Guide](https://docs.trychroma.com/)
- 🤖 [SentenceTransformers](https://www.sbert.net/)
- 🎨 [Streamlit Docs](https://docs.streamlit.io/)

---

*Ultimo aggiornamento: Settembre 2025 - Sistema RAG v2.0*