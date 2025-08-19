"""
Modulo per gestire LLM locale con Ollama (gratuito)
"""

import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class OllamaLLM:
    """
    Classe per interfacciarsi con Ollama per LLM locale gratuito
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
        """Genera risposta usando Ollama con retry automatico"""
        
        # Costruisce il prompt completo OTTIMIZZATO E CONCISO
        full_prompt = f"""Sei l'assistente AI della Segreteria UniBG. Rispondi in italiano, modo professionale e conciso.

REGOLE CRITICHE:
- USA SOLO informazioni dal CONTESTO fornito
- Se non hai info sufficienti: "Non ho informazioni sufficienti"
- Link: copia ESATTAMENTE dal contesto, MAI inventare
- Massimo 150 parole per risposta

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
                "top_p": 0.9,
                "max_tokens": 300,  # Ridotto da 500 per risposte più concise
                "num_predict": 300,  # Limita predizione
                "stop": ["\n\nDOMANDA:", "DOMANDA STUDENTE:", "CONTESTO:"],  # Stop tokens
                "repeat_penalty": 1.1,  # Evita ripetizioni
                "top_k": 40  # Limita vocabolario per velocità
            }
        }
        
        # Sistema di retry con timeout progressivo
        timeouts = [15, 25, 35]  # Timeout progressivi
        
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
                    answer = result.get('response', 'Errore nella generazione della risposta.')
                    
                    # Verifica che la risposta non sia vuota
                    if answer.strip():
                        print(f"✅ Risposta generata al tentativo {attempt}")
                        return answer
                    else:
                        print(f"⚠️  Risposta vuota al tentativo {attempt}")
                        continue
                else:
                    print(f"❌ HTTP {response.status_code} al tentativo {attempt}")
                    if attempt == len(timeouts):
                        return f"Errore HTTP {response.status_code}: {response.text}"
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"⏱️  Timeout al tentativo {attempt} ({timeout}s)")
                if attempt == len(timeouts):
                    return "Il sistema sta impiegando troppo tempo. Riprova tra qualche momento o contatta la segreteria."
                continue
            except Exception as e:
                print(f"❌ Errore al tentativo {attempt}: {str(e)}")
                if attempt == len(timeouts):
                    return f"Errore nella comunicazione con il sistema: {str(e)}"
                continue
        
        return "Errore imprevisto nella generazione della risposta."

    def pull_model(self) -> bool:
        """Scarica il modello se non presente"""
        payload = {"name": self.model}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=600  # 10 minuti per il download
            )
            return response.status_code == 200
        except:
            return False

def setup_ollama():
    """Setup e verifica di Ollama"""
    print("🔄 Verifica setup Ollama...")
    
    llm = OllamaLLM()
    
    # Verifica se Ollama è in esecuzione
    if not llm.is_running():
        print("❌ Ollama non è in esecuzione!")
        print("💡 Avvia Ollama con: ollama serve")
        return False
    
    print("✅ Ollama è in esecuzione!")
    
    # Verifica modelli disponibili
    models = llm.list_models()
    print(f"📋 Modelli disponibili: {models}")
    
    if llm.model not in models:
        print(f"⬇️  Scaricamento modello {llm.model}...")
        print("⚠️  Questo può richiedere diversi minuti...")
        if llm.pull_model():
            print("✅ Modello scaricato!")
        else:
            print("❌ Errore nel download del modello")
            return False
    
    return True

if __name__ == "__main__":
    # Test del modulo
    if setup_ollama():
        llm = OllamaLLM()
        
        # Test di generazione
        test_context = "L'università di Bergamo offre corsi di laurea in ingegneria informatica."
        test_query = "Ci sono corsi di informatica?"
        
        print(f"\n🧪 Test generazione:")
        print(f"Contesto: {test_context}")
        print(f"Domanda: {test_query}")
        
        response = llm.generate(test_query, test_context)
        print(f"\n🤖 Risposta: {response}")
    else:
        print("❌ Setup Ollama fallito!")
