#!/usr/bin/env python3
"""
Setup automatico ChatBot Segreteria Studenti UniBg
Sistema RAG con Mistral 7B + SentenceTransformers + ChromaDB
"""

import os
import sys
import subprocess
import platform
import time

def print_header(title):
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

def print_step(step, description):
    print(f"\n{step} {description}")

def run_command(command, description, check=True):
    """Esegue un comando e mostra il risultato"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] {description}")
            return True
        else:
            if check:
                print(f"[ERRORE] {description}")
                if result.stderr.strip():
                    print(f"Dettagli: {result.stderr.strip()}")
                return False
            else:
                print(f"[WARN] {description} - continuo")
                return True
    except Exception as e:
        print(f"[ERRORE] Comando fallito: {str(e)}")
        return False

def check_python():
    """Verifica versione Python"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"[ERRORE] Python {version.major}.{version.minor} - Richiede 3.9+")
        return False
def check_venv():
    """Verifica ambiente virtuale"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print(f"[OK] Ambiente virtuale attivo")
        return True
    else:
        print("[INFO] Nessun ambiente virtuale rilevato")
        return False

def create_venv():
    """Crea ambiente virtuale"""
    print_step("1.", "Setup ambiente virtuale")
    
    venv_name = "chatbot_env"
    
    if check_venv():
        return True
    
    if os.path.exists(venv_name):
        print(f"[OK] Ambiente virtuale '{venv_name}' già presente")
        if platform.system().lower() == "windows":
            print(f"Per attivarlo: {venv_name}\\Scripts\\activate")
        else:
            print(f"Per attivarlo: source {venv_name}/bin/activate")
        
        choice = input("\nContinuare senza ambiente virtuale? (s/N): ").lower()
        if choice != 's':
            print("[INFO] Attiva l'ambiente virtuale e riesegui setup")
            return False
        return True
    
    print(f"[INFO] Creazione ambiente virtuale '{venv_name}'...")
    if not run_command(f"{sys.executable} -m venv {venv_name}", "Creazione ambiente virtuale"):
        return False
    
    print("\n" + "="*50)
    print(" ATTIVA L'AMBIENTE VIRTUALE")
    print("="*50)
    
    if platform.system().lower() == "windows":
        activate_cmd = f"{venv_name}\\Scripts\\activate"
    else:
        activate_cmd = f"source {venv_name}/bin/activate"
    
    print(f"1. Esegui: {activate_cmd}")
    print(f"2. Riesegui: python setup.py")
    print("="*50)
    
    return False

def install_ollama():
    """Verifica e installa Ollama"""
    print_step("2.", "Configurazione Ollama")

    if run_command("ollama --version", "Verifica Ollama", check=False):
        print("[OK] Ollama già installato")
        return True
    
    print("[INFO] Ollama non trovato")
    system = platform.system().lower()
    
    if system == "windows":
        print("Scarica da: https://ollama.ai/download/windows")
        input("Premi INVIO dopo aver installato Ollama...")
        return run_command("ollama --version", "Verifica Ollama")
        
    elif system == "darwin":
        return run_command("brew install ollama", "Installazione Ollama")
        
    elif system == "linux":
        return run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installazione Ollama")
    
    else:
        print(f"[ERRORE] Sistema {system} non supportato")
        return False

def install_python_deps():
    """Installa dipendenze Python"""
    print_step("3.", "Installazione dipendenze Python")
    
    if not os.path.exists("requirements.txt"):
        print("[ERRORE] File requirements.txt non trovato")
        return False
    
    if not check_venv():
        print("[WARN] Ambiente virtuale non attivo")
        choice = input("Continuare? (s/N): ").lower()
        if choice != 's':
            return False
    
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Aggiornamento pip", check=False)
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installazione pacchetti"
    )

def setup_ollama_model():
    """Setup modello Mistral"""
    print_step("4.", "Setup modello Mistral 7B")

    print("[INFO] Verifica servizio Ollama...")
    if not run_command("ollama list", "Verifica servizio", check=False):
        print("[INFO] Avvio servizio Ollama...")
        if platform.system().lower() == "windows":
            subprocess.Popen(["ollama", "serve"], shell=True)
        else:
            subprocess.Popen(["ollama", "serve"])
        
        time.sleep(5)
    
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if "mistral" in result.stdout:
        print("[OK] Modello Mistral già presente")
        return True
    
    print("[INFO] Download modello Mistral 7B (~4GB)...")
    return run_command("ollama pull mistral:7b", "Download Mistral")

def setup_environment():
    """Setup configurazione"""
    print_step("5.", "Configurazione ambiente")
    
    if os.path.exists(".env"):
        print("[OK] File .env già presente")
        return True
    
    env_content = """# Configurazione ChatBot Segreteria Studenti UniBg
