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

    print("🚀 RICOSTRUZIONE DATABASE VETTORIALE CON LINK")
    print("=" * 50)
    
    tutti_i_chunks = []
    file_processati = 0
    
    # 1. Processa file FAQ (già ben formattati)
    cartella_faq = "data/FAQ"
    
    if os.path.exists(cartella_faq):
        print(f"\n📁 ELABORAZIONE FAQ da {cartella_faq}")
        for filepath in glob.glob(os.path.join(cartella_faq, "*.txt")):
            filename = os.path.basename(filepath)
            print(f"   📄 {filename}")
            
            with open(filepath, "r", encoding="utf-8") as f:
                testo = f.read()
                
            if testo.strip():
                chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
                # Aggiungi metadata per identificare la fonte
                for i, chunk in enumerate(chunks):
                    tutti_i_chunks.append(f"[FAQ-{filename.replace('.txt', '')}] {chunk}")
                file_processati += 1
                print(f"      ✅ {len(chunks)} chunk estratti")
    else:
        print(f"⚠️ Cartella FAQ {cartella_faq} non trovata")
    
    # 2. Processa file PDF Enhanced (con link migliorati)
    cartella_enhanced = "extracted_text"
    
    if os.path.exists(cartella_enhanced):
        print(f"\n📁 ELABORAZIONE PDF ENHANCED da {cartella_enhanced}")
        for filepath in glob.glob(os.path.join(cartella_enhanced, "*_enhanced.txt")):
            filename = os.path.basename(filepath)
            print(f"   📄 {filename}")
            
            with open(filepath, "r", encoding="utf-8") as f:
                testo = f.read()
                
            if testo.strip():
                chunks = split_text_in_chunks(testo, max_len=1000, overlap=200)
                # Aggiungi metadata per identificare la fonte
                fonte = filename.replace('_enhanced.txt', '')
                for i, chunk in enumerate(chunks):
                    tutti_i_chunks.append(f"[PDF-{fonte}] {chunk}")
                file_processati += 1
                print(f"      ✅ {len(chunks)} chunk estratti")
    else:
        print(f"⚠️ Cartella Enhanced {cartella_enhanced} non trovata")

    # 3. Crea vectorstore
    if tutti_i_chunks:
        print(f"\n📊 RIEPILOGO:")
        print(f"   File processati: {file_processati}")
        print(f"   Chunk totali: {len(tutti_i_chunks)}")
        print(f"\n🔧 Creazione vectorstore...")
        
        vectordb = crea_vectorstore_free(tutti_i_chunks)
        
        # Test funzionalità ricerca
        print(f"\n🧪 Test del database...")
        results = search_vectorstore("segreteria studenti")
        print(f"   ✅ Test completato: {len(results['documents'][0])} risultati trovati")
        
        print(f"\n🎉 DATABASE VETTORIALE COMPLETATO!")
        print(f"   Documenti con link integrati: {len(tutti_i_chunks)}")
    else:
        print("❌ Nessun chunk trovato!")