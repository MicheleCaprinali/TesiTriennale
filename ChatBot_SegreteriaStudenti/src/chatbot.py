from dotenv import load_dotenv
load_dotenv()

import os
import sys
from pathlib import Path

# Aggiungi il path src per import relativi
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from local_embeddings import LocalEmbeddings
from ollama_llm import OllamaLLM
from create_vectorstore import search_vectorstore

# Importa sistema di risposte rapide
try:
    from quick_responses import get_quick_response
except ImportError:
    def get_quick_response(query):
        return None

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
                k=self.retrieval_k,
                embedder=self.embedder  # Passa l'embedder esistente
            )
            
            # Estrai i documenti più rilevanti
            if results and 'documents' in results and results['documents']:
                documents = results['documents'][0]  # Prima lista di risultati
                context = "\n\n".join(documents)
                return context
            
            return ""
            
        except Exception as e:
            print(f"⚠️ Errore nel recupero contesto: {str(e)}")
            return ""
    
    def validate_and_clean_response(self, response: str, context: str) -> str:
        """Valida e pulisce la risposta rimuovendo link non validi"""
        import re
        
        # Trova tutti i link nella risposta
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        response_urls = re.findall(url_pattern, response)
        
        # Trova tutti i link nel contesto
        context_urls = re.findall(url_pattern, context)
        
        # Domini ufficiali UniBG da mantenere sempre
        unibg_domains = [
            'www.unibg.it',
            'unibg.it'
        ]
        
        # Rimuovi link che non sono nel contesto originale, eccetto quelli ufficiali UniBG
        for url in response_urls:
            is_official_unibg = any(domain in url for domain in unibg_domains)
            
            if url not in context_urls and not is_official_unibg:
                response = response.replace(url, "[LINK RIMOSSO - contatta la segreteria per informazioni specifiche]")
                print(f"⚠️ Rimosso link non valido: {url}")
            elif is_official_unibg and url not in context_urls:
                corrected_url = url
                
                # Rimuovi doppi slash nel percorso (ma non in https://)
                if '//' in url and not url.startswith('https://'):
                    parts = url.split('://', 1)
                    if len(parts) == 2:
                        protocol, rest = parts
                        rest = rest.replace('//', '/')
                        corrected_url = f"{protocol}://{rest}"
                elif '//' in url.replace('https://', '', 1):
                    # Doppi slash dopo il dominio
                    corrected_url = url.replace('https://', '', 1).replace('//', '/')
                    corrected_url = f"https://{corrected_url}"
                
                if corrected_url != url:
                    response = response.replace(url, corrected_url)
                    print(f"Corretto link UniBG: {url} → {corrected_url}")
        
        return response

    def generate_response(self, query: str, context: str) -> str:
        """Genera risposta usando il LLM locale"""
        try:
            response = self.llm.generate(query, context)
            cleaned_response = self.validate_and_clean_response(response, context)
            return cleaned_response
        except Exception as e:
            return f"Errore nella generazione della risposta: {str(e)}"
    
    def chat(self, query: str) -> dict:
        """Pipeline completa RAG: Retrieve + Generate con sistema di fallback"""
        
        # Prima verifica se c'è una risposta rapida disponibile
        quick_response = get_quick_response(query)
        if quick_response:
            print("✅ Utilizzando risposta rapida ottimizzata")
            return {
                "response": quick_response,
                "context_found": True,
                "should_redirect": False,
                "context": "Risposta rapida dal database ottimizzato"
            }
        
        print("Ricerca documenti pertinenti...")
        context = self.retrieve_context(query)
        
        if not context or len(context.strip()) < 50:
            return {
                "response": "Mi dispiace, non ho trovato informazioni pertinenti alla tua domanda nei documenti disponibili. Ti suggerisco di contattare direttamente la segreteria per un'assistenza personalizzata.",
                "context_found": False,
                "should_redirect": True
            }
        
        print("Generazione risposta...")
        response = self.generate_response(query, context)
        
        # Se la risposta indica timeout, prova una risposta basata solo sul contesto
        if "troppo tempo" in response or "timeout" in response.lower():
            # Genera una risposta di base basata sul contesto
            import re
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            context_links = re.findall(url_pattern, context)
            
            if context_links:
                fallback_response = f"Ho trovato informazioni pertinenti alla tua domanda. Ecco i link utili:\n\n"
                for i, link in enumerate(context_links[:3], 1):  # Massimo 3 link
                    fallback_response += f"🔗 **Link {i}:** {link}\n"
                
                fallback_response += "\nPer maggiori dettagli contatta la segreteria studenti."
                
                return {
                    "response": fallback_response,
                    "context_found": True,
                    "should_redirect": False,
                    "context": context[:500] + "..." if len(context) > 500 else context
                }
        
        should_redirect = self._should_redirect_to_ticket(response, query)
        
        if should_redirect and "contatt" not in response.lower():
            response += "\n\nPer informazioni più specifiche o assistenza personalizzata, contatta la segreteria studenti:"
        
        return {
            "response": response,
            "context_found": True,
            "should_redirect": should_redirect,
            "context": context[:500] + "..." if len(context) > 500 else context
        }
    
    def _should_redirect_to_ticket(self, response: str, query: str) -> bool:
        """Determina se rimandare l'utente al sistema di ticketing"""
        
        # Frasi che indicano bassa confidenza o necessità di assistenza personalizzata
        redirect_indicators = [
            "non ho informazioni sufficienti",
            "non sono sicuro",
            "non posso fornire",
            "non so",
            "mi dispiace, non",
            "errore nella",
            "contatta la segreteria",
            "rivolgiti alla segreteria",
            "informazioni specifiche",
            "caso particolare",
            "situazione personale"
        ]
        
        # Verifica lunghezza risposta (troppo corta = poco informativa)
        if len(response.strip()) < 30:
            return True
        
        # Verifica frasi di bassa confidenza
        response_lower = response.lower()
        for indicator in redirect_indicators:
            if indicator in response_lower:
                return True
        
        # Domande che richiedono accesso a dati personali/sistemi universitari
        personal_query_patterns = [
            # Carriera personale
            "mia carriera", "miei esami", "mio piano", "miei crediti", "mia media",
            "mia situazione", "mio libretto", "mia iscrizione", "mio stato",
            
            # Richieste specifiche/personali
            "posso", "devo", "quando devo", "come faccio a", "il mio caso",
            "la mia", "il mio", "personale", "specifica", "particolare",
            
            # Procedure che richiedono identificazione
            "iscrivere esame", "presentare domanda", "richiedere certificato",
            "pagare tassa", "modificare piano", "cambiare corso"
        ]
        
        query_lower = query.lower()
        for pattern in personal_query_patterns:
            if pattern in query_lower:
                return True
        
        # Se la risposta è generica e la domanda sembra specifica
        generic_response_keywords = ["in generale", "solitamente", "di solito", "normalmente"]
        specific_question_keywords = ["quando", "come", "dove", "perché", "cosa devo"]
        
        has_generic_response = any(keyword in response_lower for keyword in generic_response_keywords)
        has_specific_question = any(keyword in query_lower for keyword in specific_question_keywords)
        
        if has_generic_response and has_specific_question:
            return True
        
        return False

