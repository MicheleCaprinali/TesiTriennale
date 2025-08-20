#!/usr/bin/env python3
"""
Script di setup automatico per ChatBot
Installa e configura tutto il necessario per il chatbot
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    print(f"\n{step} {description}")
    print("-" * 40)

def run_command(command, description, check=True):
    """Esegue un comando e mostra il risultato"""
    print(f" Eseguendo: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completato!")
            if result.stdout.strip():
                print(f" Output: {result.stdout.strip()}")
            return True
        else:
            if check:
                print(f"❌ Errore in {description}")
                print(f" Error: {result.stderr.strip()}")
                return False
            else:
                print(f"⚠️  {description} - continuiamo...")
                return True
    except Exception as e:
        print(f"❌ Errore esecuzione comando: {str(e)}")
        return False

def check_python():
    """Verifica versione Python"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Richiede Python 3.9+")
        return False

def install_ollama():
    """Installa Ollama se non presente"""
    print_step("1-", "Installazione Ollama")

    system = platform.system().lower()
    
    # Verifica se Ollama è già installato
    if run_command("ollama --version", "Verifica Ollama", check=False):
        print("✅ Ollama già installato!")
        return True
    
    print(" Ollama non trovato, installazione in corso...")
    
    if system == "windows":
        print(" Sistema Windows rilevato")
        print(" Scarica Ollama manualmente da: https://ollama.ai/download/windows")
        print(" Premi INVIO dopo aver installato Ollama...")
        input()
        return run_command("ollama --version", "Verifica installazione Ollama")
        
    elif system == "darwin":  # macOS
        print(" Sistema macOS rilevato")
        return run_command("brew install ollama", "Installazione Ollama via Homebrew")
        
    elif system == "linux":
        print(" Sistema Linux rilevato")
        return run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installazione Ollama")
    
    else:
        print(f"❌ Sistema {system} non supportato per installazione automatica")
        print(" Installa Ollama manualmente da: https://ollama.ai")
        return False

def install_python_deps():
    """Installa dipendenze Python"""
    print_step("2-", "Installazione dipendenze Python")
    
    # Verifica se requirements.txt esiste
    if not os.path.exists("requirements.txt"):
        print("❌ File requirements.txt non trovato!")
        return False
    
    # Installa le dipendenze
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installazione pacchetti Python"
    )

def setup_ollama_model():
    """Setup modello Mistral in Ollama"""
    print_step("3-", "Setup modello Mistral 7B")

    # Avvia Ollama se non è in esecuzione
    print(" Verifica servizio Ollama...")
    if not run_command("ollama list", "Verifica servizio Ollama", check=False):
        print(" Avvio servizio Ollama...")
        if platform.system().lower() == "windows":
            subprocess.Popen(["ollama", "serve"], shell=True)
        else:
            subprocess.Popen(["ollama", "serve"])
        
        print(" Attesa 5 secondi per l'avvio del servizio...")
        time.sleep(5)
    
    # Verifica se il modello è già presente
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if "mistral" in result.stdout:
        print("✅ Modello Mistral già presente!")
        return True
    
    # Scarica il modello
    print(" Download modello Mistral 7B (questo può richiedere 10-20 minuti)...")
    print(" Dimensione: ~4GB")
    
    return run_command("ollama pull mistral:7b", "Download modello Mistral")

def setup_environment():
    """Setup file di ambiente"""
    print_step("4-", "Setup configurazione ambiente")
    
    if os.path.exists(".env"):
        print("✅ File .env già presente!")
        return True
    
    # Usa .env.example se disponibile, altrimenti crea configurazione base
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print("✅ Creato .env da .env.example")
        
        # Aggiungi DEBUG se mancante
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "DEBUG=" not in content:
            with open(".env", "a", encoding="utf-8") as f:
                f.write("\n# Debug mode\nDEBUG=false\n")
            print("✅ Aggiunto parametro DEBUG")
        
        return True
    else:
        # Fallback: crea configurazione base
        env_content = """# Configurazione ChatBot
DEBUG=false
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=5
TEMPERATURE=0.1
OLLAMA_MODEL=mistral:7b
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTORDB_PATH=vectordb
TICKET_URL=https://www.unibg.it/servizi-studenti/contatti
"""
        
        try:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            print("✅ Creato file .env con configurazioni di base")
            return True
        except Exception as e:
            print(f"❌ Errore nella creazione del file .env: {str(e)}")
            return False

