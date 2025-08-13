#!/usr/bin/env python3
"""
Script di setup automatico per ChatBot RAG Gratuito
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
    print(f"🚀 {title}")
    print("="*60)

def print_step(step, description):
    print(f"\n{step} {description}")
    print("-" * 40)

def run_command(command, description, check=True):
    """Esegue un comando e mostra il risultato"""
    print(f"📟 Eseguendo: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completato!")
            if result.stdout.strip():
                print(f"📄 Output: {result.stdout.strip()}")
            return True
        else:
            if check:
                print(f"❌ Errore in {description}")
                print(f"📄 Error: {result.stderr.strip()}")
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
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Richiede Python 3.8+")
        return False

def install_ollama():
    """Installa Ollama se non presente"""
    print_step("1️⃣", "Installazione Ollama")
    
    system = platform.system().lower()
    
    # Verifica se Ollama è già installato
    if run_command("ollama --version", "Verifica Ollama", check=False):
        print("✅ Ollama già installato!")
        return True
    
    print("⬇️  Ollama non trovato, installazione in corso...")
    
    if system == "windows":
        print("🪟 Sistema Windows rilevato")
        print("💡 Scarica Ollama manualmente da: https://ollama.ai/download/windows")
        print("⏳ Premi INVIO dopo aver installato Ollama...")
        input()
        return run_command("ollama --version", "Verifica installazione Ollama")
        
    elif system == "darwin":  # macOS
        print("🍎 Sistema macOS rilevato")
        return run_command("brew install ollama", "Installazione Ollama via Homebrew")
        
    elif system == "linux":
        print("🐧 Sistema Linux rilevato")
        return run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installazione Ollama")
    
    else:
        print(f"❌ Sistema {system} non supportato per installazione automatica")
        print("💡 Installa Ollama manualmente da: https://ollama.ai")
        return False

def install_python_deps():
    """Installa dipendenze Python"""
    print_step("2️⃣", "Installazione dipendenze Python")
    
    # Verifica se requirements_free.txt esiste
    if not os.path.exists("requirements_free.txt"):
        print("❌ File requirements_free.txt non trovato!")
        return False
    
    # Installa le dipendenze
    return run_command(
        f"{sys.executable} -m pip install -r requirements_free.txt",
        "Installazione pacchetti Python"
    )

def setup_ollama_model():
    """Setup modello Mistral in Ollama"""
    print_step("3️⃣", "Setup modello Mistral 7B")
    
    # Avvia Ollama se non è in esecuzione
    print("🔄 Verifica servizio Ollama...")
    if not run_command("ollama list", "Verifica servizio Ollama", check=False):
        print("🚀 Avvio servizio Ollama...")
        if platform.system().lower() == "windows":
            subprocess.Popen(["ollama", "serve"], shell=True)
        else:
            subprocess.Popen(["ollama", "serve"])
        
        print("⏳ Attesa 5 secondi per l'avvio del servizio...")
        time.sleep(5)
    
    # Verifica se il modello è già presente
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if "mistral" in result.stdout:
        print("✅ Modello Mistral già presente!")
        return True
    
    # Scarica il modello
    print("⬇️  Download modello Mistral 7B (questo può richiedere 10-20 minuti)...")
    print("📊 Dimensione: ~4GB")
    
    return run_command("ollama pull mistral:7b", "Download modello Mistral")

def setup_environment():
    """Setup file di ambiente"""
    print_step("4️⃣", "Setup configurazione ambiente")
    
    if os.path.exists(".env"):
        print("✅ File .env già presente!")
        return True
    
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print("✅ Creato .env da .env.example")
        return True
    else:
        print("❌ File .env.example non trovato!")
        return False

def create_vectorstore():
    """Crea il vectorstore dai documenti"""
    print_step("5️⃣", "Creazione vectorstore dai documenti")
    
    # Verifica se i documenti esistono
    if not os.path.exists("data"):
        print("❌ Cartella 'data' non trovata!")
        print("💡 Assicurati di aver caricato i documenti FAQ e guide")
        return False
    
    # Estrai i documenti
    if not os.path.exists("extracted_text") or not os.listdir("extracted_text"):
        print("📂 Estrazione testi dai documenti...")
        if not run_command(f"{sys.executable} src/extract_and_save.py", "Estrazione documenti"):
            return False
    
    # Crea vectorstore
    if not os.path.exists("vectordb") or not os.listdir("vectordb"):
        print("🔄 Creazione vectorstore (questo può richiedere alcuni minuti)...")
        return run_command(f"{sys.executable} src/create_vectorstore.py", "Creazione vectorstore")
    else:
        print("✅ Vectorstore già presente!")
        return True

def test_chatbot():
    """Test rapido del chatbot"""
    print_step("6️⃣", "Test del chatbot")
    
    try:
        # Import dei moduli necessari
        sys.path.append("src")
        from chatbot import setup_chatbot
        
        print("🧪 Test inizializzazione chatbot...")
        chatbot = setup_chatbot()
        
        if chatbot:
            print("✅ Chatbot inizializzato correttamente!")
            
            # Test rapido
            print("🔍 Test query rapida...")
            result = chatbot.chat("Orari segreteria")
            print(f"📝 Risposta test: {result['response'][:100]}...")
            
            return True
        else:
            print("❌ Errore nell'inizializzazione del chatbot")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel test: {str(e)}")
        return False

def main():
    print_header("SETUP AUTOMATICO CHATBOT RAG GRATUITO")
    print("🎓 ChatBot Segreteria Studenti - UniBG")
    print("🤖 Tecnologie: Mistral 7B + SentenceTransformers + ChromaDB")
    print("💰 Completamente GRATUITO e LOCALE")
    
    # Verifica Python
    if not check_python():
        print("❌ Versione Python non compatibile!")
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
                break
        except KeyboardInterrupt:
            print("\n🛑 Setup interrotto dall'utente")
            break
        except Exception as e:
            print(f"❌ Errore in {step_name}: {str(e)}")
            break
    
    # Riepilogo finale
    print_header("RIEPILOGO SETUP")
    print(f"✅ Step completati: {len(success_steps)}/{len(steps)}")
    
    for step in success_steps:
        print(f"   ✅ {step}")
    
    if len(success_steps) == len(steps):
        print("\n🎉 SETUP COMPLETATO CON SUCCESSO!")
        print("🚀 Avvia il chatbot con: python main.py")
    else:
        print(f"\n⚠️  Setup parzialmente completato ({len(success_steps)}/{len(steps)})")
        print("💡 Risolvi gli errori e riprova il setup")
    
    print("\n📚 Documentazione aggiuntiva:")
    print("   🌐 Ollama: https://ollama.ai")
    print("   🤖 Mistral: https://mistral.ai")
    print("   📊 ChromaDB: https://docs.trychroma.com")

if __name__ == "__main__":
    main()