def setup_chatbot():
    """Setup completo del chatbot"""
    print("Setup Chatbot RAG Gratuito")
    print("=" * 40)
    
    if not os.path.exists("extracted_text"):
        print("❌ Cartella 'extracted_text' non trovata!")
        print("Esegui prima 'python src/extract_and_save.py'")
        return None
    
    if not os.path.exists("vectordb"):
        print("❌ Vectorstore non trovato!")
        print("Esegui prima 'python src/create_vectorstore.py'")
        return None
    
    llm = OllamaLLM()
    if not llm.is_running():
        print("❌ Ollama non è in esecuzione!")
        print("Avvia Ollama con: 'ollama serve'")
        print("Scarica Mistral con: 'ollama pull mistral:7b'")
        return None
    
    chatbot = ChatbotRAG()
    return chatbot

if __name__ == "__main__":
    chatbot = setup_chatbot()
    
    if not chatbot:
        print("❌ Setup fallito!")
        exit(1)
    
    print("\n" + "=" * 50)
    print("CHATBOT SEGRETERIA STUDENTI UNIBG")
    print("=" * 50)
    print("Scrivi una domanda o 'exit' per uscire")
    print("=" * 50)
    
    while True:
        print("\n" + "-" * 30)
        query = input("Studente > ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Arrivederci!")
            break
        
        if not query:
            continue
        
        result = chatbot.chat(query)
        
        if result['should_redirect']:
            print("Assistente: " + result['response'])
            print(f"\nPer assistenza personalizzata:")
            print(f"{os.getenv('TICKET_URL', 'https://www.unibg.it')}")
        else:
            print("Assistente: " + result['response'])