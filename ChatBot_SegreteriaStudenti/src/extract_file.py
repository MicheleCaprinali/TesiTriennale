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
        testo = estrai_testo(percorso_file)
        print(f"Estratti {len(testo)} caratteri da {percorso_file}")
        print(testo[:200] + "..." if len(testo) > 200 else testo)
    except Exception as e:
        print(f"❌ Errore: {e}")