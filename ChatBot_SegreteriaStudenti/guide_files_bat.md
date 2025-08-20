# GUIDA AI FILE .BAT ALL'INTERNO DEL PROGETTO

**IMPORTANTE:** I file .bat sono ottimizzati per Windows e richiedono che l'ambiente virtuale sia configurato correttamente.

### **`start_chatbot.bat`**
- **Funzione**: Avvia il chatbot in modalità console
- **Output**: Interfaccia testuale interattiva
- **Requisiti**: Ambiente virtuale attivo
- **Comando equivalente**: 
  ```bash
  venv\Scripts\activate.bat
  python main.py
  ```

### **`start_web.bat`**
- **Funzione**: Avvia l'interfaccia web Streamlit
- **URL**: http://localhost:8501
- **Requisiti**: Ambiente virtuale attivo
- **Comando equivalente**: 
  ```bash
  venv\Scripts\activate.bat
  streamlit run interfaces\streamlit_app.py --server.port 8501
  ```

### **`run_tests.bat`**
- **Funzione**: Esegue tutti i test e genera le metriche
- **Include**:
  - Test di retrieval
  - Test validazione link
  - Metriche software (CC, WMC, LCOM)
  - Valutazione performance
- **Output**: Risultati salvati in `results/`

### **`update_database.bat`**
- **Funzione**: Ricrea completamente il database vettoriale
- **Quando usare**: Se modifichi i file sorgente in `data/`
- **ATTENZIONE**: Sovrascrive il database esistente

### **`setup.bat`**
- **Funzione**: Setup completo dell'ambiente di sviluppo
- **Include**:
  - Creazione/verifica ambiente virtuale
  - Installazione dipendenze
  - Controllo Ollama e modello Mistral
  - Test configurazione
- **Quando usare**: Prima installazione o problemi con l'ambiente

## **RISOLUZIONE PROBLEMI**

Se i file .bat non funzionano:

1. **Esegui come Amministratore** se richiesto
2. **Verifica ambiente virtuale**: `setup.bat`
3. **Usa PowerShell**: Alcuni comandi potrebbero richiedere PowerShell
4. **Manuale**: Attiva l'ambiente ed esegui i comandi singolarmente

**Comando manuale per attivare ambiente:**
```powershell
.\venv\Scripts\Activate.ps1  # PowerShell
# OPPURE
venv\Scripts\activate.bat    # Command Prompt
```
