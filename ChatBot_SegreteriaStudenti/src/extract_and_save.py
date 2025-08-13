import os
from extract_file import estrai_testo  # usa la funzione già fatta

# Cartelle di input e output
cartella_input = "data/student_guide"
cartella_output = "extracted_text"

os.makedirs(cartella_output, exist_ok=True)  # crea la cartella se non esiste

for nome_file in os.listdir(cartella_input):
    percorso_file = os.path.join(cartella_input, nome_file)
    
    try:
        testo = estrai_testo(percorso_file)
        nome_output = os.path.splitext(nome_file)[0] + "_extract.txt"
        percorso_output = os.path.join(cartella_output, nome_output)

        with open(percorso_output, "w", encoding="utf-8") as f:
            f.write(testo)
        
        print(f"✅ Estratto: {nome_file} → {nome_output}")
    
    except Exception as e:
        print(f"❌ Errore con {nome_file}: {e}")
