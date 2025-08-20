import os
import chromadb
from chromadb.config import Settings
from local_embeddings import LocalEmbeddings
from dotenv import load_dotenv

load_dotenv()

def crea_vectorstore_free(chunk_list, persist_dir="vectordb"):
    """
    Crea vectorstore usando ChromaDB e Sentence Transformers
    """
    print(f"Creazione vectorstore in {persist_dir}...")
    
    embedder = LocalEmbeddings()
    
    # Configura ChromaDB
    client = chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(
            anonymized_telemetry=False
        )
    )
    
    # Nome della collection
    collection_name = os.getenv('VECTORDB_COLLECTION', 'unibg_docs')
    
    try:
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' esistente rimossa")
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "Documenti UniBg per chatbot"}
    )
    
    print(f"Preparazione di {len(chunk_list)} chunk...")
    
    embeddings = embedder.embed_documents(chunk_list)
    
    ids = [f"chunk_{i}" for i in range(len(chunk_list))]
    
    print("Salvataggio nel vectorstore...")
    collection.add(
        documents=chunk_list,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": f"chunk_{i}"} for i in range(len(chunk_list))]
    )
    
    print(f"✅ Vectorstore creato con {len(chunk_list)} documenti!")
    print(f"Percorso: {os.path.abspath(persist_dir)}")
    
    return collection

def search_vectorstore(query, persist_dir="vectordb", k=5, embedder=None):
    """
    Cerca nel vectorstore esistente
    """
    if embedder is None:
        embedder = LocalEmbeddings()
    
    # Connetti a ChromaDB esistente
    client = chromadb.PersistentClient(path=persist_dir)
    collection_name = os.getenv('VECTORDB_COLLECTION', 'unibg_docs')
    collection = client.get_collection(collection_name)
    
    # Crea embedding per la query
    query_embedding = embedder.embed_query(query)
    
    # Cerca documenti simili
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    return results

if __name__ == "__main__":
    from split_into_chunks import split_text_in_chunks
    import glob

    cartella_estratti = "extracted_text"
    
    if not os.path.exists(cartella_estratti):
        print(f"❌ Cartella {cartella_estratti} non trovata!")
        print("Esegui prima extract_and_save.py")
        exit(1)
    
    tutti_i_chunks = []
    
    for filepath in glob.glob(os.path.join(cartella_estratti, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            testo = f.read()
            
        if testo.strip():
            chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
            tutti_i_chunks.extend(chunks)

    if tutti_i_chunks:
        print(f"Creazione vectorstore con {len(tutti_i_chunks)} chunk...")
        vectordb = crea_vectorstore_free(tutti_i_chunks)
        
        # Test funzionalità ricerca
        results = search_vectorstore("test query")
        print(f"Test completato: {len(results['documents'][0])} risultati trovati")
    else:
        print("❌ Nessun chunk trovato!")