def create_vectorstore():
    """Crea il vectorstore dai documenti"""
    print_step("5-", "Creazione vectorstore dai documenti")
    
    # Verifica se i documenti esistono
    if not os.path.exists("data"):
        print("❌ Cartella 'data' non trovata!")
        print(" Assicurati di aver caricato i documenti FAQ e guide")
        return False
    
    # Estrai i documenti
    if not os.path.exists("extracted_text") or not os.listdir("extracted_text"):
        print(" Estrazione testi dai documenti...")
        if not run_command(f"{sys.executable} src/extract_and_save.py", "Estrazione documenti"):
            return False
    
    # Crea vectorstore
    if not os.path.exists("vectordb") or not os.listdir("vectordb"):
        print(" Creazione vectorstore (questo può richiedere alcuni minuti)...")
        return run_command(f"{sys.executable} src/create_vectorstore.py", "Creazione vectorstore")
    else:
        print("✅ Vectorstore già presente!")
        return True

def test_chatbot():
    """Test rapido del chatbot"""
    print_step("6-", "Test del chatbot")
    
    try:
        # Verifica che tutti i file necessari esistano
        required_files = [
            "src/chatbot.py",
            "src/ollama_llm.py", 
            "vectordb",
            "extracted_text"
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                print(f"❌ File necessario mancante: {file_path}")
                return False
        
        # Test import dei moduli
        sys.path.append("src")
        try:
            from chatbot import setup_chatbot  # type: ignore
            print("✅ Import moduli completato!")
        except ImportError as e:
            print(f"❌ Errore import: {str(e)}")
            return False
        
        # Test inizializzazione (senza eseguire query per velocità)
        print(" Test inizializzazione chatbot...")
        try:
            chatbot = setup_chatbot()
            if chatbot:
                print("✅ Chatbot inizializzato correttamente!")
                return True
            else:
                print("❌ Errore nell'inizializzazione del chatbot")
                return False
        except Exception as e:
            print(f"❌ Errore nell'inizializzazione: {str(e)}")
            print(" Nota: Assicurati che Ollama sia in esecuzione")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel test: {str(e)}")
        return False

def main():
    print_header("SETUP AUTOMATICO CHATBOT")
    print(" ChatBot Segreteria Studenti - UniBG")
    print(" Tecnologie: Mistral 7B + SentenceTransformers + ChromaDB")
    print(" Python 3.9+ richiesto")
    
    # Verifica Python
    if not check_python():
        print("❌ Versione Python non compatibile!")
        print(" Aggiorna Python a versione 3.9 o superiore")
        return
    
    success_steps = []
    
    # Step di installazione
    steps = [
        ("Ollama", install_ollama),
        ("Dipendenze Python", install_python_deps),
        ("Modello Mistral", setup_ollama_model),
        ("Configurazione", setup_environment),
        ("Vectorstore", create_vectorstore),
        ("Test Chatbot", test_chatbot)
    ]
    
    for step_name, step_func in steps:
        try:
            if step_func():
                success_steps.append(step_name)
                print(f"✅ {step_name} completato!")
            else:
                print(f"❌ {step_name} fallito!")
                print(" Controlla i messaggi di errore sopra")
                break
        except KeyboardInterrupt:
            print("\n Setup interrotto dall'utente")
            break
        except Exception as e:
            print(f"❌ Errore inatteso in {step_name}: {str(e)}")
            break
    
    # Riepilogo finale
    print_header("RIEPILOGO SETUP")
    print(f"✅ Step completati: {len(success_steps)}/{len(steps)}")
    
    for step in success_steps:
        print(f"   ✅ {step}")
    
    if len(success_steps) == len(steps):
        print("\n SETUP COMPLETATO CON SUCCESSO!")
        print(" ")
        print(" Comandi disponibili:")
        print("   python main.py                    # Interfaccia CLI")
        print("   streamlit run interfaces/streamlit_app.py  # Interfaccia Web")
        print("   start_chatbot.bat                 # Avvio rapido CLI")
        print("   start_web.bat                     # Avvio rapido Web")
        print(" ")
        print(" Il sistema è pronto per l'uso!")
    else:
        print(f"\n⚠️  Setup parzialmente completato ({len(success_steps)}/{len(steps)})")
        print(" Risolvi gli errori sopra e riprova il setup")
        print(" ")
        print(" Comandi utili per troubleshooting:")
        print("   ollama --version     # Verifica Ollama")
        print("   ollama list          # Lista modelli")
        print("   pip list             # Verifica pacchetti Python")
    
    print("\n Documentazione di riferimento:")
    print("    USER_MANUAL.md       - Guida utente completa")
    print("    TECHNICAL_DOCS.md    - Documentazione tecnica")
    print("    Ollama: https://ollama.ai")
    print("    Mistral: https://mistral.ai")

if __name__ == "__main__":
    main()
