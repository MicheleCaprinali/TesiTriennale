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
        """Genera risposta usando Ollama con parametri ottimizzati per risposte complete"""
        
        # Prompt semplice e diretto
        final_prompt = f"""Contesto: {context}

Domanda: {prompt}

Risposta completa (includi tutti i dettagli e link):"""
        
        # Parametri ottimizzati per VELOCITÀ MASSIMA
        data = {
            "model": self.model,
            "prompt": final_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,     # Bassa per consistenza
                "top_p": 0.8,          
                "num_predict": 150,     # Ridotto per velocità
                "num_ctx": 1024,       # Ridotto per velocità
                "repeat_penalty": 1.1,  
                "stop": ["Domanda:", "Contesto:"]
            }
        }
        
        try:
            print(f"Generazione risposta (timeout: 30s)...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=30  # Timeout ridotto per velocità
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('response', '').strip()
                
                if answer and len(answer) > 10:
                    print(f"✅ Risposta generata ({len(answer)} caratteri)")
                    return answer
                else:
                    print(f"❌ Risposta troppo breve")
                    return "REDIRECT_TO_HUMAN - Risposta incompleta"
                    
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout - sistema sovraccarico")
            return "REDIRECT_TO_HUMAN - Sistema temporaneamente lento, riprova tra qualche secondo"
            
        except Exception as e:
            print(f"❌ Errore LLM: {str(e)}")
            return "REDIRECT_TO_HUMAN - Errore tecnico"
        
        return "REDIRECT_TO_HUMAN - Nessuna risposta generata"

    def generate_with_retry(self, prompt: str, context: str = "") -> str:
        """Genera risposta con retry automatico e timeout progressivi"""
        
        full_prompt = f"""Sei l'assistente AI della Segreteria UniBg. Rispondi in italiano, modo professionale e completo.

REGOLE CRITICHE:
- USA SOLO informazioni dal CONTESTO fornito
- Se non hai info sufficienti: "Non ho informazioni sufficienti"
- Link: copia ESATTAMENTE dal contesto, MAI inventare
- Fornisci risposte complete e dettagliate

CONTESTO:
{context}

DOMANDA: {prompt}

RISPOSTA:"""

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": 0.8,
                "num_predict": 150,  # Ridotto per velocità
                "num_ctx": 1024,     # Ridotto per velocità
                "stop": ["\n\nDOMANDA:", "DOMANDA STUDENTE:", "CONTESTO:"],
                "repeat_penalty": 1.1,
                "top_k": 20  # Ridotto per velocità
            }
        }
        
        # Sistema di retry con timeout ottimizzati per velocità
        timeouts = [10, 20, 30]  # Timeout ridotti per velocità
        
        for attempt, timeout in enumerate(timeouts, 1):
            try:
                print(f"Tentativo {attempt}/{len(timeouts)} (timeout: {timeout}s)")
                
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('response', '').strip()
                    
                    if answer and len(answer) > 20:
                        print(f"✅ Risposta generata al tentativo {attempt}")
                        return answer
                    else:
                        print(f"⚠️ Risposta vuota al tentativo {attempt}")
                        if attempt < len(timeouts):
                            continue
                else:
                    print(f"❌ HTTP {response.status_code} al tentativo {attempt}")
                    if attempt == len(timeouts):
                        return f"Errore del server ({response.status_code}). Riprova più tardi."
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"Timeout al tentativo {attempt} ({timeout}s)")
                if attempt == len(timeouts):
                    return "Il sistema sta impiegando troppo tempo. Riprova tra qualche momento o contatta la segreteria."
                continue
            except Exception as e:
                print(f"❌ Errore al tentativo {attempt}: {str(e)}")
                if attempt == len(timeouts):
                    return f"Errore nella comunicazione con il sistema: {str(e)}"
                continue
        
        return "Errore imprevisto nella generazione della risposta."

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
