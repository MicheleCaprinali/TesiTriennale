#!/usr/bin/env python3
"""
Script di setup automatico per ChatBot Segreteria Studenti UniBg
Installa e configura tutto il necessario per il sistema RAG
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)

def print_step(step, description):
    print(f"\n{step} {description}")
    print("-" * 40)

def run_command(command, description, check=True):
    """Esegue un comando e mostra il risultato"""
    print(f"Eseguendo: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completato!")
            return True
        else:
            if check:
                print(f"❌ Errore in {description}")
                if result.stderr.strip():
                    print(f"Error: {result.stderr.strip()}")
                return False
            else:
                print(f"⚠️ {description} - continuiamo...")
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

def check_venv():
    """Verifica se siamo in un ambiente virtuale"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        venv_path = sys.prefix
        print(f"✅ Ambiente virtuale attivo: {venv_path}")
        return True
    else:
        print("⚠️ Nessun ambiente virtuale rilevato")
        return False

def create_venv():
    """Crea e attiva ambiente virtuale"""
    print_step("1.", "Setup ambiente virtuale")
    
    venv_name = "chatbot_env"
    
    if check_venv():
        return True
    
    # Verifica se l'ambiente esiste già
    if os.path.exists(venv_name):
        print(f"✅ Ambiente virtuale '{venv_name}' già presente!")
        print(f"💡 Per attivarlo manualmente:")
        if platform.system().lower() == "windows":
            print(f"   {venv_name}\\Scripts\\activate")
        else:
            print(f"   source {venv_name}/bin/activate")
        
        # Chiedi se continuare o attivare manualmente
        choice = input("\nVuoi continuare senza ambiente virtuale? (s/N): ").lower()
        if choice != 's':
            print("⚠️ Attiva l'ambiente virtuale e riesegui lo setup")
            return False
        return True
    
    print(f"🔧 Creazione ambiente virtuale '{venv_name}'...")
    if not run_command(f"{sys.executable} -m venv {venv_name}", "Creazione ambiente virtuale"):
        return False
    
    print("\n" + "="*60)
    print("⚠️  IMPORTANTE: ATTIVA L'AMBIENTE VIRTUALE")
    print("="*60)
    
    if platform.system().lower() == "windows":
        activate_cmd = f"{venv_name}\\Scripts\\activate"
    else:
        activate_cmd = f"source {venv_name}/bin/activate"
    
    print(f"1. Apri un nuovo terminale")
    print(f"2. Esegui: {activate_cmd}")
    print(f"3. Riesegui: python setup.py")
    print("\nL'ambiente virtuale isola le dipendenze del progetto!")
    print("="*60)
    
    return False  # Ferma il setup per permettere attivazione manuale

def install_ollama():
    """Installa Ollama se non presente"""
    print_step("2.", "Verifica e installazione Ollama")

    if run_command("ollama --version", "Verifica Ollama", check=False):
        print("✅ Ollama già installato!")
        return True
    
    print("Ollama non trovato, installazione richiesta...")
    system = platform.system().lower()
    
    if system == "windows":
        print("Sistema Windows rilevato")
        print("📥 Scarica e installa Ollama da: https://ollama.ai/download/windows")
        print("Premi INVIO dopo aver installato Ollama...")
        input()
        return run_command("ollama --version", "Verifica installazione Ollama")
        
    elif system == "darwin":  # macOS
        print("Sistema macOS rilevato")
        print("Installazione via Homebrew...")
        return run_command("brew install ollama", "Installazione Ollama")
        
    elif system == "linux":
        print("Sistema Linux rilevato")
        return run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installazione Ollama")
    
    else:
        print(f"❌ Sistema {system} non supportato per installazione automatica")
        print("Installa Ollama manualmente da: https://ollama.ai")
        return False

def install_python_deps():
    """Installa dipendenze Python nell'ambiente virtuale"""
    print_step("3.", "Installazione dipendenze Python")
    
    if not os.path.exists("requirements.txt"):
        print("❌ File requirements.txt non trovato!")
        return False
    
    # Verifica ambiente virtuale
    if not check_venv():
        print("⚠️ Raccomandato: attiva ambiente virtuale prima dell'installazione")
        choice = input("Continuare comunque? (s/N): ").lower()
        if choice != 's':
            return False
    
    # Aggiorna pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Aggiornamento pip", check=False)
    
    # Installa le dipendenze
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installazione pacchetti Python"
    )

def setup_ollama_model():
    """Setup modello Mistral in Ollama"""
    print_step("4.", "Setup modello Mistral 7B")

    # Avvia servizio Ollama se non attivo
    print("Verifica servizio Ollama...")
    if not run_command("ollama list", "Verifica servizio Ollama", check=False):
        print("Avvio servizio Ollama...")
        if platform.system().lower() == "windows":
            subprocess.Popen(["ollama", "serve"], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["ollama", "serve"])
        
        print("Attesa avvio servizio...")
        time.sleep(5)
    
    # Verifica se Mistral è già installato
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if "mistral" in result.stdout:
        print("✅ Modello Mistral già presente!")
        return True
    
    print("📥 Download modello Mistral 7B...")
    print("⏳ Dimensione: ~4GB - Tempo stimato: 10-20 minuti")
    print("Non interrompere il download...")
    
    return run_command("ollama pull mistral:7b", "Download modello Mistral")

