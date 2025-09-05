# 👨‍🎓 Manuale Utente
## ChatBot Segreteria Studenti UniBG

**Versione aggiornata - Settembre 2025**

---

## 🚀 Avvio Rapido

### 1. **Avvia l'interfaccia web** (consigliata)
```cmd
start_web.bat
```
→ Vai su: **http://localhost:8501**

### 2. **Oppure usa la console**
```cmd
start_chatbot.bat
```

---

## 💬 Come Usare il ChatBot

### **Interfaccia Web** 
- **Design moderno** nero/azzurro, ottimizzato per UniBG
- **Esempi nella sidebar** - clicca per domande rapide
- **Link cliccabili** nelle risposte
- **Tempo di risposta**: 10-30 secondi

### **Tipi di domande supportate:**

✅ **OTTIME** (risposta rapida e accurata):
- "Orari della segreteria studenti"
- "Come iscriversi agli esami"
- "Quando pagare le tasse universitarie"
- "Informazioni su alloggi universitari"
- "Servizi per studenti con disabilità"
- "Come richiedere certificati"

✅ **BUONE** (risposta accurata):
- "Procedure per la laurea"
- "Info su tirocini e stage"
- "Contatti utili per problemi"
- "Borse di studio disponibili"
- "Modalità esami"

⚠️ **LIMITATE** (potrebbe rimandare alla segreteria):
- Domande su situazioni personali specifiche
- Richieste di accesso a dati privati
- Informazioni non presenti nelle guide 2025-2026

---

## 🎯 Esempi Pratici

### **Domanda sugli Alloggi:**
```
👤 "informazioni inerenti agli alloggi"

🤖 "Per gli alloggi universitari, UniBg offre diverse opzioni:
• Residenze universitarie gestite dall'ateneo
• Convenzioni con strutture private
• Servizio di supporto per la ricerca alloggi

🔗 https://www.unibg.it/vivere-unibg/spazi-e-servizi/alloggi

Per informazioni specifiche e disponibilità, contatta il servizio alloggi."
```

### **Domanda sui Contatti:**
```
👤 "contatti segreteria"

🤖 "Ecco i principali contatti:
• 📧 segreteria.studenti@unibg.it
• 📞 035 2052xxx (orari 9-12, 14-16)
• 🏢 Via dei Caniana 2, piano terra
• 🎫 Ticketing: https://helpdesk.unibg.it

Orari ricevimento: Lun-Ven 9:00-12:00, Mar-Gio 14:00-16:00"
```

---

## 🔧 Risoluzione Problemi

### **"Sistema temporaneamente lento"**
- **Causa**: Database grande, LLM occupato
- **Soluzione**: Riprova tra 30-60 secondi
- **Tempo normale**: 10-30 secondi per risposta

### **"Non ho informazioni sufficienti"**
- **Causa**: Domanda troppo specifica o non in database
- **Soluzione**: Riformula la domanda o contatta segreteria
- **Esempi**: Invece di "la mia situazione" → "procedure generali per..."

### **Link non funzionanti**
- **Causa**: Link obsoleti o errori di estrazione
- **Soluzione**: Vai direttamente su www.unibg.it
- **Nota**: Il sistema valida automaticamente i link

---

## 📋 FAQ Sistema

### **Q: Quanto è veloce il sistema?**
A: 10-30 secondi per risposta normale. Se impiega più di 60s, riprova.

### **Q: I dati sono aggiornati?**
A: Sì, basati su guide UniBG 2025-2026 e FAQ aggiornate.

### **Q: Posso chiedere info personali?**
A: No, il sistema fornisce solo info generali. Per dati personali usa il portale studenti.

### **Q: Il sistema memorizza le mie domande?**
A: No, è completamente locale e non salva conversazioni.

### **Q: Cosa fare se non funziona?**
A: Contatta direttamente la segreteria studenti o usa il sistema di ticketing UniBG.

---

## 📞 Supporto

**Per problemi tecnici:**
- Prova a riavviare: `start_web.bat`
- Verifica Ollama: `ollama --version`

**Per info universitarie:**
- 🎫 **Ticket**: https://helpdesk.unibg.it  
- 📧 **Email**: segreteria.studenti@unibg.it
- 🌐 **Sito**: https://www.unibg.it