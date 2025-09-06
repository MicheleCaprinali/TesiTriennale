"""
Modulo per gestire LLM locale con Ollama
"""

import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class OllamaLLM:
    """
    Classe per interfacciarsi con Ollama per LLM locale
    """
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = model or os.getenv('OLLAMA_MODEL', 'mistral:7b')
        self.temperature = float(os.getenv('TEMPERATURE', 0.1))
        
    def is_running(self) -> bool:
        """Verifica se Ollama è in esecuzione"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            # Verifica se il processo è in esecuzione su Windows
            import subprocess
            try:
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ollama.exe'], 
                                      capture_output=True, text=True)
                return 'ollama.exe' in result.stdout
            except:
                return False
    
    def list_models(self) -> list:
        """Lista i modelli disponibili in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def generate(self, prompt: str, context: str = "") -> str:
        """Genera risposta con sistema di retry ottimizzato e timeout adattivi"""
        
        # Prompt ottimizzato per performance e qualità
        final_prompt = f"""Sei l'assistente AI della Segreteria UniBg. Rispondi in italiano, professionale e completo.

REGOLE:
- Usa solo informazioni presenti nel contesto fornito.
- Se non ci sono informazioni sufficienti, rispondi: "Non ho informazioni sufficienti".
- Mantieni i link esattamente come nel contesto, senza troncarli.
- Non troncare frasi o link. Fornisci risposte complete.
- Fornisci esempi concreti se utili.

CONTESTO: {context[:3000]}

DOMANDA: {prompt}

RISPOSTA:"""
        
        # Parametri ottimizzati per velocità e qualità
        payload = {
            "model": self.model,
            "prompt": final_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.8,          
                "num_predict": 450,     # Ridotto per maggiore velocità
                "num_ctx": 1024,       # Ottimale per performance
                "repeat_penalty": 1.1,
                "top_k": 20,
            }
        }
        
        # Sistema retry con timeout adattivi ottimizzati
        timeouts = [30, 40, 50]  # Timeout più generosi per ridurre fallimenti
        
        for attempt, timeout in enumerate(timeouts, 1):
            try:
                print(f"🔄 Tentativo {attempt}/{len(timeouts)} (timeout: {timeout}s)")
                
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('response', '').strip()
                    
                    # Validazione risposta migliorata
                    if answer and len(answer) > 15 and not answer.startswith('Non ho'):
                        print(f"✅ Risposta generata ({len(answer)} caratteri, tentativo {attempt})")
                        return answer
                    elif answer and 'Non ho informazioni' in answer:
                        print(f"⚠️ Informazioni insufficienti nel database")
                        return answer
                    else:
                        print(f"⚠️ Risposta inadeguata al tentativo {attempt}")
                        if attempt < len(timeouts):
                            continue
                            
                else:
                    print(f"❌ HTTP {response.status_code} al tentativo {attempt}")
                    if attempt == len(timeouts):
                        return f"REDIRECT_TO_HUMAN - Errore server (HTTP {response.status_code})"
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout {timeout}s al tentativo {attempt}")
                if attempt == len(timeouts):
                    return "REDIRECT_TO_HUMAN - Sistema sovraccarico, riprova tra qualche secondo"
                    
            except requests.exceptions.ConnectionError:
                print(f"🔌 Errore connessione al tentativo {attempt}")
                if attempt == len(timeouts):
                    return "REDIRECT_TO_HUMAN - Errore di connessione al servizio"
                    
            except Exception as e:
                print(f"❌ Errore imprevisto al tentativo {attempt}: {str(e)}")
                if attempt == len(timeouts):
                    return f"REDIRECT_TO_HUMAN - Errore tecnico: {str(e)[:100]}"
        
        return "REDIRECT_TO_HUMAN - Impossibile generare risposta dopo tutti i tentativi"

    def get_performance_stats(self) -> Dict[str, Any]:
        """Ottieni statistiche di performance del sistema Ollama"""
        try:
            # Test di velocità con query semplice
            import time
            start_time = time.time()
            
            test_payload = {
                "model": self.model,
                "prompt": "Test di velocità: rispondi solo 'OK'",
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 5,
                    "num_ctx": 256
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=test_payload,
                timeout=10
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    "healthy": True,
                    "response_time": round(response_time, 2),
                    "model": self.model,
                    "performance": "Veloce" if response_time < 3 else "Normale" if response_time < 8 else "Lento"
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

    def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Scarica un modello da Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name}
            )
            return {
                "success": response.status_code == 200,
                "message": response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_model(self, model_name: str) -> Dict[str, Any]:
        """Elimina un modello da Ollama"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name}
            )
            return {
                "success": response.status_code == 200,
                "message": "Modello eliminato con successo" if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_model_info(self, model_name: str = None) -> Dict[str, Any]:
        """Ottiene informazioni su un modello specifico"""
        target_model = model_name or self.model
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": target_model}
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "error": f"Modello {target_model} non trovato"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def health_check(self) -> Dict[str, Any]:
        """Verifica completa dello stato di Ollama"""
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
                "available_models": models
            }
            
        except requests.exceptions.Timeout:
            return {"healthy": False, "error": "Timeout nella connessione"}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