EMBEDDING_MODEL=all-MiniLM-L6-v2
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b
TEMPERATURE=0.1
VECTORDB_COLLECTION=unibg_docs
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("[OK] File .env creato")
        return True
    except Exception as e:
        print(f"[ERRORE] Creazione .env fallita: {str(e)}")
        return False

def check_data_structure():
    """Verifica struttura progetto"""
    print_step("6.", "Verifica struttura progetto")
    
    required_dirs = ["data", "src", "interfaccia"]
    required_files = [
        "src/local_embeddings.py",
        "src/ollama_llm.py", 
        "src/creazione_vectorstore.py",
        "main.py"
    ]
    
    missing = []
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing.append(f"Cartella: {dir_name}")
    
    for file_name in required_files:
        if not os.path.exists(file_name):
            missing.append(f"File: {file_name}")
    
    if missing:
        print("[ERRORE] Elementi mancanti:")
        for item in missing:
            print(f"   - {item}")
        return False
    
    print("[OK] Struttura progetto completa")
    return True

def extract_texts():
    """Estrae testi dai PDF"""
    print_step("7.", "Estrazione testi documenti")
    
    if os.path.exists("data/testi_estratti") and os.listdir("data/testi_estratti"):
        print("[OK] Testi già estratti")
        return True
    
    if not os.path.exists("data"):
        print("[ERRORE] Cartella 'data' non trovata")
        return False
    
    return run_command(f"{sys.executable} src/testi_estratti.py", "Estrazione documenti")

def create_vectorstore():
    """Crea database vettoriale"""
    print_step("8.", "Creazione database vettoriale")
    
    if os.path.exists("vectordb") and os.listdir("vectordb"):
        print("[OK] Database vettoriale già presente")
        return True
    
    print("[INFO] Creazione database vettoriale...")
    return run_command(f"{sys.executable} src/creazione_vectorstore.py", "Creazione vectorstore")

def test_system():
    """Test sistema"""
    print_step("9.", "Test sistema")
    
    try:
        sys.path.append("src")
        from local_embeddings import LocalEmbeddings
        from ollama_llm import OllamaLLM
        print("[OK] Import moduli completato")
        
        embedder = LocalEmbeddings()
        test_embedding = embedder.embed_query("test")
        if test_embedding and len(test_embedding) > 0:
            print("[OK] Sistema embedding funzionante")
        
        llm = OllamaLLM()
        if hasattr(llm, 'check_connection') and llm.check_connection():
            print("[OK] Connessione Ollama attiva")
        else:
            print("[WARN] Ollama non risponde")
            
        print("[OK] Sistema funzionante")
        return True
        
    except ImportError as e:
        print(f"[ERRORE] Import fallito: {str(e)}")
        return False
    except Exception as e:
        print(f"[ERRORE] Test fallito: {str(e)}")
        return False

def main():
    print_header("SETUP CHATBOT SEGRETERIA STUDENTI - UNIBG")
    
    if not check_python():
        print("[ERRORE] Aggiorna Python alla versione 3.13+")
        return
    
    steps = [
        ("Ambiente virtuale", create_venv),
        ("Configurazione Ollama", install_ollama),
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
                print(f"[OK] {step_name} completato")
            else:
                print(f"[ERRORE] {step_name} fallito")
                break
        except KeyboardInterrupt:
            print("\n[INFO] Setup interrotto")
            break
        except Exception as e:
            print(f"[ERRORE] {step_name}: {str(e)}")
            break
    
    print_header("RIEPILOGO SETUP")
    print(f"Completati: {len(completed)}/{len(steps)} passaggi")
    
    if len(completed) == len(steps):
        print("[OK] SISTEMA PRONTO")
        print("\nComandi disponibili:")
        if check_venv():
            print("   python main.py                    # Chatbot CLI")
            print("   streamlit run interfaccia/streamlit.py  # Interfaccia web")
        else:
            venv_name = "chatbot_env"
            if platform.system().lower() == "windows":
                print(f"   {venv_name}\\Scripts\\activate      # Attiva ambiente")
            else:
                print(f"   source {venv_name}/bin/activate   # Attiva ambiente")
            print("   python main.py                    # Chatbot CLI")
        
        print("   python main.py --check           # Verifica sistema")
    else:
        print(f"[WARN] Setup incompleto ({len(completed)}/{len(steps)})")
        print("Risolvi gli errori e riesegui setup")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup interrotto")