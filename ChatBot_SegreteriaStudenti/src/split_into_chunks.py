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
        if filename.endswith('.txt'):
            percorso = os.path.join(cartella_estratti, filename)
            with open(percorso, "r", encoding="utf-8") as f:
                testo = f.read()
                
            if testo.strip():
                chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
                tutti_i_chunks.extend(chunks)

    print(f"Processati {len(tutti_i_chunks)} chunk da {len([f for f in os.listdir(cartella_estratti) if f.endswith('.txt')])} file")