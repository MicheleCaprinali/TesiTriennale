import os

def split_text_in_chunks(text, max_len=1000):
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

    for filename in os.listdir(cartella_estratti):
        percorso = os.path.join(cartella_estratti, filename)
        with open(percorso, "r", encoding="utf-8") as f:
            testo = f.read()
            chunks = split_text_in_chunks(testo, max_len=1000)
            print(f"File '{filename}' suddiviso in {len(chunks)} chunk.")
            tutti_i_chunks.extend(chunks)

    print(f"\nTotale chunk creati da tutti i file: {len(tutti_i_chunks)}")