import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_in_chunks(text, max_len=1000, overlap=200):
    """
    Suddivide il testo in chunk con overlap usando RecursiveCharacterTextSplitter
    per mantenere la coerenza semantica
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_len,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", "? ", "! ", " "]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks

def split_text_in_chunks_simple(text, max_len=1000):
    """Versione semplificata per compatibilità"""
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start+max_len]
        chunks.append(chunk)
        start += max_len
    return chunks

if __name__ == "__main__":
    cartella_estratti = "extracted_text"
    tutti_i_chunks = []

    if not os.path.exists(cartella_estratti):
        print(f"❌ Cartella {cartella_estratti} non trovata!")
        exit(1)

    for filename in os.listdir(cartella_estratti):
        if not filename.endswith('.txt'):
            continue
            
        percorso = os.path.join(cartella_estratti, filename)
        with open(percorso, "r", encoding="utf-8") as f:
            testo = f.read()
            
        if not testo.strip():
            print(f"⚠️  File {filename} è vuoto, skip...")
            continue
            
        chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
        print(f"📄 File '{filename}' suddiviso in {len(chunks)} chunk.")
        tutti_i_chunks.extend(chunks)

    print(f"\n📊 Totale chunk creati da tutti i file: {len(tutti_i_chunks)}")
    
    # Statistiche sui chunk
    if tutti_i_chunks:
        lunghezze = [len(chunk) for chunk in tutti_i_chunks]
        print(f"📏 Lunghezza media chunk: {sum(lunghezze) / len(lunghezze):.0f} caratteri")
        print(f"📏 Chunk più corto: {min(lunghezze)} caratteri")
        print(f"📏 Chunk più lungo: {max(lunghezze)} caratteri")