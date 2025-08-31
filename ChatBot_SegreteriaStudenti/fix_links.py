#!/usr/bin/env python3
"""
Script per correggere i problemi con i link nei file estratti
"""

import os
import re

def fix_malformed_links():
    """Corregge i link malformati nei file di testo"""
    print("CORREZIONE LINK MALFORMATI")
    print("=" * 40)
    
    extracted_dir = "extracted_text"
    fixes_made = 0
    
    # Pattern per trovare link malformati
    patterns_to_fix = [
        # Link con parentesi extra alla fine
        (r'(https?://[^\s<>"{}|\\^`\[\]]+)\)', r'\1'),
        # Link con virgole/punti alla fine
        (r'(https?://[^\s<>"{}|\\^`\[\]]+)[,.](?=\s|$)', r'\1'),
        # Link duplicati sulla stessa riga
        (r'(https?://[^\s<>"{}|\\^`\[\]]+)\s+\1', r'\1'),
        # Spazi extra negli URL
        (r'(https?://[^\s]+)\s+([^\s/]+)', r'\1/\2'),
    ]
    
    for filename in os.listdir(extracted_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(extracted_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Applica le correzioni
                for pattern, replacement in patterns_to_fix:
                    content = re.sub(pattern, replacement, content)
                
                # Salva solo se ci sono stati cambiamenti
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Corretto: {filename}")
                    fixes_made += 1
                    
            except Exception as e:
                print(f"❌ Errore in {filename}: {e}")
    
    print(f"\n📊 File corretti: {fixes_made}")
    return fixes_made

def optimize_ollama_settings():
    """Crea un file di configurazione ottimizzato per Ollama"""
    config_content = '''# Configurazione ottimizzata per Ollama
# Riduce i timeout e migliora le performance

# Variabili di ambiente per ottimizzare Ollama
OLLAMA_HOST=127.0.0.1:11434
OLLAMA_NUM_PARALLEL=1
OLLAMA_MAX_LOADED_MODELS=1

# Per ridurre l'uso di memoria
OLLAMA_FLASH_ATTENTION=1

# Timeout per le richieste (secondi)
OLLAMA_REQUEST_TIMEOUT=45
'''
    
    try:
        with open('.env.ollama', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("✅ Creato file di configurazione Ollama ottimizzata")
        return True
    except Exception as e:
        print(f"❌ Errore creazione config: {e}")
        return False

def create_fast_response_fallback():
    """Crea un sistema di fallback per risposte rapide quando il LLM è lento"""
    
    fallback_content = '''"""
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
'''
    
    try:
        with open('src/quick_responses.py', 'w', encoding='utf-8') as f:
            f.write(fallback_content)
        
        print("✅ Creato sistema di risposte rapide")
        return True
    except Exception as e:
        print(f"❌ Errore creazione fallback: {e}")
        return False

if __name__ == "__main__":
    print("RIPARAZIONE PROBLEMI LINK")
    print("=" * 50)
    
    # 1. Correggi link malformati
    fix_malformed_links()
    
    print("\n" + "=" * 50)
    
    # 2. Ottimizza configurazione Ollama
    optimize_ollama_settings()
    
    print("\n" + "=" * 50)
    
    # 3. Crea sistema di fallback
    create_fast_response_fallback()
    
    print("\n" + "=" * 50)
    print("CORREZIONI COMPLETATE!")
    print("=" * 50)
    
    print("\n📋 PROSSIMI PASSI:")
    print("1. Riavvia Ollama: ollama serve")
    print("2. Rigenera il vectorstore: python src/create_vectorstore.py")
    print("3. Testa il chatbot: python main.py")
