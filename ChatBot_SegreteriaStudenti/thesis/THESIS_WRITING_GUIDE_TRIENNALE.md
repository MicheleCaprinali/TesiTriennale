# 🎓 GUIDA SCRITTURA TESI TRIENNALE - ChatBot RAG UniBG

## 📝 **STRATEGIA OTTIMIZZATA (50-60 pagine)**

### **🎯 MINDSET TRIENNALE:**
- **Focus**: Implementazione pratica + Valutazione empirica
- **Stile**: Diretto, concreto, orientato ai risultati
- **Enfasi**: "Cosa ho fatto" > "Cosa esiste in letteratura"
- **Obiettivo**: Dimostrare competenze tecniche e capacità di problem-solving

---

## 📅 **PIANO DI SCRITTURA 3 SETTIMANE**

### **🗓️ SETTIMANA 1: PREPARAZIONE**

#### **GIORNI 1-2: Ricerca Bibliografia Essenziale**
```
🎯 Target: 10-15 paper chiave (NON 30!)
📍 Focus su:
- 3-4 paper RAG fundamentals
- 2-3 educational chatbot case studies  
- 2-3 local LLM deployment
- 2-3 evaluation methodologies

🔍 Strategia rapida:
- Cerca "survey" papers per overview rapidi
- Focus su paper 2022-2024 (più recenti)
- Priorità: abstract + conclusions + figures
```

#### **GIORNI 3-5: User Study Execution**
```
👥 Target: 10-15 studenti UniBG
⏱️ Sessioni: 30 min ciascuna
📊 Dati da raccogliere:
- SUS scores
- Task completion rates
- Qualitative feedback
- Performance metrics
```

#### **GIORNI 6-7: Analisi Dati**
```
📈 Output necessari:
- Grafici performance (già hai thesis_performance_charts.png)
- Statistiche user study
- Tabelle comparative
- Error analysis
```

---

### **🗓️ SETTIMANA 2: SCRITTURA CORE**

#### **GIORNI 1-2: Capitolo 3 - Implementazione (15-18 pagine)**
```
✍️ SEZIONI DA SCRIVERE:

3.1 Analisi Requisiti (2-3 pagine)
- Requisiti funzionali (3-4 punti essenziali)
- Requisiti non funzionali (performance, costi, privacy)
- Constraints tecnici (hardware, software disponibili)

3.2 Architettura Sistema (3-4 pagine)  
- Diagramma overview (usa draw.io o PowerPoint)
- Componenti principali (5-6 blocchi max)
- Data flow (documenti → embeddings → retrieval → response)
- Technology stack decision matrix

3.3 Implementazione Dettagliata (6-8 pagine)
- Document processing (statistiche: 20 docs, 113 chunks)
- Embedding system (all-MiniLM-L6-v2 specifics)
- Vector store (ChromaDB configuration)
- LLM integration (Ollama + Mistral setup)
- User interfaces (CLI + Streamlit screenshots)
- Routing logic (personal query detection)

3.4 Scelte Tecnologiche (2 pagine)
- Comparison table (tua scelta vs alternatives)
- Motivazioni (costo, performance, privacy)
```

#### **GIORNI 3-4: Capitolo 4 - Valutazione (12-15 pagine)**
```
✍️ SEZIONI DA SCRIVERE:

4.1 Metodologia (2-3 pagine)
- Test dataset (100 query realistiche)
- Metriche evaluation (response time, accuracy, usability)
- Experimental setup (hardware, software, configuration)

4.2 Risultati Performance (4-5 pagine)
- Automated tests (usa i tuoi dati: 44.29s avg, 80% accuracy)
- Grafici da thesis_performance_charts.png
- Resource utilization analysis
- Bottleneck identification

4.3 User Study (4-5 pagine)
- Participant demographics
- Task completion analysis
- SUS scores + satisfaction metrics
- Qualitative feedback themes

4.4 Discussione (2-3 pagine)  
- Strengths vs limitations
- Comparison con state-of-art (costi, privacy, customization)
- Lessons learned
```

#### **GIORNI 5-7: Capitolo 2 - Background (8-10 pagine)**
```
✍️ SEZIONI DA SCRIVERE:

2.1 Retrieval-Augmented Generation (3-4 pagine)
- RAG principles (retrieval + generation pipeline)
- Advantages over pure LLM (hallucination reduction, domain knowledge)
- Architecture overview (cite Lewis et al. 2020)

2.2 Tecnologie Chiave (3-4 pagine)
- Local LLM deployment (Ollama ecosystem)
- Sentence embeddings (SentenceTransformers overview)  
- Vector databases (ChromaDB vs alternatives)

2.3 Educational Chatbots (2-3 pagine)
- University case studies (ASU, Georgia State)
- Common challenges (cost, privacy, integration)
- Gap analysis (what's missing in current solutions)
```

