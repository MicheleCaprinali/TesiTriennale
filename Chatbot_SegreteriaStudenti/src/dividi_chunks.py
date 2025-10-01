import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_in_chunks(text, max_len=1000, overlap=200):
    """Suddivide il testo in chunk semanticamente coerenti usando RecursiveCharacterTextSplitter"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_len,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", "? ", "! ", " "]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks

def split_text_in_chunks_simple(text, max_len=1000):
    """Versione semplificata di chunking per sistemi senza LangChain"""
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start+max_len]
        chunks.append(chunk)
        start += max_len
    return chunks

def save_chunks_to_file(chunks, output_file):
    """Salva i chunks generati in un file per debug e verifica qualità"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            f.write(f"=== CHUNK {i+1} ===\n")
            f.write(chunk)
            f.write(f"\n{'='*50}\n\n")

if __name__ == "__main__":
    # Configurazione percorsi basata sulla struttura del progetto
    cartella_estratti = "../data/testi_estratti"
    output_chunks_file = "../data/chunks_debug.txt"
    tutti_i_chunks = []

    if not os.path.exists(cartella_estratti):
        print(f"Cartella {cartella_estratti} non trovata!")
        exit(1)

    print(f"Processando file da: {cartella_estratti}")
    
    file_processati = 0
    for filename in os.listdir(cartella_estratti):
        if filename.endswith('.txt'):
            percorso = os.path.join(cartella_estratti, filename)
            print(f"Elaborando: {filename}")
            
            try:
                with open(percorso, "r", encoding="utf-8") as f:
                    testo = f.read()
                
                if testo.strip():
                    try:
                        # Prova prima con RecursiveCharacterTextSplitter
                        chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
                    except ImportError:
                        print("LangChain non disponibile, uso chunking semplice")
                        chunks = split_text_in_chunks_simple(testo, max_len=1000)
                    
                    tutti_i_chunks.extend(chunks)
                    file_processati += 1
                    print(f"   {len(chunks)} chunks creati")
                else:
                    print(f"   File vuoto: {filename}")
                    
            except Exception as e:
                print(f"   Errore nel processare {filename}: {e}")

    print(f"\nElaborazione completata:")
    print(f"   File processati: {file_processati}")
    print(f"   Chunks totali: {len(tutti_i_chunks)}")
    
    if tutti_i_chunks:
        # Salva i chunks per debug
        save_chunks_to_file(tutti_i_chunks, output_chunks_file)
        print(f"   Chunks salvati in: {output_chunks_file}")
        
        # Statistiche sui chunks
        lunghezze = [len(chunk) for chunk in tutti_i_chunks]
        print(f"   Lunghezza media chunk: {sum(lunghezze)/len(lunghezze):.0f} caratteri")
        print(f"   Chunk più corto: {min(lunghezze)} caratteri")
        print(f"   Chunk più lungo: {max(lunghezze)} caratteri")
    else:
        print("   Nessun chunk generato!")