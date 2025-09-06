#!/usr/bin/env python3
"""
ChatBot Segreteria Studenti - Tesi Triennale Ingegneria Informatica
Sistema per rispondere automaticamente alle domande degli studenti universitari

Tecnologie utilizzate:
- Sentence Transformers (all-MiniLM-L6-v2) per embedding
- ChromaDB per vector store
- Ollama + Mistral 7B per LLM locale
- LangChain per orchestrazione RAG
"""

import os
import sys
from datetime import datetime

# Aggiungi il path per gli import
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import con gestione errori
try:
    from chatbot import setup_chatbot, ChatbotRAG  # type: ignore
    from create_vectorstore import crea_vectorstore_free  # type: ignore
    from ollama_llm import OllamaLLM  # type: ignore
except ImportError as e:
    print(f"❌ Errore import moduli: {e}")
    print("Esegui: pip install -r requirements.txt")
    sys.exit(1)

def check_requirements():
    """Verifica requisiti minimi per il funzionamento"""
    print("Verifica sistema...")
    
    checks = []
    
    # Verifica Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get('models', [])
            has_mistral = any('mistral' in model.get('name', '') for model in models)
            if has_mistral:
                checks.append("✅ Ollama + Mistral: Pronti")
            else:
                checks.append("⚠️ Ollama: Attivo, ma Mistral mancante")
        else:
            checks.append("❌ Ollama: Non risponde")
    except:
        checks.append("❌ Ollama: Non in esecuzione")
    
    # Verifica vectorstore
    if os.path.exists("vectordb") and os.listdir("vectordb"):
        checks.append("✅ Database vettoriale: Presente")
    else:
        checks.append("❌ Database vettoriale: Mancante")
    
    # Verifica documenti estratti
    if os.path.exists("extracted_text") and os.listdir("extracted_text"):
        checks.append("✅ Documenti estratti: Presenti")
    else:
        checks.append("❌ Documenti estratti: Mancanti")
    
    for check in checks:
        print(f"{check}")
    
    has_errors = any("❌" in check for check in checks)
    if has_errors:
        print("\nUsa 'python setup.py' per il setup completo")
        return False
    
    has_warnings = any("⚠️" in check for check in checks)
    if has_warnings:
        print("\n⚠️ Sistema parzialmente configurato")
        return True
        
    return True

def setup_project():
    """Verifica rapida e recovery automatico se necessario"""
    print("Inizializzazione ChatBot...")
    print("=" * 50)
    
    if not check_requirements():
        print("\n❌ Setup incompleto!")
        print("Esegui: python setup.py")
        return False
    
    if not os.path.exists("vectordb") or not os.listdir("vectordb"):
        print("\nRecovery automatico database...")
        try:
            import setup
            if setup.create_vectorstore():
                print("✅ Database ricreato!")
            else:
                print("❌ Errore nel recovery - usa setup.py manuale")
                return False
        except Exception as e:
            print(f"❌ Recovery fallito: {str(e)}")
            print("Esegui: python setup.py")
            return False
    
    print("✅ Sistema pronto!")
    return True

def chatbot_cli():
    """Interfaccia a riga di comando per il chatbot"""
    chatbot = setup_chatbot()
    
    if not chatbot:
        print("❌ Impossibile inizializzare il chatbot")
        return False
    
    print("\n" + "=" * 60)
    print("CHATBOT SEGRETERIA STUDENTI UNIBG")
    print("=" * 60)
    print("Fai una domanda sull'università!")
    print("Digita 'help' per esempi - 'exit' per uscire")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 40)
        domanda = input("Studente > ").strip()
        
        if domanda.lower() in ['exit', 'quit', 'bye']:
            print("Arrivederci!")
            break
            
        elif domanda.lower() == 'help':
            show_help()
            continue
            
        elif not domanda:
            print("Scrivi una domanda.")
            continue
        
        try:
            result = chatbot.chat(domanda)
            response = result['response']
            
            import re
            url_pattern = r'(https?://[^\s<>"{}|\\^`\[\]]+)'
            highlighted_response = re.sub(url_pattern, r'\1', response)
            
            print(f"ChatBot: {highlighted_response}")
            
            if result['should_redirect']:
                print(f"\nPer assistenza personalizzata:")
                print(f"{os.getenv('TICKET_URL', 'https://helpdesk.unibg.it/')}")
                
        except Exception as e:
            print(f"❌ Errore nel processare la richiesta: {str(e)}")
            print("Ti consiglio di contattare direttamente la Segreteria:")
            print(f"{os.getenv('TICKET_URL', 'https://helpdesk.unibg.it/')}")
    
    return True

def show_help():
    """Mostra esempi di domande che il chatbot può gestire"""
    print("\nESEMPI DI DOMANDE:")
    print("-" * 30)
    print("'Come faccio a iscrivermi agli esami?'")
    print("'Quando devo pagare le tasse universitarie?'")
    print("'Come richiedo un certificato di laurea?'")
    print("'Che documenti servono per la laurea?'")
    print("'Quali sono i contatti della segreteria?'")
    print("'Come funziona il servizio disabilità?'")
    print("'Come trovo informazioni sui tirocini?'")

def show_setup_instructions():
    """Mostra istruzioni per il setup iniziale"""
    print("\nSETUP RAPIDO:")
    print("=" * 30)
    print("Setup automatico (raccomandato):")
    print("   python setup.py")
    print()
    print("Setup manuale:")
    print("1. Installa Ollama: https://ollama.ai")
    print("2. Avvia Ollama: ollama serve")
    print("3. Scarica modello: ollama pull mistral:7b")
    print("4. Installa Python deps: pip install -r requirements.txt")
    print("5. Avvia chatbot: python main.py")
    print()
    print("Documentazione completa:")
    print("   user_manual.md")
    print("   technical_docs.md")

def main():
    """Funzione principale"""
    print("ChatBot Segreteria Studenti - UniBg")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            show_setup_instructions()
            return
        elif sys.argv[1] == "--check":
            check_requirements()
            return
        elif sys.argv[1] == "--help":
            print("\nComandi disponibili:")
            print("  python main.py           # Avvia chatbot")
            print("  python main.py --setup   # Mostra istruzioni setup")
            print("  python main.py --check   # Verifica sistema")
            print("  python setup.py          # Setup automatico completo")
            return
    
    if not setup_project():
        return
    
    chatbot_cli()

if __name__ == "__main__":
    main()