---

### **🗓️ SETTIMANA 3: FINALIZZAZIONE**

#### **GIORNI 1-2: Apertura e Chiusura**
```
✍️ Capitolo 1: Introduzione (6-8 pagine)
- Motivation (concrete university problems)
- Objectives (clear, measurable goals)
- Contributions (what you achieved uniquely)

✍️ Capitolo 5: Conclusioni (4-6 pagine)  
- Summary achievements
- Limitations acknowledgment
- Future work roadmap
```

#### **GIORNI 3-4: Bibliografia e Appendici**
```
📚 Bibliografia (2-3 pagine)
- 15-20 riferimenti essenziali
- IEEE format standard
- Balance: foundational papers + recent work

📋 Appendici (3-5 pagine)
- Code snippets principali
- Complete user study questionnaire  
- Detailed experimental results
- Query examples + responses
```

#### **GIORNI 5-7: Revisione e Formattazione**
```
🔍 Quality check:
- Consistency terminologia
- Figure numbering and captions
- Reference formatting
- Abstract + summary writing
- Table of contents
- Final proofreading
```

---

## 📊 **TEMPLATE SEZIONI CHIAVE**

### **🔧 TEMPLATE SEZIONE IMPLEMENTAZIONE:**
```markdown
## 3.X [Component Name]

### Descrizione
[Cosa fa questo componente in 2-3 frasi]

### Implementazione
```python
# Code snippet significativo (5-10 righe max)
class ComponentName:
    def key_method(self):
        # Logic core
        return result
```

### Configurazione
- **Parameter 1**: Value (motivazione)
- **Parameter 2**: Value (trade-off consideration)

### Risultati
- **Metric 1**: X value
- **Metric 2**: Y value

### Challenges e Soluzioni
- **Problem**: [Specific issue encountered]
- **Solution**: [How you solved it]
```

### **📈 TEMPLATE SEZIONE RISULTATI:**
```markdown
## 4.X [Experiment Name]

### Setup
- **Dataset**: N samples, characteristics
- **Metrics**: What you measured, why
- **Procedure**: Step-by-step execution

### Risultati Quantitativi
[Table or bullet points with numbers]

### Analisi
[What the numbers mean, implications]

### Discussione
[Strengths, limitations, comparison with expectations]
```

---

## 🎯 **CONTENT GUIDELINES TRIENNALE**

### **✅ COSA INCLUDERE:**
- **Concrete results**: Numeri, grafici, screenshot
- **Implementation details**: Code snippets, configurations
- **Problem-solving**: Challenges encountered + solutions
- **Evaluation**: Quantitative + qualitative evidence
- **Practical impact**: How this helps real students

### **❌ COSA EVITARE:**
- **Excessive theory**: Deep mathematical formulations
- **Exhaustive literature review**: Focus on key papers only
- **Implementation trivia**: Every small code detail
- **Speculation**: Stick to what you actually tested
- **Perfectionism**: Good enough > perfect but incomplete

### **📝 WRITING STYLE:**
- **Active voice**: "I implemented" > "It was implemented"
- **Concrete language**: "44.29s average" > "reasonable performance"
- **Direct structure**: Problem → Solution → Results → Discussion
- **Visual support**: Every claim supported by figure/table when possible

---

## 🚀 **QUICK START ACTIONS**

### **📅 OGGI - IMMEDIATE NEXT STEPS:**

1. **Choose starting point:**
   - **Option A**: Bibliografia (safer, traditional approach)
   - **Option B**: User Study (fresh data for results)
   - **Option C**: Capitolo 3 (you have all implementation ready)

2. **Setup writing environment:**
   - LaTeX template or Word document
   - Figure folder structure
   - Bibliography manager (Zotero/Mendeley)

3. **Time blocking:**
   - 3-4 hours writing sessions
   - Daily targets: 3-5 pages
   - Weekly reviews and adjustments

### **🎯 SUCCESS METRICS:**
- **Week 1 end**: 15 references + user study data
- **Week 2 end**: 35-40 pages core content  
- **Week 3 end**: 50-55 pages complete draft

**Quale starting point scegli? Posso guidarti step-by-step! 🎯**
