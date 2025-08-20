# GUIDA AI FILE .BAT ALL'INTERNO DEL PROGETTO

### **`start_chatbot.bat`**
- **Funzione**: Avvia il chatbot in modalità console
- **Output**: Interfaccia testuale interattiva
- **Comando equivalente**: 
  ```bash
  .\venv\Scripts\Activate.ps1
  python main.py
  ```

### **`start_web.bat`**
- **Funzione**: Avvia l'interfaccia web Streamlit
- **URL**: http://localhost:8501
- **Comando equivalente**: 
  ```bash
  .\venv\Scripts\Activate.ps1
  streamlit run interfaces/streamlit_app.py
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
- **Processo**:
  1. Estrazione testo da documenti
  2. Creazione nuovo vectorstore
- **ATTENZIONE**: Sovrascrive il database esistente

### **`setup.bat`**
- **Funzione**: Setup completo dell'ambiente di sviluppo
- **Include**:
  - Creazione/verifica ambiente virtuale
  - Installazione dipendenze
  - Controllo Ollama e modello Mistral
  - Test configurazione
- **Quando usare**: Prima installazione o problemi con l'ambiente
