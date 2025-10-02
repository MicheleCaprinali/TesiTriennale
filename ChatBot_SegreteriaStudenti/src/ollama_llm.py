"""
Modulo per gestire LLM locale con Ollama
Versione ottimizzata con prompt templates e gestione errori migliorata
✅ OTTIMIZZATO: Timeout ridotti, parametri LLM ottimizzati, validazione meno rigida
"""

import requests
import os
import logging
import time
import subprocess
from dotenv import load_dotenv
from typing import Dict, Any

# Import sicuro per prompt templates
try:
    from prompt_templates import get_optimized_prompt
    PROMPT_OPTIMIZATION = True
    print("✅ Sistema prompt ottimizzati caricato")
except ImportError as e:
    PROMPT_OPTIMIZATION = False
    print(f"⚠️ Prompt optimization non disponibile: {e}")

# Import sicuro per link enhancer
try:
    from link_enhancer import LinkEnhancer
    LINK_ENHANCEMENT_AVAILABLE = True
    print("✅ Sistema link automatico caricato")
except ImportError as e:
    LINK_ENHANCEMENT_AVAILABLE = False
    print(f"⚠️ Link enhancement non disponibile: {e}")

load_dotenv()

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaLLM:
    """
    Classe per interfacciarsi con Ollama per LLM locale
    Supporta prompt ottimizzati e gestione errori avanzata
    ✅ OTTIMIZZATO: Parametri LLM bilanciati per velocità/qualità
    """
    
    def __init__(self, base_url: str = None, model: str = None):
        """Inizializza il client LLM per comunicazione con Ollama"""
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = model or os.getenv('OLLAMA_MODEL', 'mistral:7b')
        self.temperature = float(os.getenv('TEMPERATURE', '0.1'))
        
        # Statistiche interne
        self._request_count = 0
        self._success_count = 0
        self._total_response_time = 0.0
        self._warmed_up = False  # ✅ Flag per tracking warm-up
        
        self.link_enhancement_enabled = False
        if LINK_ENHANCEMENT_AVAILABLE:
            try:
                self.link_enhancer = LinkEnhancer()
                self.link_enhancement_enabled = True
                print("🔗 Link enhancer inizializzato")
            except Exception as e:
                self.link_enhancement_enabled = False
                print(f"⚠️ Errore inizializzazione link enhancer: {e}")
            
        logger.info(f"Inizializzato OllamaLLM: {self.base_url}, modello: {self.model}")
    
    def is_running(self) -> bool:
        """Verifica se il servizio Ollama è attivo e raggiungibile"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            # Verifica se il processo è in esecuzione su Windows
            try:
                result = subprocess.run(
                    ['tasklist', '/FI', 'IMAGENAME eq ollama.exe'], 
                    capture_output=True, 
                    text=True,
                    timeout=5
                )
                return 'ollama.exe' in result.stdout
            except:
                return False
    
    def check_connection(self) -> bool:
        """Metodo di compatibilità per main.py - verifica connessione Ollama"""
        return self.is_running()
    
    def list_models(self) -> list:
        """Restituisce l'elenco dei modelli LLM disponibili in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception as e:
            logger.warning(f"Errore nel recupero modelli: {e}")
            return []
    
    def generate(self, query: str, context: str = "") -> str:
        """
        ✅ OTTIMIZZATO: Genera risposta veloce con prompt ottimizzato
        
        Args:
            query: Query ORIGINALE dell'utente (es. "Come iscrivermi agli esami?")
            context: Contesto documenti recuperati dal RAG (testo concatenato)
            
        Returns:
            str: Risposta generata o messaggio di errore
        """
        
        start_time = time.time()
        self._request_count += 1
        
        # ✅ WARM-UP: Prima richiesta richiede più tempo (caricamento modello)
        if not self._warmed_up:
            print("🔥 Caricamento modello in corso (prima richiesta più lenta)...")
            self._warmed_up = True
        
        # FASE 1: Costruzione prompt ottimizzato
        if PROMPT_OPTIMIZATION:
            try:
                # ✅ Passa query originale + context separati per categorizzazione
                final_prompt = get_optimized_prompt(query, context)
                print("🔧 Usando prompt ottimizzato")
            except Exception as e:
                print(f"⚠️ Errore prompt optimization: {e}")
                final_prompt = self._get_fallback_prompt(query, context)
        else:
            final_prompt = self._get_fallback_prompt(query, context)
            print("⚠️ Usando prompt base")
        
        # FASE 2: Configurazione parametri ottimizzati per velocità/qualità
        payload = {
            "model": self.model,
            "prompt": final_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,      # ✅ BILANCIATO: buon compromesso qualità/velocità
                "top_p": 0.85,           # ✅ BILANCIATO: tra 0.8 e 0.9
                "num_predict": 400,      # ✅ AUMENTATO da 300 (risposte complete ma non eccessive)
                "num_ctx": 2048,         # ✅ Mantenuto (efficiente)
                "repeat_penalty": 1.1,   # ✅ OK
                "top_k": 40,             # ✅ OK
                "stop": ["Human:", "Assistant:", "###"]
            }
        }
        
        # FASE 3: Sistema retry con timeout bilanciati velocità/affidabilità
        timeouts = [30, 45, 60]  # ✅ BILANCIATI: abbastanza per Mistral, non eccessivi (max 135s)
        
        for attempt, timeout in enumerate(timeouts, 1):
            try:
                print(f"🔄 Tentativo {attempt}/{len(timeouts)} (timeout: {timeout}s)")
                
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=timeout,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('response', '').strip()
                    
                    # FASE 4: Validazione e post-processing
                    processed_answer = self._process_response(answer, query)  # ✅ Usa query originale
                    
                    if self.link_enhancement_enabled and hasattr(self, 'link_enhancer') and processed_answer:
                        try:
                            category = self._determine_category(query)  # ✅ Usa query originale
                            original_links = self.link_enhancer.count_links(processed_answer)
                            processed_answer = self.link_enhancer.enhance_response(processed_answer, category)
                            new_links = self.link_enhancer.count_links(processed_answer)
                            if new_links > original_links:
                                print(f"🔗 Link aggiunti: {new_links - original_links} (totale: {new_links})")
                        except Exception as e:
                            print(f"⚠️ Errore link enhancement: {e}")

                    if self._is_valid_response(processed_answer):
                        response_time = time.time() - start_time
                        self._success_count += 1
                        self._total_response_time += response_time
                        
                        print(f"✅ Risposta generata ({len(processed_answer)} caratteri, {response_time:.1f}s)")
                        return processed_answer
                    else:
                        print(f"⚠️ Risposta inadeguata al tentativo {attempt}: {answer[:50]}...")
                        if attempt < len(timeouts):
                            continue
                
                elif response.status_code == 404:
                    return f"REDIRECT_TO_HUMAN - Modello '{self.model}' non trovato. Verifica installazione."
                
                else:
                    print(f"❌ HTTP {response.status_code} al tentativo {attempt}")
                    if attempt == len(timeouts):
                        return f"REDIRECT_TO_HUMAN - Errore server (HTTP {response.status_code})"
            
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout {timeout}s al tentativo {attempt} - il modello sta elaborando...")
                if attempt == len(timeouts):
                    return "REDIRECT_TO_HUMAN - Il sistema sta richiedendo più tempo del previsto. Riprova tra un momento o semplifica la domanda."
            
            except requests.exceptions.ConnectionError:
                print(f"🔌 Errore connessione al tentativo {attempt}")
                if attempt == len(timeouts):
                    return "REDIRECT_TO_HUMAN - Servizio Ollama non disponibile. Verifica che sia in esecuzione."
            
            except Exception as e:
                print(f"❌ Errore imprevisto al tentativo {attempt}: {str(e)}")
                if attempt == len(timeouts):
                    return f"REDIRECT_TO_HUMAN - Errore tecnico: {str(e)[:100]}"
            
            # Pausa tra tentativi
            if attempt < len(timeouts):
                print(f"⏸️ Pausa 2 secondi prima del prossimo tentativo...")
                time.sleep(2)
        
        return "REDIRECT_TO_HUMAN - Impossibile generare risposta dopo tutti i tentativi"
    
    def _get_fallback_prompt(self, query: str, context: str) -> str:
        """
        ✅ OTTIMIZZATO: Usa query invece di prompt per chiarezza
        Genera prompt di fallback quando l'ottimizzazione avanzata non è disponibile
        """
        return f"""Sei l'assistente AI della Segreteria Studenti dell'Università di Bergamo.

CONTESTO: {context}

DOMANDA STUDENTE: {query}

ISTRUZIONI:
- Rispondi in modo professionale e completo
- Usa SOLO le informazioni del contesto fornito
- Se le informazioni sono insufficienti, indica chiaramente cosa manca
- Mantieni un tono cordiale ma formale
- Struttura la risposta in modo chiaro e leggibile

RISPOSTA:"""
    
    def _process_response(self, answer: str, original_query: str) -> str:
        """
        ✅ OTTIMIZZATO: Rinominato parametro per chiarezza
        Post-elabora la risposta per migliorarne qualità e formato
        """
        
        if not answer:
            return ""
        
        # Rimuovi eventuali prefissi indesiderati
        prefixes_to_remove = [
            "RISPOSTA:", "Risposta:", "CONTESTO:", "DOMANDA:",
            "Assistant:", "AI:", "Bot:"
        ]
        
        for prefix in prefixes_to_remove:
            if answer.startswith(prefix):
                answer = answer[len(prefix):].strip()
                answer = answer[len(prefix):].strip()
        
        # Rimuovi ripetizioni eccessive
        answer = self._remove_repetitions(answer)
        
        # Assicurati che la risposta finisca con punteggiatura
        if answer and not answer.endswith(('.', '!', '?', ':')):
            answer += '.'
        
        return answer
    
    def _remove_repetitions(self, text: str) -> str:
        """Rimuove ripetizioni eccessive e ridondanze nel testo generato"""
        lines = text.split('\n')
        unique_lines = []
        seen_lines = set()
        
        for line in lines:
            line_clean = line.strip().lower()
            if line_clean and line_clean not in seen_lines:
                unique_lines.append(line)
                seen_lines.add(line_clean)
            elif not line_clean:  # Mantieni righe vuote
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)
    
    def _is_valid_response(self, answer: str) -> bool:
        """
        ✅ OTTIMIZZATO: Validazione meno rigida per ridurre retry inutili
        Valuta se la risposta generata è utile e di qualità sufficiente
        """
        
        if not answer or len(answer.strip()) < 15:  # ✅ Abbassato da 20 a 15
            return False
        
        # ✅ MODIFICATO: Pattern più specifici (evita falsi positivi)
        invalid_patterns = [
            "non riesco a rispondere",
            "non posso aiutarti con questo", 
            "non ho informazioni sufficienti per rispondere",
            "errore nella generazione della risposta", 
            "impossibile rispondere a questa specifica domanda"
        ]
        
        answer_lower = answer.lower()
        
        # ✅ OTTIMIZZATO: Scarta solo se TUTTA la risposta è chiaramente invalida
        if len(answer) < 80:  # ✅ Abbassato da 100 a 80 (più permissivo)
            # Richiede almeno 2 pattern invalidi per scartare
            invalid_count = sum(1 for pattern in invalid_patterns if pattern in answer_lower)
            if invalid_count >= 2:
                return False
        
        return True  # ✅ Accetta tutte le altre risposte
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Restituisce statistiche dettagliate sulle performance del sistema LLM"""
        try:
            # Test di velocità
            start_time = time.time()
            
            test_payload = {
                "model": self.model,
                "prompt": "Test: rispondi solo 'Sistema funzionante'",
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 10,
                    "num_ctx": 256
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=test_payload,
                timeout=15
            )
            
            response_time = time.time() - start_time
            
            # Statistiche cumulative
            avg_response_time = (self._total_response_time / self._success_count 
                               if self._success_count > 0 else 0)
            success_rate = (self._success_count / self._request_count * 100 
                          if self._request_count > 0 else 0)
            
            if response.status_code == 200:
                return {
                    "healthy": True,
                    "current_response_time": round(response_time, 2),
                    "avg_response_time": round(avg_response_time, 2),
                    "success_rate": round(success_rate, 1),
                    "total_requests": self._request_count,
                    "model": self.model,
                    "performance": self._classify_performance(response_time)
                }
            else:
                return {
                    "healthy": False,
                    "error": f"HTTP {response.status_code}",
                    "response_time": response_time
                }
        
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e),
                "performance": "Non disponibile"
            }
    
    def _classify_performance(self, response_time: float) -> str:
        """Classifica le performance in base ai tempi di risposta registrati"""
        if response_time < 5:
            return "Eccellente"
        elif response_time < 15:
            return "Buono"
        elif response_time < 30:
            return "Accettabile"
        else:
            return "Lento"
    
    def health_check(self) -> Dict[str, Any]:
        """Esegue verifica completa dello stato del servizio Ollama"""
        try:
            # Test connessione
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code != 200:
                return {"healthy": False, "error": f"HTTP {response.status_code}"}
            
            # Test modelli disponibili
            models = self.list_models()
            if not models:
                return {"healthy": False, "error": "Nessun modello disponibile"}
            
            # Test se il modello corrente è disponibile
            current_model_available = any(self.model in model for model in models)
            if not current_model_available:
                return {
                    "healthy": False,
                    "error": f"Modello '{self.model}' non disponibile",
                    "available_models": models
                }
            
            return {
                "healthy": True,
                "base_url": self.base_url,
                "model": self.model,
                "available_models": models,
                "optimization_enabled": PROMPT_OPTIMIZATION
            }
        
        except requests.exceptions.Timeout:
            return {"healthy": False, "error": "Timeout nella connessione"}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Scarica e installa un modello specifico da Ollama"""
        try:
            print(f"📥 Scaricamento modello {model_name}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=1800  # 30 minuti per il download
            )
            return {
                "success": response.status_code == 200,
                "message": response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_model(self, model_name: str) -> Dict[str, Any]:
        """Rimuove un modello specifico dall'installazione Ollama"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name},
                timeout=30
            )
            return {
                "success": response.status_code == 200,
                "message": "Modello eliminato con successo" if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_model_info(self, model_name: str = None) -> Dict[str, Any]:
        """Restituisce informazioni dettagliate su un modello specifico"""
        target_model = model_name or self.model
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": target_model},
                timeout=15
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "error": f"Modello {target_model} non trovato"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def _determine_category(self, query: str) -> str:
        """
        ✅ OTTIMIZZATO: Usa query invece di prompt
        Analizza la domanda per determinare la categoria più appropriata
        """
        query_lower = query.lower()
    
        if any(word in query_lower for word in ['iscriver', 'esam', 'prenotare']):
            return 'iscrizioni_esami'
        elif any(word in query_lower for word in ['tasse', 'pagare', 'pagament']):
            return 'tasse_pagamenti'  
        elif any(word in query_lower for word in ['certificat', 'document']):
            return 'certificati_documenti'
        elif any(word in query_lower for word in ['orari', 'contatt', 'telefono']):
            return 'orari_contatti'
        elif any(word in query_lower for word in ['servizi', 'agevolazioni', 'borse']):
            return 'servizi_studenti'
    
        return 'generic'    



# Funzioni helper per compatibilità
def test_ollama_connection() -> bool:
    """Funzione helper per testare rapidamente la connessione a Ollama"""
    try:
        llm = OllamaLLM()
        return llm.check_connection()
    except:
        return False
    

if __name__ == "__main__":
    # Test del modulo
    print("Test OllamaLLM")
    llm = OllamaLLM()
    
    print(f"Connessione: {'OK' if llm.check_connection() else 'ERRORE'}")
    print(f"Modelli: {llm.list_models()}")
    
    # Test generazione
    test_query = "Come mi iscrivo agli esami?"
    test_context = "Per iscriversi agli esami bisogna accedere al portale studenti..."
    result = llm.generate(test_query, test_context)
    print(f"Test generazione: {result[:100]}...")
    
    # Statistiche
    stats = llm.get_performance_stats()
    print(f"Performance: {stats}")

