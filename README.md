# 🤖 CHATBOT SEGRETERIA STUDENTI - UniBG

Assistente virtuale per rispondere alle domande degli studenti universitari usando **intelligenza artificiale** e **RAG (Retrieval-Augmented Generation)**.

## 📋 Cosa può fare il chatbot?

Il chatbot risponde a domande su:

- ✅ **Iscrizioni** agli esami e ai corsi
- 💰 **Tasse universitarie** e pagamenti
- 📄 **Certificati** e documenti (laurea, iscrizione, etc.)
- 📅 **Orari** delle lezioni e contatti segreteria
- 🎓 **Servizi** per studenti (mense, biblioteche, wifi)
- 📊 **Carriera** universitaria e piani di studio
- 🧭 **Orientamento** e informazioni generali

---

## 🚀 GUIDA RAPIDA - Come usare il chatbot

### 📦 PREREQUISITI

Prima di iniziare, assicurati di avere:

1. **Python 3.10+** installato → [Scarica Python](https://www.python.org/downloads/)
2. **Ollama** installato e avviato → [Scarica Ollama](https://ollama.ai/download)
3. **Git** (opzionale, per clonare il progetto) → [Scarica Git](https://git-scm.com/)

---

## 🛠️ INSTALLAZIONE (Prima volta)

### Windows (Metodo Automatico) ⚡

Doppio click su **`setup.bat`** nella cartella principale.

Lo script installerà automaticamente:
- Ambiente virtuale Python
- Tutte le dipendenze necessarie
- Download del modello AI (Mistral 7B)

**Tempo richiesto:** ~5-10 minuti (dipende dalla connessione internet)

### Installazione Manuale (Windows/Linux/Mac)

```bash
# 1. Entra nella cartella del progetto
cd Chatbot_SegreteriaStudenti

# 2. Crea ambiente virtuale Python
python -m venv chatbot_env

# 3. Attiva l'ambiente virtuale

# Windows CMD:
chatbot_env\Scripts\activate.bat

# Windows PowerShell:
.\chatbot_env\Scripts\Activate.ps1

# Linux/Mac:
source chatbot_env/bin/activate

# 4. Installa le dipendenze
pip install -r requirements.txt

# 5. Crea il database vettoriale (necessario per il RAG)
python src/creazione_vectorstore.py
```
---

## 🎯 USARE IL CHATBOT

### Metodo 1: Interface Web (Consigliato) 🌐

**Windows - Avvio Veloce:**

Doppio click su **`start_web.bat`**

Il browser si aprirà automaticamente su `http://localhost:8501`

**Manuale (Windows/Linux/Mac):**

```bash
# 1. Attiva ambiente virtuale (se non già attivo)
# Windows CMD:
chatbot_env\Scripts\activate.bat

# Windows PowerShell:
.\chatbot_env\Scripts\Activate.ps1

# Linux/Mac:
source chatbot_env/bin/activate

# 2. Avvia l'interface web
streamlit run interfaccia/streamlit.py
```

### Metodo 2: Console/Terminale 💻

**Windows - Avvio Veloce:**

Doppio click su **`start_chatbot.bat`**

**Manuale (Windows/Linux/Mac):**

```bash
# 1. Attiva ambiente virtuale
# (vedi comandi sopra)

# 2. Avvia il chatbot
python main.py
```

**Esempio di conversazione:**

```
Chatbot avviato! Digita 'exit' per uscire.

> Come mi iscrivo all'esame?
Per iscriverti agli esami devi...

> Quali tasse devo pagare?
All'immatricolazione paghi...
```

---

## 🔄 AGGIORNARE IL DATABASE

Se aggiungi nuovi documenti nella cartella `data/FAQ/` o modifichi quelli esistenti:

**Windows - Avvio Veloce:**

Doppio click su **`aggiornamento_db.bat`**

**Manuale:**

```bash
# Attiva ambiente virtuale
chatbot_env\Scripts\activate.bat    # Windows
source chatbot_env/bin/activate     # Linux/Mac

# Rigenera il database
python src/creazione_vectorstore.py
```

---

## 🆘 RISOLUZIONE PROBLEMI

### ❌ Errore: "ModuleNotFoundError" o "python non trovato"

**Causa:** Ambiente virtuale non attivo o Python non installato

**Soluzione:**

```bash
# Verifica che Python sia installato
python --version

# Se Python è installato, attiva l'ambiente virtuale
# Windows:
chatbot_env\Scripts\activate.bat

# Linux/Mac:
source chatbot_env/bin/activate

# Controlla che il prompt inizi con (chatbot_env)
# Esempio: (chatbot_env) C:\...\Chatbot_SegreteriaStudenti>
```

### ❌ Errore: "No module named 'chromadb'" (o altra libreria)

**Causa:** Dipendenze non installate

**Soluzione:**

```bash
# 1. Attiva ambiente virtuale (vedi sopra)
# 2. Installa dipendenze
pip install -r requirements.txt
```

### ❌ Errore: "Connection refused" o "Ollama non risponde"

**Causa:** Ollama non è in esecuzione

**Soluzione:**

```bash
# 1. Installa Ollama (se non l'hai già fatto)
# Windows: https://ollama.ai/download
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# Mac: brew install ollama

# 2. Avvia Ollama (in un terminale separato)
ollama serve

# 3. Scarica il modello AI (prima volta, ~4GB)
ollama pull mistral

# 4. Verifica che Ollama funzioni
ollama list
```

**⚠️ IMPORTANTE:** Tieni aperto il terminale con `ollama serve` mentre usi il chatbot!

### ❌ Errore: "Port 8501 già in uso" (Streamlit)

**Causa:** Un'altra istanza di Streamlit è già aperta

**Soluzione:**

```bash
# Opzione A - Usa porta diversa
streamlit run interfaccia/streamlit.py --server.port 8502

# Opzione B - Chiudi il processo esistente
# Windows:
netstat -ano | findstr :8501
taskkill /F /PID <PID_NUMBER>

# Linux/Mac:
lsof -ti:8501 | xargs kill -9
```

### ❌ Database vettoriale corrotto o errori ChromaDB

**Soluzione:**

```bash
# 1. Attiva ambiente virtuale
chatbot_env\Scripts\activate.bat    # Windows
source chatbot_env/bin/activate     # Linux/Mac

# 2. Elimina il database corrotto
# Windows:
rmdir /s /q vectordb

# Linux/Mac:
rm -rf vectordb/

# 3. Ricrea il database da zero (~2-3 minuti)
python src/creazione_vectorstore.py
```

---

## 📁 STRUTTURA PROGETTO

```
Chatbot_SegreteriaStudenti/
│
├── 📄 main.py                      ⭐ Punto di ingresso principale
├── 📄 requirements.txt             📦 Dipendenze Python
│
├── 🔧 setup.bat                    🚀 Setup automatico Windows
├── 🔧 start_chatbot.bat            🚀 Avvia chatbot console
├── 🔧 start_web.bat                🚀 Avvia interface web
├── 🔧 aggiornamento_db.bat         🔄 Aggiorna database
│
├── 📁 chatbot_env/                 🐍 Ambiente virtuale Python
│   ├── Scripts/activate.bat       (attiva ambiente)
│   └── Lib/site-packages/         (dipendenze installate)
│
├── 📁 src/                         💻 Codice sorgente
│   ├── ollama_llm.py              (comunicazione con AI)
│   ├── creazione_vectorstore.py   (crea database vettoriale)
│   ├── local_embeddings.py        (embeddings documenti)
│   ├── link_enhancer.py           (aggiunge link utili)
│   └── prompt_templates.py        (template domande AI)
│
├── 📁 interfaccia/                 🌐 Interface web
│   └── streamlit.py               (app web moderna)
│
├── 📁 data/                        📚 Database conoscenza
│   ├── FAQ/                       (15 file FAQ categorizzati)
│   └── guida_dello_studente/      (4 PDF guide UniBG)
│
└── 📁 vectordb/                    🗄️ Database vettoriale ChromaDB
    ├── chroma.sqlite3             (database SQLite)
    └── ...                        (embeddings vettoriali)
```

**Tecnologie usate:**
- 🤖 **LLM:** Mistral 7B (via Ollama)
- 🔍 **Vector DB:** ChromaDB con embeddings all-MiniLM-L6-v2
- 🌐 **Interface:** Streamlit (web) + CLI (console)
- 🐍 **Linguaggio:** Python 3.13

---

## 📞 SUPPORTO E CONTATTI

- 🎓 **Studente:** Michele Caprinali
- 📧 **Email:** m.caprinali@studenti.unibg.it
- 🏫 **Università:** Università degli Studi di Bergamo
- 🔗 **Repository:** [GitHub](https://github.com/MicheleCaprinali/TesiTriennale)

---

## 📝 NOTE TECNICHE

- **Modello AI:** Mistral 7B (locale, nessuna connessione a servizi esterni)
- **Embeddings:** all-MiniLM-L6-v2 (384 dimensioni)
- **Vector DB:** ChromaDB con ricerca top-k=5
- **Documenti:** 16 FAQ categorizzate + 4 PDF guide UniBG
- **Privacy:** Tutto locale, nessun dato inviato a server esterni

**Requisiti hardware consigliati:**
- RAM: 8GB+ (16GB consigliati per performance ottimali)
- Spazio disco: 10GB liberi (per modello AI e dipendenze)
- CPU: Qualsiasi processore moderno (GPU opzionale ma non necessaria)