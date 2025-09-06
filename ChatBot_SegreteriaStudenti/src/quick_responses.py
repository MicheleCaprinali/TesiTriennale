"""
Sistema di fallback per risposte rapide sui tirocini
"""

QUICK_RESPONSES = {
    "tirocini_info": {
        "keywords": ["tirocinio", "tirocini", "stage"],
        "response": """Per informazioni sui tirocini:

🔗 **Pagina principale tirocini:** https://www.unibg.it/studia-noi/frequentare/tirocinio

🔗 **Tirocini per dipartimento:** https://www.unibg.it/studia-noi/frequentare/tirocinio/tirocini-dipartimento

🔗 **Regolamento tirocini:** https://www.unibg.it/sites/default/files/normativa/regolamento_per_tirocini_curriculari_0.pdf

📞 **Ufficio Tirocini:** (+39 035 205 2265)
📍 **Indirizzo:** Via S.Bernardino 72/e, Bergamo

**Orari:** Lunedì, Mercoledì, Giovedì, Venerdì: 9:30-12:00"""
    },
    
    "segreteria_orari": {
        "keywords": ["orari segreteria", "quando aperta", "orario sportello", "orari", "quando è aperta"],
        "response": """**Orari Segreteria Studenti:**

📍 **Sede Bergamo** (via dei Caniana, 2):
• **Lunedì:** 13:30-15:30
• **Giovedì:** 10:00-12:00

📍 **Sede Dalmine** (via Einstein, 2):
• **Lunedì:** 13:30-15:30  
• **Giovedì:** 10:00-12:00

� **Telefono:** Lunedì-Venerdì 10:30-12:00

🎥 **Videoconferenza:**
• **Mercoledì:** 10:00-12:00
• **Venerdì:** 10:00-12:00

🎫 **Per richieste:** https://helpdesk.unibg.it/helpdesksegrestud/"""
    },
    
    "contatti_email": {
        "keywords": ["email segreteria", "contattare segreteria", "email", "contatti", "scrivere segreteria"],
        "response": """**Contatti Segreteria Studenti:**

📧 **Email principale:** segreteria.studenti@unibg.it
� **Per tasse:** tasse.studenti@unibg.it  
📧 **Per certificati:** certificati.studenti@unibg.it

🎫 **Sistema ticket:** https://helpdesk.unibg.it/helpdesksegrestud/

📞 **Telefono:** (+39 035 205 2014) - Lunedì-Venerdì 10:30-12:00

**Orari ricevimento:** Lunedì 13:30-15:30 e Giovedì 10:00-12:00"""
    },
    
    "tasse_pagamento": {
        "keywords": ["pagare tasse", "tasse", "pagamento", "rata", "contributi", "come pago"],
        "response": """**Pagamento Tasse Universitarie:**

� **Modalità di pagamento:**
• PagoPA (consigliato)
• Bonifico bancario
• Sportello bancario

🔗 **Pagina tasse:** https://www.unibg.it/studiare/iscriversi/tasse-e-agevolazioni

🔗 **Modalità pagamento:** https://www.unibg.it/studiare/iscriversi/tasse-e-agevolazioni/contribuzione-studentesca/modalita-pagamento

📅 **Scadenze rate:** Verifica sempre le date sul portale studenti

🎫 **Assistenza:** https://helpdesk.unibg.it/helpdesksegrestud/"""
    },
    
    "esami_iscrizione": {
        "keywords": ["iscriversi esami", "iscrizione esami", "prenotare esame", "esami", "prenotazione"],
        "response": """**Iscrizione agli esami:**

🔗 **Sportello Studenti (per iscriversi):** https://sportello.unibg.it/Home.do

� **Procedura:**
1. Accedi con le tue credenziali UniBG
2. Vai alla sezione "Esami"
3. Seleziona l'esame desiderato
4. Scegli data e orario disponibile
5. Conferma l'iscrizione

⏰ **Scadenze:** L'iscrizione chiude generalmente 3 giorni prima dell'esame

❌ **Cancellazione:** Possibile fino a 2 giorni prima dell'esame

🎫 **Problemi tecnici:** https://helpdesk.unibg.it/helpdesksegrestud/"""
    },
    
    "certificati_laurea": {
        "keywords": ["certificato laurea", "certificato", "diploma", "pergamena", "attestato"],
        "response": """**Certificati e Documenti:**

🔗 **Richiesta certificati:** http://www.unibg.it/node/6673

� **Tipi di certificato:**
• Certificato di laurea con/senza voti
• Pergamena di laurea
• Dichiarazione sostitutiva di certificazione

💰 **Costi:**
• Certificato semplice: gratuito
• Pergamena: circa 50€

⏱️ **Tempi:**
• Certificato digitale: 2-3 giorni
• Pergamena: 2-3 settimane

🎫 **Richieste:** https://helpdesk.unibg.it/helpdesksegrestud/"""
    },
    
    "pdf_conversion": {
        "keywords": ["pdf", "pdf/a", "convertire", "conversione"],
        "response": """Per convertire file in PDF/A:

🔗 **Guida conversione PDF/A:** https://www.unibg.it/sites/default/files/media/documents/2023-04-19/Guida_PDF-A.pdf

La guida contiene istruzioni dettagliate per convertire documenti nel formato PDF/A richiesto dall'università."""
    }
}

def get_quick_response(query):
    """Cerca una risposta rapida per la query"""
    query_lower = query.lower()
    
    for topic, data in QUICK_RESPONSES.items():
        if any(keyword in query_lower for keyword in data["keywords"]):
            return data["response"]
    
    return None
