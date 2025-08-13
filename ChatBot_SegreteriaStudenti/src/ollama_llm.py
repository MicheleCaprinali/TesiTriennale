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
        """Genera risposta usando Ollama"""
        
        # Costruisce il prompt completo
        full_prompt = f"""Sei un assistente della Segreteria Studenti dell'Università degli Studi di Bergamo.
Rispondi in italiano in modo professionale ma amichevole.

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
                "max_tokens": 500
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate", 
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'Errore nella generazione della risposta.')
            else:
                return f"Errore HTTP {response.status_code}: {response.text}"
                
        except requests.exceptions.Timeout:
            return "Timeout: Il modello sta impiegando troppo tempo a rispondere."
        except Exception as e:
            return f"Errore nella comunicazione con Ollama: {str(e)}"
    
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
