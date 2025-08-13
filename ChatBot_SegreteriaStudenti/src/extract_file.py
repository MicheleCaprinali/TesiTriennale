import os

def estrai_testo(percorso):
    estensione = os.path.splitext(percorso)[1].lower()
    
    if estensione == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(percorso)
        testo = ""
        for pagina in reader.pages:
            testo += pagina.extract_text()
        return testo
    
    elif estensione == ".txt":
        with open(percorso, "r", encoding="utf-8") as f:
            return f.read()
    
    else:
        raise ValueError(f"Formato file non supportato: {estensione}")

if __name__ == "__main__":
    percorso_file = "data/FAQ/carriera.txt"
    try:
        print(f"📂 Tentativo di lettura del file: {percorso_file}")
        testo = estrai_testo(percorso_file)
        print(f"📏 Lunghezza del testo estratto: {len(testo)} caratteri")
        if testo.strip():
            print("✅ Testo estratto con successo! Ecco un'anteprima:")
            print("-" * 50)
            print(testo[:1000])
            print("-" * 50)
        else:
            print("⚠️ Il file è vuoto o non contiene testo utile.")
    except Exception as e:
        print(f"❌ Errore: {e}")