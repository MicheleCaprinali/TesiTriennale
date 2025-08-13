import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def crea_vectorstore(chunk_list, persist_dir="vectordb"):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(chunk_list, embeddings, persist_directory=persist_dir)
    vectordb.persist()
    print(f"✅ Vectorstore creato e salvato in '{persist_dir}'")
    return vectordb

if __name__ == "__main__":
    # Qui importa i chunk dal passo precedente o rilegge da file
    # Per semplicità riuso lo split nel codice
    from split_into_chunks import split_text_in_chunks
    import glob

    cartella_estratti = "extracted_text"
    tutti_i_chunks = []

    for filepath in glob.glob(os.path.join(cartella_estratti, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            testo = f.read()
            chunks = split_text_in_chunks(testo, max_len=1000)
            tutti_i_chunks.extend(chunks)

    vectordb = crea_vectorstore(tutti_i_chunks)
