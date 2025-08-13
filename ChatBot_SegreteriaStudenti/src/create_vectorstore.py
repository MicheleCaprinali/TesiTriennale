import os
import chromadb
from chromadb.config import Settings
from local_embeddings import LocalEmbeddings
from dotenv import load_dotenv

load_dotenv()

def crea_vectorstore_free(chunk_list, persist_dir="vectordb"):
    """
    Crea vectorstore usando ChromaDB e Sentence Transformers (tutto gratuito)
    """
    print(f"🔄 Creazione vectorstore in {persist_dir}...")
    
    # Inizializza embedding locale
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
    
    # Cancella collection esistente se presente
    try:
        client.delete_collection(collection_name)
        print(f"🗑️  Collection '{collection_name}' esistente rimossa")
    except:
        pass
    
    # Crea nuova collection
    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "Documenti UniBG per chatbot"}
    )
    
    # Prepara i dati per ChromaDB
    print(f"📊 Preparazione di {len(chunk_list)} chunk...")
    
    # Crea embedding per tutti i chunk
    embeddings = embedder.embed_documents(chunk_list)
    
    # Crea ID univoci per ogni chunk
    ids = [f"chunk_{i}" for i in range(len(chunk_list))]
    
    # Aggiungi i documenti alla collection
    print("💾 Salvataggio nel vectorstore...")
    collection.add(
        documents=chunk_list,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": f"chunk_{i}"} for i in range(len(chunk_list))]
    )
    
    print(f"✅ Vectorstore creato con {len(chunk_list)} documenti!")
    print(f"📍 Percorso: {os.path.abspath(persist_dir)}")
    
    return collection

def search_vectorstore(query, persist_dir="vectordb", k=5):
    """
    Cerca nel vectorstore esistente
    """
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
    # Crea vectorstore dai file estratti
    from split_into_chunks import split_text_in_chunks
    import glob

    cartella_estratti = "extracted_text"
    
    if not os.path.exists(cartella_estratti):
        print(f"❌ Cartella {cartella_estratti} non trovata!")
        print("💡 Esegui prima extract_and_save.py")
        exit(1)
    
    tutti_i_chunks = []
    
    print("📂 Caricamento file estratti...")
    for filepath in glob.glob(os.path.join(cartella_estratti, "*.txt")):
        filename = os.path.basename(filepath)
        print(f"📄 Processando: {filename}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            testo = f.read()
            
        if not testo.strip():
            print(f"⚠️  File {filename} è vuoto, skip...")
            continue
            
        chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
        print(f"   └─ {len(chunks)} chunk creati")
        tutti_i_chunks.extend(chunks)

    print(f"\n📊 Totale chunk da processare: {len(tutti_i_chunks)}")
    
    if tutti_i_chunks:
        vectordb = crea_vectorstore_free(tutti_i_chunks)
        
        # Test di ricerca
        print("\n🔍 Test ricerca...")
        test_query = "come iscriversi agli esami"
        results = search_vectorstore(test_query)
        
        print(f"Query: '{test_query}'")
        print(f"Risultati trovati: {len(results['documents'][0])}")
        
        for i, doc in enumerate(results['documents'][0][:3]):
            print(f"\n📄 Risultato {i+1}:")
            print(f"   {doc[:200]}...")
    else:
        print("❌ Nessun chunk trovato!")
