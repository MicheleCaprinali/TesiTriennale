#!/usr/bin/env python3
"""
ChatBot Segreteria Studenti - Tesi Triennale Ingegneria Informatica
Sistema RAG GRATUITO per rispondere automaticamente alle domande degli studenti universitari

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

from chatbot import setup_chatbot, ChatbotRAG
from extract_and_save import process_all_documents
from create_vectorstore import crea_vectorstore_free
from ollama_llm import setup_ollama

def check_requirements():
    """Verifica requisiti del sistema"""
    print("🔍 Verifica requisiti sistema...")
    
    requirements = []
    
    # Verifica Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            requirements.append("✅ Ollama: Disponibile")
        else:
            requirements.append("❌ Ollama: Non risponde")
    except:
        requirements.append("❌ Ollama: Non in esecuzione")
    
    # Verifica pacchetti Python
    packages = [
        ("sentence_transformers", "Sentence Transformers"),
        ("chromadb", "ChromaDB"),
        ("requests", "Requests"),
    ]
    
    for package, name in packages:
        try:
            __import__(package)
            requirements.append(f"✅ {name}: Installato")
        except ImportError:
            requirements.append(f"❌ {name}: Mancante")
    
    for req in requirements:
        print(f"   {req}")
    
    return all("✅" in req for req in requirements)

def setup_project():
    """Inizializzazione completa del progetto"""
    print("🚀 SETUP CHATBOT RAG GRATUITO")
    print("=" * 50)
    
    # Step 1: Verifica requisiti
    if not check_requirements():
        print("\n❌ Requisiti mancanti! Segui le istruzioni di setup.")
        return False
    
    # Step 2: Verifica/crea file estratti
    if not os.path.exists("extracted_text") or not os.listdir("extracted_text"):
        print("\n📂 Estrazione documenti in corso...")
        if not process_all_documents():
            print("❌ Errore nell'estrazione documenti")
            return False
    else:
        print("✅ File estratti già presenti")
    
    # Step 3: Verifica/crea vectorstore
    if not os.path.exists("vectordb") or not os.listdir("vectordb"):
        print("\n🔄 Creazione vectorstore...")
        try:
            from split_into_chunks import split_text_in_chunks
            import glob
            
            cartella_estratti = "extracted_text"
            tutti_i_chunks = []
            
            for filepath in glob.glob(os.path.join(cartella_estratti, "*.txt")):
                with open(filepath, "r", encoding="utf-8") as f:
                    testo = f.read()
                    chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
                    tutti_i_chunks.extend(chunks)
            
            if tutti_i_chunks:
                crea_vectorstore_free(tutti_i_chunks)
                print("✅ Vectorstore creato!")
            else:
                print("❌ Nessun chunk trovato")
                return False
                
        except Exception as e:
            print(f"❌ Errore creazione vectorstore: {str(e)}")
            return False
    else:
        print("✅ Vectorstore già presente")
    
    # Step 4: Setup Ollama
    print("\n🔄 Verifica setup Ollama...")
    if not setup_ollama():
        print("❌ Setup Ollama fallito")
        return False
    
    print("\n✅ Setup completato con successo!")
    return True

def chatbot_cli():
    """Interfaccia a riga di comando per il chatbot"""
    chatbot = setup_chatbot()
    
    if not chatbot:
        print("❌ Impossibile inizializzare il chatbot")
        return False
    
    print("\n" + "=" * 60)
    print("🎓 CHATBOT SEGRETERIA STUDENTI UNIBG - GRATUITO")
    print("=" * 60)
    print("🤖 Tecnologie: Mistral 7B + SentenceTransformers + ChromaDB")
    print("💡 Fai una domanda sull'università!")
    print("📝 Digita 'help' per vedere esempi di domande")
    print("🚪 Digita 'exit' per uscire")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 40)
        domanda = input("👤 Studente > ").strip()
        
        if domanda.lower() in ['exit', 'quit', 'bye']:
            print("👋 Arrivederci! Buono studio!")
            break
            
        elif domanda.lower() == 'help':
            show_help()
            continue
            
        elif not domanda:
            print("❓ Per favore, scrivi una domanda.")
            continue
        
        try:
            # Elabora la domanda
            result = chatbot.chat(domanda)
            
            # Mostra la risposta
            print("🤖 " + result['response'])
            
            # Se necessario, suggerisci il ticket
            if result['should_redirect']:
                print(f"\n🎫 Per assistenza personalizzata:")
                print(f"🌐 {os.getenv('TICKET_URL', 'https://www.unibg.it/servizi-studenti/contatti')}")
                
        except Exception as e:
            print(f"❌ Errore nel processare la richiesta: {str(e)}")
            print("🎫 Ti consiglio di contattare direttamente la Segreteria.")
    
    return True

def show_help():
    """Mostra esempi di domande che il chatbot può gestire"""
    print("\n💡 ESEMPI DI DOMANDE:")
    print("─" * 30)
    print("📚 'Come faccio a iscrivermi agli esami?'")
    print("💰 'Quando devo pagare le tasse universitarie?'")
    print("📄 'Come richiedo un certificato di laurea?'")
    print("🎓 'Che documenti servono per la laurea?'")
    print("📞 'Quali sono i contatti della segreteria?'")
    print("🕒 'Quali sono gli orari di apertura?'")
    print("♿ 'Come funziona il servizio disabilità?'")
    print("💼 'Come trovo informazioni sui tirocini?'")

def show_setup_instructions():
    """Mostra istruzioni per il setup iniziale"""
    print("\n📋 ISTRUZIONI SETUP:")
    print("=" * 30)
    print("1️⃣  Installa Ollama:")
    print("    🌐 https://ollama.ai")
    print("    💻 Scarica e installa per il tuo OS")
    print()
    print("2️⃣  Avvia Ollama:")
    print("    📟 ollama serve")
    print()
    print("3️⃣  Scarica Mistral 7B:")
    print("    📟 ollama pull mistral:7b")
    print("    ⏳ (Può richiedere 10-20 minuti)")
    print()
    print("4️⃣  Installa dipendenze Python:")
    print("    📟 pip install -r requirements_free.txt")
    print()
    print("5️⃣  Crea file .env:")
    print("    📄 Copia .env.example in .env")
    print()
    print("6️⃣  Avvia il chatbot:")
    print("    📟 python main.py")

def main():
    """Funzione principale"""
    print("🎓 ChatBot Segreteria Studenti - Setup")
    
    # Verifica argomenti
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            show_setup_instructions()
            return
        elif sys.argv[1] == "--check":
            check_requirements()
            return
    
    # Setup del progetto
    if not setup_project():
        print("\n❌ Setup fallito!")
        print("� Usa 'python main.py --setup' per le istruzioni")
        return
    
    # Avvia chatbot
    chatbot_cli()

if __name__ == "__main__":
    main()