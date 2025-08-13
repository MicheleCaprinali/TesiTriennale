#!/usr/bin/env python3
"""
Test del sistema RAG - Solo retrieval (senza LLM per ora)
"""

import os
import sys
sys.path.append("src")

from local_embeddings import LocalEmbeddings
from create_vectorstore import search_vectorstore

def test_retrieval_system():
    """Testa il sistema di retrieval semantico"""
    print("🧪 TEST SISTEMA RAG - RETRIEVAL")
    print("=" * 50)
    
    try:
        # Test queries di esempio
        test_queries = [
            "Come faccio a iscrivermi agli esami?",
            "Quando devo pagare le tasse universitarie?",
            "Come richiedo un certificato di laurea?",
            "Quali sono gli orari della segreteria?",
            "Come funziona il servizio disabilità?"
        ]
        
        print(f"🔍 Test con {len(test_queries)} query di esempio\n")
        
        for i, query in enumerate(test_queries, 1):
            print(f"Query {i}: '{query}'")
            print("-" * 40)
            
            # Cerca documenti pertinenti
            results = search_vectorstore(query, k=3)
            
            if results and 'documents' in results and results['documents']:
                documents = results['documents'][0]
                distances = results.get('distances', [[]])[0]
                
                print(f"✅ Trovati {len(documents)} documenti pertinenti:")
                
                for j, (doc, dist) in enumerate(zip(documents, distances)):
                    similarity = 1 - dist  # Converte distanza in similarità
                    print(f"\n📄 Documento {j+1} (Similarità: {similarity:.2f}):")
                    print(f"   {doc[:200]}...")
                    
            else:
                print("❌ Nessun documento trovato")
                
            print("\n" + "="*80 + "\n")
    
    except Exception as e:
        print(f"❌ Errore nel test: {str(e)}")
        return False
    
    return True

def interactive_search():
    """Modalità interattiva per testare ricerche personalizzate"""
    print("🔍 MODALITÀ RICERCA INTERATTIVA")
    print("=" * 40)
    print("💡 Scrivi una domanda per testare la ricerca semantica")
    print("🚪 Digita 'exit' per uscire\n")
    
    while True:
        query = input("🔍 Domanda > ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("👋 Test completato!")
            break
            
        if not query:
            continue
            
        try:
            print(f"\n🔍 Ricerca per: '{query}'")
            results = search_vectorstore(query, k=5)
            
            if results and 'documents' in results and results['documents']:
                documents = results['documents'][0]
                distances = results.get('distances', [[]])[0]
                
                print(f"✅ Trovati {len(documents)} documenti:")
                
                for i, (doc, dist) in enumerate(zip(documents[:3], distances[:3])):
                    similarity = 1 - dist
                    print(f"\n📄 Risultato {i+1} (Similarità: {similarity:.2f}):")
                    print(f"   {doc[:300]}...")
                    
            else:
                print("❌ Nessun documento trovato")
                
        except Exception as e:
            print(f"❌ Errore: {str(e)}")
        
        print("\n" + "-" * 60)

def main():
    print("🎓 CHATBOT UNIBG - TEST RETRIEVAL SYSTEM")
    print("⚡ Versione senza LLM per testare il retrieval")
    print("=" * 60)
    
    # Verifica che il vectorstore esista
    if not os.path.exists("vectordb"):
        print("❌ VectorStore non trovato!")
        print("💡 Esegui prima: python src/create_vectorstore.py")
        return
    
    try:
        # Test automatico
        if test_retrieval_system():
            print("✅ Test automatico completato con successo!\n")
            
            # Modalità interattiva
            response = input("🤔 Vuoi testare ricerche personalizzate? (y/n): ")
            if response.lower().startswith('y'):
                interactive_search()
        else:
            print("❌ Test automatico fallito!")
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrotto dall'utente")
    except Exception as e:
        print(f"❌ Errore generale: {str(e)}")

if __name__ == "__main__":
    main()
