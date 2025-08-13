from dotenv import load_dotenv
load_dotenv()

import os
from local_embeddings import LocalEmbeddings
from ollama_llm import OllamaLLM
from create_vectorstore import search_vectorstore

class ChatbotRAG:
    """
    Chatbot RAG completamente gratuito usando:
    - Sentence Transformers per embedding
    - ChromaDB per vector store
    - Ollama + Mistral per LLM
    """
    
    def __init__(self, vectordb_path="vectordb"):
        self.vectordb_path = vectordb_path
        self.embedder = LocalEmbeddings()
        self.llm = OllamaLLM()
        self.retrieval_k = int(os.getenv('RETRIEVAL_K', 5))
        
        print("✅ Chatbot RAG gratuito inizializzato!")
    
    def retrieve_context(self, query: str) -> str:
        """Recupera contesto pertinente dal vectorstore"""
        try:
            results = search_vectorstore(
                query, 
                persist_dir=self.vectordb_path, 
                k=self.retrieval_k
            )
            
            # Estrai i documenti più rilevanti
            if results and 'documents' in results and results['documents']:
                documents = results['documents'][0]  # Prima lista di risultati
                context = "\n\n".join(documents)
                return context
            
            return ""
            
        except Exception as e:
            print(f"⚠️  Errore nel recupero contesto: {str(e)}")
            return ""
    
    def generate_response(self, query: str, context: str) -> str:
        """Genera risposta usando il LLM locale"""
        try:
            response = self.llm.generate(query, context)
            return response
        except Exception as e:
            return f"Errore nella generazione della risposta: {str(e)}"
    
    def chat(self, query: str) -> dict:
        """Pipeline completa RAG: Retrieve + Generate"""
        
        # Step 1: Recupera contesto pertinente
        print("🔍 Ricerca documenti pertinenti...")
        context = self.retrieve_context(query)
        
        if not context:
            return {
                "response": "Mi dispiace, non ho trovato informazioni pertinenti alla tua domanda.",
                "context_found": False,
                "should_redirect": True
            }
        
        # Step 2: Genera risposta
        print("🧠 Generazione risposta...")
        response = self.generate_response(query, context)
        
        # Step 3: Valuta se rimandare al ticket
        should_redirect = self._should_redirect_to_ticket(response, query)
        
        return {
            "response": response,
            "context_found": True,
            "should_redirect": should_redirect,
            "context": context[:500] + "..." if len(context) > 500 else context
        }
    
    def _should_redirect_to_ticket(self, response: str, query: str) -> bool:
        """Determina se rimandare l'utente al sistema di ticketing"""
        
        # Frasi che indicano bassa confidenza
        low_confidence_phrases = [
            "non sono sicuro",
            "non posso fornire",
            "non ho informazioni sufficienti",
            "non so",
            "mi dispiace, non",
            "errore nella"
        ]
        
        # Verifica lunghezza risposta (troppo corta = poco informativa)
        if len(response.strip()) < 50:
            return True
        
        # Verifica frasi di bassa confidenza
        response_lower = response.lower()
        for phrase in low_confidence_phrases:
            if phrase in response_lower:
                return True
        
        # Domande che richiedono dati personali/specifici
        personal_keywords = [
            "mia carriera", "miei esami", "mio piano", "miei crediti", 
            "mia situazione", "personale", "specifica situazione",
            "caso particolare", "mia iscrizione"
        ]
        
        query_lower = query.lower()
        for keyword in personal_keywords:
            if keyword in query_lower:
                return True
        
        return False

def setup_chatbot():
    """Setup completo del chatbot"""
    print("🚀 Setup Chatbot RAG Gratuito")
    print("=" * 40)
    
    # Verifica che esistano i file estratti
    if not os.path.exists("extracted_text"):
        print("❌ Cartella 'extracted_text' non trovata!")
        print("💡 Esegui prima 'python src/extract_and_save.py'")
        return None
    
    # Verifica che esista il vectorstore
    if not os.path.exists("vectordb"):
        print("❌ Vectorstore non trovato!")
        print("💡 Esegui prima 'python src/create_vectorstore.py'")
        return None
    
    # Verifica Ollama
    llm = OllamaLLM()
    if not llm.is_running():
        print("❌ Ollama non è in esecuzione!")
        print("💡 Avvia Ollama con: 'ollama serve'")
        print("💡 Scarica Mistral con: 'ollama pull mistral:7b'")
        return None
    
    # Crea chatbot
    chatbot = ChatbotRAG()
    return chatbot

if __name__ == "__main__":
    # Interfaccia CLI per test
    chatbot = setup_chatbot()
    
    if not chatbot:
        print("❌ Setup fallito!")
        exit(1)
    
    print("\n" + "=" * 60)
    print("🎓 CHATBOT SEGRETERIA STUDENTI UNIBG - VERSIONE GRATUITA")
    print("=" * 60)
    print("💡 Basato su Mistral 7B + Sentence Transformers + ChromaDB")
    print("📝 Scrivi una domanda o 'exit' per uscire")
    print("🎫 Link ticket: " + os.getenv('TICKET_URL', 'https://www.unibg.it'))
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 40)
        query = input("👤 Studente > ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("👋 Arrivederci! Buono studio!")
            break
        
        if not query:
            continue
        
        # Elabora la domanda
        result = chatbot.chat(query)
        
        # Mostra la risposta
        if result['should_redirect']:
            print("🤖 " + result['response'])
            print(f"\n🎫 Per assistenza personalizzata, apri un ticket:")
            print(f"🌐 {os.getenv('TICKET_URL', 'https://www.unibg.it')}")
        else:
            print("🤖 " + result['response'])
        
        # Debug info (opzionale)
        if os.getenv('DEBUG', '').lower() == 'true':
            print(f"\n� Debug - Contesto trovato: {result['context_found']}")
            print(f"🔍 Debug - Redirect suggerito: {result['should_redirect']}")
            if result.get('context'):
                print(f"🔍 Debug - Contesto: {result['context'][:200]}...")