def setup_environment():
    """Setup file di ambiente"""
    print_step("5.", "Configurazione ambiente")
    
    if os.path.exists(".env"):
        print("✅ File .env già presente!")
        return True
    
    env_content = """# Configurazione ChatBot Segreteria Studenti UniBg
# Configurazione Embedding
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Configurazione Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b
TEMPERATURE=0.1

# Configurazione ChromaDB
VECTORDB_COLLECTION=unibg_docs
TICKET_URL=https://helpdesk.unibg.it/
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ File .env creato con configurazioni di base")
        return True
    except Exception as e:
        print(f"❌ Errore nella creazione del file .env: {str(e)}")
        return False

def check_data_structure():
    """Verifica struttura dati necessaria"""
    print_step("6.", "Verifica struttura dati")
    
    required_dirs = ["data", "src", "interfaccia"]  # ✅ Aggiunta cartella interfaccia
    required_files = [
        "src/local_embeddings.py",
        "src/ollama_llm.py", 
        "src/creazione_vectorstore.py",
        "src/testi_estratti.py",
        "src/dividi_chunks.py",
        "interfaccia/streamlit.py",  # ✅ Aggiunto file streamlit
        "main.py"  # ✅ Aggiunto main.py
    ]
    
    missing = []
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing.append(f"Cartella: {dir_name}")
    
    for file_name in required_files:
        if not os.path.exists(file_name):
            missing.append(f"File: {file_name}")
    
    if missing:
        print("❌ Elementi mancanti:")
        for item in missing:
            print(f"   - {item}")
        return False
    
    print("✅ Struttura progetto completa!")
    return True

def extract_texts():
    """Estrae testi dai PDF se necessario"""
    print_step("7.", "Estrazione testi dai documenti")
    
    if os.path.exists("data/testi_estratti") and os.listdir("data/testi_estratti"):
        print("✅ Testi già estratti!")
        return True
    
    if not os.path.exists("data"):
        print("❌ Cartella 'data' non trovata!")
        print("Carica i documenti PDF nella cartella data/")
        return False
    
    print("Estrazione testi dai PDF...")
    return run_command(f"{sys.executable} src/testi_estratti.py", "Estrazione documenti PDF")

def create_vectorstore():
    """Crea il vectorstore dai documenti"""
    print_step("8.", "Creazione database vettoriale")
    
    if os.path.exists("vectordb") and os.listdir("vectordb"):
        print("✅ Database vettoriale già presente!")
        return True
    
    print("📚 Creazione database vettoriale...")
    print("⏳ Questo processo può richiedere alcuni minuti...")
    
    return run_command(f"{sys.executable} src/creazione_vectorstore.py", "Creazione vectorstore")

def test_system():
    """Test completo del sistema"""
    print_step("9.", "Test del sistema")
    
    try:
        sys.path.append("src")
        from local_embeddings import LocalEmbeddings
        from ollama_llm import OllamaLLM
        print("✅ Import moduli completato!")
        
        # Test embedding
        embedder = LocalEmbeddings()
        test_embedding = embedder.embed_query("test")
        if test_embedding and len(test_embedding) > 0:  # ✅ Migliore controllo
            print("✅ Sistema embedding funzionante!")
        
        # Test Ollama
        llm = OllamaLLM()
        if llm.check_connection():
            print("✅ Connessione Ollama attiva!")
        else:
            print("⚠️ Ollama non risponde - verifica che sia in esecuzione")
            return True  # ✅ Non bloccare per Ollama
            
        print("✅ Tutti i componenti funzionanti!")
        return True
        
    except ImportError as e:
        print(f"❌ Errore import: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Errore nel test: {str(e)}")
        return False

def main():
    print_header("SETUP CHATBOT SEGRETERIA STUDENTI - UNIBG")
    print("Sistema RAG con Mistral 7B + SentenceTransformers + ChromaDB")
    
    if not check_python():
        print("❌ Aggiorna Python alla versione 3.9 o superiore")
        return
    
    steps = [
        ("Ambiente virtuale", create_venv),
        ("Installazione Ollama", install_ollama),
        ("Dipendenze Python", install_python_deps),
        ("Modello Mistral", setup_ollama_model),
        ("Configurazione", setup_environment),
        ("Verifica struttura", check_data_structure),
        ("Estrazione testi", extract_texts),
        ("Database vettoriale", create_vectorstore),
        ("Test sistema", test_system)
    ]
    
    completed = []
    
    for step_name, step_func in steps:
        try:
            if step_func():
                completed.append(step_name)
                print(f"✅ {step_name} - COMPLETATO")
            else:
                print(f"❌ {step_name} - FALLITO")
                break
        except KeyboardInterrupt:
            print("\n⚠️ Setup interrotto dall'utente")
            break
        except Exception as e:
            print(f"❌ Errore in {step_name}: {str(e)}")
            break
    
    # Riepilogo finale
    print_header("RIEPILOGO SETUP")
    print(f"Completati: {len(completed)}/{len(steps)} passaggi")
    
    if len(completed) == len(steps):
        print("🎉 SISTEMA PRONTO!")
        print("\nComandi disponibili:")
        if check_venv():
            print("   python main.py                    # Avvia chatbot CLI")
            print("   start_web.bat                     # Avvia interfaccia web")  # ✅ Aggiunto
        else:
            venv_name = "chatbot_env"
            if platform.system().lower() == "windows":
                print(f"   {venv_name}\\Scripts\\activate      # Attiva ambiente")
            else:
                print(f"   source {venv_name}/bin/activate   # Attiva ambiente")
            print("   python main.py                    # Avvia chatbot CLI")
            print("   start_web.bat                     # Avvia interfaccia web")
        
        print("   python main.py --check           # Verifica sistema")
        print("   python main.py --help            # Mostra aiuto")
    else:
        print(f"\n⚠️ Setup incompleto ({len(completed)}/{len(steps)})")
        print("Risolvi gli errori e riesegui lo setup")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrotto. Riesegui quando pronto.")