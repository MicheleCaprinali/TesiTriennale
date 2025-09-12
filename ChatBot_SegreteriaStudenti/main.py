#!/usr/bin/env python3
"""
ChatBot Segreteria Studenti - Tesi Triennale Ingegneria Informatica
Sistema per rispondere automaticamente alle domande degli studenti universitari

Tecnologie utilizzate:
- Sentence Transformers (all-MiniLM-L6-v2) per embedding
- ChromaDB per vector store
- Ollama + Mistral 7B per LLM locale
- RAG (Retrieval-Augmented Generation)
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

# Import con gestione errori
try:
    from local_embeddings import LocalEmbeddings
    from creazione_vectorstore import search_vectorstore, crea_vectorstore_free
    from ollama_llm import OllamaLLM
    from dividi_chunks import split_text_in_chunks
except ImportError as e:
    print(f"❌ Errore import moduli: {e}")
    print("Verifica che tutti i file siano presenti in src/")
    print("Esegui: pip install -r requirements.txt")
    sys.exit(1)

class ChatbotRAG:
    """Classe principale del chatbot RAG"""
    
    def __init__(self):
        """Inizializza i componenti del chatbot"""
        print("🤖 Inizializzazione ChatBot RAG...")
        
        try:
            # Inizializza embedding
            self.embedder = LocalEmbeddings()
            print("✅ Embeddings caricati")
            
            # Inizializza LLM
            self.llm = OllamaLLM()
            print("✅ LLM Ollama configurato")
            
            # Verifica connessione Ollama
            if not self.llm.check_connection():
                raise Exception("Ollama non raggiungibile")
            
            print("✅ ChatBot pronto!")
            
        except Exception as e:
            print(f"❌ Errore inizializzazione: {e}")
            raise
    
    def retrieve_documents(self, query, k=5):
        """Recupera documenti rilevanti dal vector store"""
        try:
            results = search_vectorstore(query, k=k, embedder=self.embedder)
            
            if not results["documents"] or not results["documents"][0]:
                return []
            
            # Formatta i documenti recuperati
            docs = []
            for doc, distance in zip(results["documents"][0], results["distances"][0]):
                docs.append({
                    "content": doc,
                    "score": distance
                })
            
            return docs
            
        except Exception as e:
            print(f"⚠️ Errore nel retrieval: {e}")
            return []
    
    def generate_response(self, query, context_docs):
        """Genera risposta usando LLM con contesto"""
        
        # Costruisci il contesto
        if context_docs:
            context = "\n\n".join([doc["content"] for doc in context_docs[:3]])
        else:
            context = "Non sono riuscito a trovare informazioni specifiche nei documenti."
        
        # Prompt template
        prompt = f"""Sei un assistente virtuale della Segreteria Studenti dell'Università di Bergamo.

CONTESTO DOCUMENTI:
{context}

DOMANDA STUDENTE: {query}

ISTRUZIONI:
- Rispondi in modo preciso e utile basandoti sul CONTESTO fornito
- Se il contesto non contiene informazioni sufficienti, dillo chiaramente
- Mantieni un tono professionale ma cordiale
- Se ci sono link/URL nel contesto, includili nella risposta
- Se la domanda non è chiara o troppo generica, chiedi maggiori dettagli
- Se la domanda è fuori dal tuo ambito (segreteria studenti), suggerisci di contattare l'ufficio competente

