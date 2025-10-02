#!/usr/bin/env python3
"""
ChatBot Segreteria Studenti - Tesi Triennale Ingegneria Informatica
Sistema RAG (Retrieval-Augmented Generation) per assistenza automatizzata studenti universitari
Tecnologie: Mistral 7B + SentenceTransformers + ChromaDB
"""

import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv

# Carica variabili ambiente
load_dotenv()

# Aggiungi il path per gli import
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import moduli core con gestione errori
try:
    from src.local_embeddings import LocalEmbeddings
    from src.creazione_vectorstore import search_vectorstore, crea_vectorstore_free
    from src.ollama_llm import OllamaLLM
    from src.dividi_chunks import split_text_in_chunks
except ImportError:
    # Fallback per sviluppo locale
    try:
        from local_embeddings import LocalEmbeddings
        from creazione_vectorstore import search_vectorstore, crea_vectorstore_free
        from ollama_llm import OllamaLLM
        from dividi_chunks import split_text_in_chunks
    except ImportError as e:
        print(f"Errore import moduli: {e}")
        print("Esegui: pip install -r requirements.txt")
        sys.exit(1)

class ChatbotRAG:
    """Classe principale del chatbot RAG - coordina embedding, retrieval e generazione"""
    
    def __init__(self):
        """Inizializza i componenti core del sistema RAG"""
        
        try:
            # Inizializza sistema di embedding semantico
            self.embedder = LocalEmbeddings()
            
            # Inizializza LLM locale (Mistral 7B)
            self.llm = OllamaLLM()
            
            # Verifica connessione Ollama
            if not self.llm.check_connection():
                raise Exception("Ollama non raggiungibile")
            
        except Exception as e:
            print(f"Errore inizializzazione: {e}")
            raise
    
    def retrieve_documents(self, query, k=5):
        """Recupera documenti semanticamente rilevanti dal vector database"""
        try:
            results = search_vectorstore(query, k=k, embedder=self.embedder)
            
            if not results["documents"] or not results["documents"][0]:
                return []
            
            # Formatta documenti con score di rilevanza
            docs = []
            for doc, distance in zip(results["documents"][0], results["distances"][0]):
                docs.append({
                    "content": doc,
                    "score": distance
                })
            
            return docs
            
        except Exception as e:
            print(f"Errore retrieval: {e}")
            return []
    
    def generate_response(self, query, context_docs):
        """Genera risposta contestualizzata usando il modello LLM"""
        
        # Costruisci contesto dai documenti recuperati
        if context_docs:
            context = "\n\n".join([doc["content"] for doc in context_docs[:3]])
        else:
            context = "Non sono riuscito a trovare informazioni specifiche nei documenti."
        
        # Template prompt ottimizzato per assistenza universitaria
        prompt = f"""Sei un assistente virtuale della Segreteria Studenti dell'Università di Bergamo.

CONTESTO DOCUMENTI:
{context}

DOMANDA STUDENTE: {query}

ISTRUZIONI:
- Rispondi in modo preciso basandoti sul CONTESTO fornito
- Se il contesto non contiene informazioni sufficienti, dillo chiaramente
- Mantieni un tono professionale ma cordiale
- Includi link/URL del contesto se presenti
- Se la domanda è fuori ambito, suggerisci di contattare l'ufficio competente

RISPOSTA:"""

        try:
            response = self.llm.generate(prompt)
            return {
                "response": response,
                "context_used": len(context_docs),
                "should_redirect": len(context_docs) == 0 or "non sono riuscito" in response.lower()
            }
            
        except Exception as e:
            print(f"Errore generazione: {e}")
            return {
                "response": "Mi dispiace, sto avendo difficoltà tecniche. Contatta direttamente la segreteria studenti (https://helpdesk.unibg.it/) .",
                "context_used": 0,
                "should_redirect": True
            }
    
    def chat(self, query):
        """Metodo principale per processare una query utente completa"""
        
        # Fase 1: Recupera documenti rilevanti
        docs = self.retrieve_documents(query)
        
        # Fase 2: Genera risposta contestualizzata
        result = self.generate_response(query, docs)
        
        return result

def check_requirements():
    """Verifica che tutti i componenti necessari siano configurati correttamente"""
    
    checks = []
    
    # Verifica servizio Ollama e modello Mistral
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            has_mistral = any('mistral' in model.get('name', '') for model in models)
            if has_mistral:
                checks.append("[OK] Ollama + Mistral: Pronti")
            else:
                checks.append("[WARN] Ollama attivo, Mistral mancante")
                checks.append("   → Esegui: ollama pull mistral:7b")
        else:
            checks.append("[ERROR] Ollama: Non risponde")
    except:
        checks.append("[ERROR] Ollama: Non in esecuzione")
        checks.append("   → Avvia Ollama e scarica Mistral")
    
    # Verifica database vettoriale
    if os.path.exists("vectordb") and os.listdir("vectordb"):
        checks.append("[OK] Database vettoriale: Presente")
    else:
        checks.append("[ERROR] Database vettoriale: Mancante")
        checks.append("   → Esegui: python src/creazione_vectorstore.py")
    
    # Verifica documenti estratti
    if os.path.exists("data/testi_estratti") and os.listdir("data/testi_estratti"):
        checks.append("[OK] Documenti estratti: Presenti")
    else:
        checks.append("[ERROR] Documenti estratti: Mancanti")
        checks.append("   → Esegui: python src/testi_estratti.py")
    
    for check in checks:
        print(f"  {check}")
    
    has_errors = any("[ERROR]" in check for check in checks)
    if has_errors:
        print(f"\nSistema non pronto. Risolvi gli errori sopra.")
        return False
        
    return True

