import os
from extract_file import estrai_testo  # usa la funzione già fatta

def process_all_documents():
    """Processa tutti i documenti dalle cartelle FAQ e student_guide"""
    
    # Cartelle di input e output
    cartelle_input = ["data/FAQ", "data/student_guide"]
    cartella_output = "extracted_text"
    
    os.makedirs(cartella_output, exist_ok=True)  # crea la cartella se non esiste
    
    total_processed = 0
    total_errors = 0
    
    for cartella_input in cartelle_input:
        if not os.path.exists(cartella_input):
            print(f"⚠️ Cartella {cartella_input} non trovata, skip...")
            continue
            
        print(f"Processando documenti in: {cartella_input}")
        
        for nome_file in os.listdir(cartella_input):
            percorso_file = os.path.join(cartella_input, nome_file)
            
            # Salta le directory
            if os.path.isdir(percorso_file):
                continue
            
            try:
                testo = estrai_testo(percorso_file)
                nome_output = os.path.splitext(nome_file)[0] + "_extract.txt"
                percorso_output = os.path.join(cartella_output, nome_output)

                with open(percorso_output, "w", encoding="utf-8") as f:
                    f.write(testo)
                
                print(f"✅ Estratto: {nome_file} → {nome_output}")
                total_processed += 1
            
            except Exception as e:
                print(f"❌ Errore con {nome_file}: {e}")
                total_errors += 1
    
    print(f"\nRiepilogo: {total_processed} file processati, {total_errors} errori")
    return total_processed > 0

if __name__ == "__main__":
    process_all_documents()