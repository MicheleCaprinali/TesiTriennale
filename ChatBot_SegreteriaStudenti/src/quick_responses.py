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
    
    "tirocini_estero": {
        "keywords": ["tirocinio all'estero", "tirocini estero", "stage estero"],
        "response": """Per tirocini all'estero:

🔗 **Informazioni generali:** https://www.unibg.it/studia-noi/frequentare/tirocini/tirocinio-allestero

🔗 **Bandi tirocini estero:** https://www.unibg.it/universita/amministrazione/concorsi-e-selezioni/bandi-tirocini-e-studio-allestero

🔗 **Accertamento linguistico:** https://www.unibg.it/internazionale/andare-allestero/partire/accertamento-conoscenza-linguistica

Per maggiori dettagli contatta l'Ufficio Tirocini al (+39 035 205 2265)"""
    },
    
    "segreteria_orari": {
        "keywords": ["orari segreteria", "quando aperta", "orario sportello"],
        "response": """**Orari Segreteria Studenti:**

📍 **Sede Bergamo** (via dei Caniana, 2):
• **Lunedì:** 13:30-15:30
• **Giovedì:** 10:00-12:00

📍 **Sede Dalmine** (via Einstein, 2):
• **Lunedì:** 13:30-15:30  
• **Giovedì:** 10:00-12:00

📞 **Telefono:** Lunedì-Venerdì 10:30-12:00

🎥 **Videoconferenza:**
• **Mercoledì:** 10:00-12:00
• **Venerdì:** 10:00-12:00

🎫 **Per richieste:** https://helpdesk.unibg.it/helpdesksegrestud/"""
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