def setup_chatbot():
    """Inizializza il chatbot verificando tutti i prerequisiti del sistema"""
    try:
        chatbot = ChatbotRAG()
        return chatbot
    except Exception as e:
        print(f"Impossibile inizializzare il chatbot: {e}")
        return None

def chatbot_cli():
    """Interfaccia CLI interattiva per conversazione con il chatbot"""
    
    if not check_requirements():
        return False
    
    chatbot = setup_chatbot()
    
    if not chatbot:
        print("Impossibile avviare il chatbot")
        return False
    
    print("\n" + "=" * 50)
    print("CHATBOT SEGRETERIA STUDENTI UNIBG")
    print("=" * 50)
    print("Fai una domanda sull'università!")
    print("Comandi: 'help' per esempi | 'exit' per uscire")
    print("=" * 50)
    
    while True:
        print("\n" + "-" * 30)
        try:
            domanda = input("Studente > ").strip()
        except KeyboardInterrupt:
            print("\n\nArrivederci!")
            break
        
        if domanda.lower() in ['exit', 'quit', 'bye', 'esci']:
            print("Arrivederci!")
            break
            
        elif domanda.lower() == 'help':
            show_help()
            continue
            
        elif not domanda:
            print("Scrivi una domanda per iniziare.")
            continue
        
        try:
            result = chatbot.chat(domanda)
            response = result['response']
            
            # Evidenzia URL nella risposta senza emoji
            url_pattern = r'(https?://[^\s<>"{}|\\^`\[\]]+)'
            highlighted_response = re.sub(url_pattern, r'Link: \1', response)
            
            print(f"\nChatBot: {highlighted_response}")
            
            # Mostra info aggiuntive se utili
            if result['context_used'] > 0:
                print(f"(Basato su {result['context_used']} documenti)")
            
            if result['should_redirect']:
                ticket_url = os.getenv('TICKET_URL', 'https://helpdesk.unibg.it/')
                print(f"\nPer assistenza personalizzata: {ticket_url}")
                
        except Exception as e:
            print(f"Errore nel processare la richiesta: {str(e)}")
            print("Ti consiglio di contattare direttamente la Segreteria:")
            print(f"🔗 {os.getenv('TICKET_URL', 'https://helpdesk.unibg.it/')}")
    
    return True

def show_help():
    """Mostra esempi di domande supportate dal chatbot"""
    print("\n" + "=" * 30)
    print("ESEMPI DI DOMANDE")
    print("=" * 30)
    
    esempi = [
        "Come faccio a iscrivermi agli esami?",
        "Quando devo pagare le tasse universitarie?",
        "Come richiedo un certificato di laurea?", 
        "Che documenti servono per la laurea?",
        "Quali sono i contatti della segreteria?",
        "Come funziona il servizio disabilità?",
        "Come trovo informazioni sui tirocini?",
        "Quali sono gli orari degli uffici?",
        "Come funziona l'immatricolazione?",
        "Dove trovo il piano di studi?"
    ]
    
    for i, esempio in enumerate(esempi, 1):
        print(f"  {i:2d}. {esempio}")
    
    print("\nPuoi fare domande su qualsiasi aspetto della vita universitaria!")

def show_setup_instructions():
    """Mostra istruzioni complete per configurazione iniziale del sistema"""
    print("\n" + "=" * 30)
    print("SETUP DEL SISTEMA")
    print("=" * 30)
    
    print("STEP 1 - Installa Ollama:")
    print("  - Scarica da: https://ollama.ai")
    print("  - Installa e avvia il servizio")
    print("")
    
    print("STEP 2 - Scarica il modello:")
    print("  - Esegui: ollama pull mistral:7b")
    print("")
    
    print("STEP 3 - Installa dipendenze Python:")
    print("  - Esegui: pip install -r requirements.txt")
    print("")
    
    print("STEP 4 - Prepara i dati:")
    print("  - Estrai testi: python src/testi_estratti.py")
    print("  - Crea database: python src/creazione_vectorstore.py")
    print("")
    
    print("STEP 5 - Avvia il chatbot:")
    print("  - Esegui: python main.py")

def main():
    """Funzione principale - gestisce i comandi CLI e avvia l'interfaccia appropriata"""
    print("ChatBot Segreteria Studenti - UniBg")
    print(f"Avviato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}")
    
    # Gestione argomenti da riga di comando
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            show_setup_instructions()
            return
        elif sys.argv[1] == "--check":
            print("\nVerifica sistema...")
            check_requirements()
            return
        elif sys.argv[1] == "--help":
            print("\n" + "=" * 30)
            print("COMANDI DISPONIBILI")
            print("=" * 30)
            print("  python main.py           # Avvia chatbot")
            print("  python main.py --setup   # Mostra istruzioni setup")  
            print("  python main.py --check   # Verifica sistema")
            print("  python main.py --help    # Mostra questo aiuto")
            return
    
    # Avvia l'interfaccia CLI principale
    chatbot_cli()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgramma interrotto dall'utente. Arrivederci!")
    except Exception as e:
        print(f"\nErrore critico: {e}")
        print("Verifica il setup con: python main.py --check")