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
        self.retrieval_k = int(os.getenv('RETRIEVAL_K', 10))  # Aumentato per migliorare recall
        
        print("✅ Chatbot RAG gratuito inizializzato!")
    
    def search_by_keywords_simple(self, query: str) -> list:
        """Ricerca semplificata per parole chiave specifiche"""
        try:
            import chromadb
            client = chromadb.PersistentClient(path=self.vectordb_path)
            collection = client.get_collection(os.getenv('VECTORDB_COLLECTION', 'unibg_docs'))
            
            # Ottieni tutti i documenti (cache questa operazione in futuro)
            all_results = collection.get()
            
            # Mappa diretta per termini critici
            keyword_patterns = {
                'alloggi': 'vivere-unibg/spazi-e-servizi/alloggi',
                'residenze': 'residenze universitarie',
                'mensa': 'servizio-ristorazione',
                'borse': 'borse-studio'
            }
            
            # Cerca pattern specifici
            matching_docs = []
            query_lower = query.lower()
            
            for doc in all_results['documents']:
                for term, pattern in keyword_patterns.items():
                    if term in query_lower and pattern in doc.lower():
                        matching_docs.append(doc)
                        break  # Un documento per query
                if len(matching_docs) >= 1:  # Trova solo il primo documento rilevante
                    break
            
            return matching_docs
            
        except Exception as e:
            print(f"⚠️ Errore ricerca keyword: {str(e)}")
            return []
    
    def retrieve_context(self, query: str) -> str:
        """Recupera contesto pertinente dal vectorstore con ricerca ibrida semplificata"""
        try:
            # 1. Ricerca vettoriale semantica (ridotta per velocità)
            results = search_vectorstore(
                query, 
                persist_dir=self.vectordb_path, 
                k=2,  # Drasticamente ridotto per database grande
                embedder=self.embedder
            )
            
            context_parts = []
            
            # Estrai documenti dalla ricerca vettoriale
            if results and 'documents' in results and results['documents']:
                documents = results['documents'][0]
                context_parts.extend(documents)
                print(f"📄 Trovati {len(documents)} documenti")
            
            # 2. Ricerca keyword SOLO per termini critici
            critical_terms = ['alloggi', 'residenze universitarie', 'mensa', 'borse di studio']
            if any(term in query.lower() for term in critical_terms):
                keyword_results = self.search_by_keywords_simple(query)
                if keyword_results:
                    context_parts.extend(keyword_results[:2])  # Max 2 documenti aggiuntivi
                    print(f"🔍 +{len(keyword_results[:2])} documenti keyword")
            
            # Limita il contesto per velocità
            context = "\n\n".join(context_parts[:10])  # Max 10 documenti
            
            return context
            
        except Exception as e:
            print(f"⚠️ Errore recupero contesto: {str(e)}")
            return ""
    
    def validate_and_clean_response(self, response: str, context: str) -> str:
        """Valida e pulisce la risposta - VERSIONE INTELLIGENTE"""
        import re
        
        # Trova tutti i link nella risposta (pattern più preciso)
        url_pattern = r'https?://[^\s<>"\[\](){}|\\^`]+'
        response_urls = re.findall(url_pattern, response)
        
        # Trova tutti i link nel contesto (pulendo i punti finali)
        context_urls_raw = re.findall(url_pattern, context)
        context_urls = [url.rstrip('.').rstrip(',').rstrip(';') for url in context_urls_raw]
        
        print(f"🔍 Link nel contesto (puliti): {context_urls}")
        print(f"🔍 Link nella risposta: {response_urls}")
        
        # VALIDAZIONE INTELLIGENTE: confronta URL normalizzati
        for url in response_urls:
            url_clean = url.rstrip('.').rstrip(',').rstrip(';')
            
            # Verifica se il link pulito è presente nel contesto pulito
            if url_clean in context_urls:
                print(f"✅ Link valido mantenuto: {url}")
            else:
                # Verifica anche match parziali per domini UniBG
                is_valid_partial = False
                if 'unibg.it' in url_clean:
                    for context_url in context_urls:
                        # Confronto intelligente per URL simili
                        if context_url.replace('www.', '').replace('https://', '') in url_clean.replace('www.', '').replace('https://', '') or \
                           url_clean.replace('www.', '').replace('https://', '') in context_url.replace('www.', '').replace('https://', ''):
                            print(f"✅ Link valido (match parziale): {url}")
                            is_valid_partial = True
                            break
                
                if not is_valid_partial:
                    response = response.replace(url, "[INFORMAZIONI DISPONIBILI PRESSO LA SEGRETERIA]")
                    print(f"⚠️ Rimosso link non valido: {url}")
        
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
            print(f"{os.getenv('TICKET_URL', 'https://helpdesk.unibg.it/')}")
        else:
            print("Assistente: " + result['response'])