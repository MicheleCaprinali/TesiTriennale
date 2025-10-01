import os
import glob
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

from local_embeddings import LocalEmbeddings
from dividi_chunks import split_text_in_chunks

load_dotenv()


def clean_text(text: str) -> str:
    """Normalizza spazi e ritorni a capo per migliorare consistenza vettoriale"""
    return " ".join(text.split())


def crea_vectorstore_free(chunk_list, persist_dir="vectordb"):
    """Crea database vettoriale usando ChromaDB e SentenceTransformers per embedding locali"""
    print(f"Creazione vectorstore in {persist_dir}...")

    embedder = LocalEmbeddings()

    # Configura ChromaDB
    client = chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(anonymized_telemetry=False),
    )

    # Nome della collection
    collection_name = os.getenv("VECTORDB_COLLECTION", "unibg_docs")

    try:
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' esistente rimossa")
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "Documenti UniBg per chatbot"},
    )

    print(f"Preparazione di {len(chunk_list)} chunk...")

    embeddings = embedder.embed_documents(chunk_list)

    ids = [f"{collection_name}_chunk_{i}" for i in range(len(chunk_list))]

    print("Salvataggio nel vectorstore...")
    collection.add(
        documents=chunk_list,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": f"chunk_{i}"} for i in range(len(chunk_list))],
    )

    print(f"Vectorstore creato con {len(chunk_list)} documenti!")
    print(f"Percorso: {os.path.abspath(persist_dir)}")

    return collection


def search_vectorstore(query, persist_dir="vectordb", k=5, embedder=None):
    """Esegue ricerca semantica nel database vettoriale esistente"""
    if embedder is None:
        embedder = LocalEmbeddings()

    client = chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(anonymized_telemetry=False)
    )
    collection_name = os.getenv("VECTORDB_COLLECTION", "unibg_docs")
    collection = client.get_collection(collection_name)

    query_embedding = embedder.embed_query(query)

    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cartella_faq = os.path.join(BASE_DIR, "../data/FAQ")
    cartella_estratti = os.path.join(BASE_DIR, "../data/testi_estratti")

    print("CREAZIONE DATABASE VETTORIALE")
    print("=" * 50)

    tutti_i_chunks = []
    file_processati = 0

    # 1. Processa file FAQ
    if os.path.exists(cartella_faq):
        print(f"\nELABORAZIONE FAQ da {cartella_faq}")
        for filepath in glob.glob(os.path.join(cartella_faq, "*.txt")):
            filename = os.path.basename(filepath)
            print(f"   {filename}")

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    testo = clean_text(f.read())

                if testo:
                    chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
                    for i, chunk in enumerate(chunks):
                        tutti_i_chunks.append(f"[FAQ-{filename.replace('.txt', '')}] {chunk}")
                    file_processati += 1
                    print(f"      {len(chunks)} chunk estratti")
            except Exception as e:
                print(f"      Errore nel processare {filename}: {e}")
    else:
        print(f"Cartella FAQ {cartella_faq} non trovata")

    # 2. Processa file PDF estratti
    if os.path.exists(cartella_estratti):
        print(f"\nELABORAZIONE PDF ESTRATTI da {cartella_estratti}")
        for filepath in glob.glob(os.path.join(cartella_estratti, "*_extracted.txt")):
            filename = os.path.basename(filepath)
            print(f"   {filename}")

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    testo = clean_text(f.read())

                if testo:
                    chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
                    fonte = filename.replace("_extracted.txt", "")
                    for i, chunk in enumerate(chunks):
                        tutti_i_chunks.append(f"[PDF-{fonte}] {chunk}")
                    file_processati += 1
                    print(f"      {len(chunks)} chunk estratti")
            except Exception as e:
                print(f"      Errore nel processare {filename}: {e}")
    else:
        print(f"Cartella estratti {cartella_estratti} non trovata")

    # 3. Crea vectorstore
    if tutti_i_chunks:
        print(f"\nRIEPILOGO:")
        print(f"   File processati: {file_processati}")
        print(f"   Chunk totali: {len(tutti_i_chunks)}")
        print(f"\nCreazione vectorstore...")

        try:
            vectordb = crea_vectorstore_free(tutti_i_chunks)
            print(f"\nDATABASE VETTORIALE COMPLETATO!")
            print(f"   Documenti salvati: {len(tutti_i_chunks)}")
            
        except Exception as e:
            print(f"Errore nella creazione del vectorstore: {e}")
    else:
        print("Nessun chunk trovato!")