RISPOSTA:"""

        try:
            response = self.llm.generate(prompt)
            return {
                "response": response,
                "context_used": len(context_docs),
                "should_redirect": len(context_docs) == 0 or "non sono riuscito" in response.lower()
            }
            
        except Exception as e:
            print(f"⚠️ Errore generazione risposta: {e}")
            return {
                "response": "Mi dispiace, sto avendo difficoltà tecniche. Ti consiglio di contattare direttamente la segreteria studenti.",
                "context_used": 0,
                "should_redirect": True
            }
    
    def chat(self, query):
        """Metodo principale per gestire una query"""
        print(f"🔍 Cercando informazioni per: '{query}'")
        
        # Recupera documenti
        docs = self.retrieve_documents(query)
        print(f"📚 Trovati {len(docs)} documenti rilevanti")
        
        # Genera risposta
        result = self.generate_response(query, docs)
        
        return result

def check_requirements():
    """Verifica requisiti minimi per il funzionamento"""
    print("🔍 Verifica sistema...")
    
    checks = []
    
    # Verifica Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            has_mistral = any('mistral' in model.get('name', '') for model in models)
            if has_mistral:
                checks.append("✅ Ollama + Mistral: Pronti")
            else:
                checks.append("⚠️ Ollama: Attivo, ma Mistral mancante")
                checks.append("   → Esegui: ollama pull mistral:7b")
        else:
            checks.append("❌ Ollama: Non risponde")
    except:
        checks.append("❌ Ollama: Non in esecuzione")
        checks.append("   → Avvia Ollama e scarica Mistral")
    
    # Verifica vectorstore
    if os.path.exists("vectordb") and os.listdir("vectordb"):
        checks.append("✅ Database vettoriale: Presente")
    else:
        checks.append("❌ Database vettoriale: Mancante")
        checks.append("   → Esegui: python src/creazione_vectorstore.py")
    
    # Verifica documenti estratti
    if os.path.exists("data/testi_estratti") and os.listdir("data/testi_estratti"):
        checks.append("✅ Documenti estratti: Presenti")
    else:
        checks.append("❌ Documenti estratti: Mancanti")
        checks.append("   → Esegui: python src/testi_estratti.py")
    
    for check in checks:
        print(f"  {check}")
    
    has_errors = any("❌" in check for check in checks)
    if has_errors:
        print(f"\n⚠️ Sistema non pronto. Risolvi gli errori sopra.")
        return False
        
    return True

def setup_chatbot():
    """Inizializza il chatbot con tutti i controlli"""
    try:
        chatbot = ChatbotRAG()
        return chatbot
    except Exception as e:
        print(f"❌ Impossibile inizializzare il chatbot: {e}")
        return None

def chatbot_cli():
    """Interfaccia a riga di comando per il chatbot"""
    
    if not check_requirements():
        return False
    
    print("\n🤖 Avvio ChatBot...")
    chatbot = setup_chatbot()
    
    if not chatbot:
        print("❌ Impossibile avviare il chatbot")
        return False
    
    print("\n" + "=" * 60)
    print("🎓 CHATBOT SEGRETERIA STUDENTI UNIBG")
    print("=" * 60)
    print("Fai una domanda sull'università!")
    print("Comandi: 'help' per esempi | 'exit' per uscire")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 40)
        try:
            domanda = input("🧑‍🎓 Studente > ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Arrivederci!")
            break
        
        if domanda.lower() in ['exit', 'quit', 'bye', 'esci']:
            print("👋 Arrivederci!")
            break
            
        elif domanda.lower() == 'help':
            show_help()
            continue
            
        elif not domanda:
            print("💬 Scrivi una domanda per iniziare.")
            continue
        
        try:
            print("🔄 Elaborazione...")
            result = chatbot.chat(domanda)
            response = result['response']
            
            # Evidenzia URL nella risposta
            url_pattern = r'(https?://[^\s<>"{}|\\^`\[\]]+)'
            highlighted_response = re.sub(url_pattern, r'🔗 \1', response)
            
            print(f"\n🤖 ChatBot: {highlighted_response}")
            
            # Info aggiuntive
            if result['context_used'] > 0:
                print(f"📊 (Basato su {result['context_used']} documenti)")
            
            if result['should_redirect']:
                ticket_url = os.getenv('TICKET_URL', 'https://helpdesk.unibg.it/')
                print(f"\n💡 Per assistenza personalizzata: 🔗 {ticket_url}")
                
        except Exception as e:
            print(f"❌ Errore nel processare la richiesta: {str(e)}")
            print("📞 Ti consiglio di contattare direttamente la Segreteria:")
            print(f"🔗 {os.getenv('TICKET_URL', 'https://helpdesk.unibg.it/')}")
    
    return True

def show_help():
    """Mostra esempi di domande che il chatbot può gestire"""
    print("\n" + "=" * 50)
    print("📚 ESEMPI DI DOMANDE")
    print("=" * 50)
    
    esempi = [
        "📝 Come faccio a iscrivermi agli esami?",
        "💰 Quando devo pagare le tasse universitarie?",
        "📄 Come richiedo un certificato di laurea?",
        "🎓 Che documenti servono per la laurea?",
        "📞 Quali sono i contatti della segreteria?",
        "♿ Come funziona il servizio disabilità?",
        "💼 Come trovo informazioni sui tirocini?",
        "🏢 Quali sono gli orari degli uffici?",
        "📋 Come funziona l'immatricolazione?",
        "📚 Dove trovo il piano di studi?"
    ]
    
    for esempio in esempi:
        print(f"  • {esempio}")
    
    print("\n💡 Puoi fare domande su qualsiasi aspetto della vita universitaria!")

def show_setup_instructions():
    """Mostra istruzioni per il setup iniziale"""
    print("\n" + "=" * 50)
    print("🛠️ SETUP DEL SISTEMA")
    print("=" * 50)
    
    print("STEP 1 - Installa Ollama:")
    print("  • Scarica da: https://ollama.ai")
    print("  • Installa e avvia il servizio")
    print("")
    
    print("STEP 2 - Scarica il modello:")
    print("  • Esegui: ollama pull mistral:7b")
    print("")
    
    print("STEP 3 - Installa dipendenze Python:")
    print("  • Esegui: pip install -r requirements.txt")
    print("")
    
    print("STEP 4 - Prepara i dati:")
    print("  • Estrai testi: python src/testi_estratti.py")
    print("  • Crea database: python src/creazione_vectorstore.py")
    print("")
    
    print("STEP 5 - Avvia il chatbot:")
    print("  • Esegui: python main.py")

def main():
    """Funzione principale"""
    print("🎓 ChatBot Segreteria Studenti - UniBg")
    print(f"📅 Avviato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            show_setup_instructions()
            return
        elif sys.argv[1] == "--check":
            check_requirements()
            return
        elif sys.argv[1] == "--help":
            print("\n" + "=" * 40)
            print("📖 COMANDI DISPONIBILI")
            print("=" * 40)
            print("  python main.py           # Avvia chatbot")
            print("  python main.py --setup   # Mostra istruzioni setup")  
            print("  python main.py --check   # Verifica sistema")
            print("  python main.py --help    # Mostra questo aiuto")
            return
    
    # Avvia l'interfaccia CLI
    chatbot_cli()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programma interrotto dall'utente. Arrivederci!")
    except Exception as e:
        print(f"\n❌ Errore critico: {e}")
        print("🔧 Verifica il setup con: python main.py --check")