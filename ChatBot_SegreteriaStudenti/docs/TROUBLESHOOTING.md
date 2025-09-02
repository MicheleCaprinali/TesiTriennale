# 🔧 GUIDA RISOLUZIONE PROBLEMI

## Problemi Comuni e Soluzioni

### ❌ "Python non trovato"
**Problema**: `'python' is not recognized`
**Soluzione**:
1. Installa Python da: https://www.python.org/downloads/
2. **IMPORTANTE**: Seleziona "Add Python to PATH"
3. Riavvia terminale
4. Verifica: `python --version`

### ❌ "Ollama non risponde"
**Problema**: Errori di connessione LLM
**Soluzione**:
```cmd
ollama serve
```
Se non installato: https://ollama.ai

### ❌ "Modello Mistral mancante"
**Problema**: Modello LLM non trovato
**Soluzione**:
```cmd
ollama pull mistral:7b
```

### ❌ "Ambiente virtuale non attivato"
**Problema**: Dipendenze non trovate
**Soluzione**:
```cmd
venv\Scripts\activate.bat
```

### ❌ "Database vettoriale corrotto"
**Problema**: Errori di ricerca
**Soluzione**:
```cmd
venv\Scripts\python.exe src\create_vectorstore.py
```

### ❌ "Porta 8501 occupata"
**Problema**: Streamlit non si avvia
**Soluzione**:
```cmd
# Cambio porta
streamlit run interfaces\streamlit_app.py --server.port 8502
```

### ❌ "Dipendenze mancanti"
**Problema**: Import error moduli
**Soluzione**:
```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt --force-reinstall
```

### ❌ "Memoria insufficiente"
**Problema**: Sistema lento/crash
**Soluzione**:
- Chiudi altre applicazioni
- Verifica RAM disponibile (minimo 8GB)
- Riavvia Ollama: `ollama serve`

## 📋 Checklist Debug

1. **Python installato?** → `python --version`
2. **Ambiente virtuale attivo?** → `venv\Scripts\activate.bat`
3. **Ollama funzionante?** → `ollama list`
4. **Modello Mistral presente?** → `ollama list | findstr mistral`
5. **Database presente?** → Controlla cartella `vectordb`
6. **Dipendenze installate?** → `pip list | findstr streamlit`

## 🆘 Reset Completo

Se nulla funziona:
```cmd
# 1. Backup dati (opzionale)
# 2. Elimina ambiente virtuale
rmdir /s venv

# 3. Re-setup completo
setup_auto.bat
```

## 📞 Supporto

Per problemi non risolti:
- Controlla log degli errori
- Verifica requisiti sistema (8GB RAM, 10GB storage)
- Documenta errore specifico e contesto
