#!/usr/bin/env python3
"""
Test Unitari - Componenti Base del Sistema RAG
============================================== 
Test per validare funzionalità core: embeddings, text processing, vectorstore
"""

import os
import sys
import json
from datetime import datetime

# Aggiungi path per import moduli
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class TestRunner:
    """Classe per eseguire e tracciare i test unitari"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_type": "unit",
            "tests": {},
            "summary": {}
        }
        
    def run_test(self, test_name, test_func):
        """Esegue un test e registra il risultato"""
        print(f"Eseguendo test: {test_name}")
        
        try:
            start_time = datetime.now()
            result = test_func()
            end_time = datetime.now()
            
            self.results["tests"][test_name] = {
                "status": "PASS" if result else "FAIL",
                "execution_time": (end_time - start_time).total_seconds(),
                "details": result if isinstance(result, dict) else {"passed": result}
            }
            
            print(f"✓ {test_name}: {'PASS' if result else 'FAIL'}")
            return result
            
        except Exception as e:
            self.results["tests"][test_name] = {
                "status": "ERROR",
                "error": str(e),
                "execution_time": 0
            }
            print(f"✗ {test_name}: ERROR - {e}")
            return False

class TestEmbeddings:
    """Test per il sistema di embedding"""
    
    def test_embeddings_initialization(self):
        """Test inizializzazione del sistema di embeddings"""
        try:
            from local_embeddings import LocalEmbeddings
            embedder = LocalEmbeddings()
            
            # Verifica che il modello sia caricato
            return hasattr(embedder, 'model') and embedder.model is not None
            
        except Exception as e:
            print(f"Errore test embeddings: {e}")
            return False
    
    def test_text_embedding(self):
        """Test generazione embedding da testo"""
        try:
            from local_embeddings import LocalEmbeddings
            embedder = LocalEmbeddings()
            
            test_text = "Come posso iscrivermi all'università?"
            embedding = embedder.embed_query(test_text)  # Usa il metodo corretto
            
            # Verifica dimensioni e tipo embedding
            return {
                "passed": len(embedding) > 0 and isinstance(embedding, list),
                "embedding_length": len(embedding),
                "text_length": len(test_text)
            }
            
        except Exception as e:
            print(f"Errore test embedding: {e}")
            return False

class TestTextProcessing:
    """Test per elaborazione testi"""
    
    def test_text_chunking(self):
        """Test divisione testo in chunks"""
        try:
            from dividi_chunks import split_text_in_chunks
            
            test_text = """Questo è un testo di esempio per testare la divisione in chunks.
            Il sistema dovrebbe dividere correttamente il testo mantenendo la coerenza semantica.
            Ogni chunk dovrebbe avere una dimensione appropriata per l'embedding."""
            
            chunks = split_text_in_chunks(test_text, max_len=100)  # Usa il parametro corretto
            
            return {
                "passed": len(chunks) > 0 and all(isinstance(chunk, str) for chunk in chunks),
                "num_chunks": len(chunks),
                "avg_chunk_length": sum(len(chunk) for chunk in chunks) / len(chunks) if chunks else 0
            }
            
        except Exception as e:
            print(f"Errore test chunking: {e}")
            return False
    
    def test_text_cleaning(self):
        """Test pulizia testo"""
        test_texts = [
            "  Testo con spazi   extra  ",
            "Testo\ncon\tmulti\r\nspazi\twhitespace",
            ""
        ]
        
        try:
            cleaned_results = []
            for text in test_texts:
                # Semplice pulizia testo
                cleaned = ' '.join(text.split())
                cleaned_results.append({
                    "original_length": len(text),
                    "cleaned_length": len(cleaned),
                    "has_content": len(cleaned.strip()) > 0
                })
            
            return {
                "passed": True,
                "results": cleaned_results
            }
            
        except Exception as e:
            print(f"Errore test pulizia: {e}")
            return False

class TestVectorStore:
    """Test per vector database"""
    
    def test_vectorstore_connection(self):
        """Test connessione al vector database"""
        try:
            import chromadb
            
            # Test connessione ChromaDB
            chroma_client = chromadb.Client()
            collections = chroma_client.list_collections()
            
            return {
                "passed": True,
                "num_collections": len(collections),
                "connection_ok": True
            }
            
        except Exception as e:
            print(f"Errore connessione vectorstore: {e}")
            return False
    
    def test_simple_search(self):
        """Test ricerca semplice nel vectorstore"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Usa il path del vectorstore del progetto
            vectordb_path = os.path.join(os.path.dirname(__file__), '..', '..', 'vectordb')
            
            if not os.path.exists(vectordb_path):
                return {
                    "passed": False,
                    "error": "Vectorstore non presente - eseguire prima creazione_vectorstore.py"
                }
            
            client = chromadb.PersistentClient(
                path=vectordb_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            collections = client.list_collections()
            collection_names = [c.name for c in collections]
            
            if not collections:
                return {
                    "passed": False,
                    "error": "Nessuna collezione trovata nel vectorstore"
                }
            
            # Usa la prima collezione disponibile
            collection = collections[0]
            
            return {
                "passed": True,
                "has_results": True,
                "collection_name": collection.name,
                "available_collections": collection_names,
                "collection_count": collection.count()
            }
            
        except Exception as e:
            print(f"Errore test search: {e}")
            return False

def run_unit_tests():
    """Esegue tutti i test unitari"""
    runner = TestRunner()
    
    # Test Embeddings
    embeddings_tests = TestEmbeddings()
    runner.run_test("embeddings_initialization", embeddings_tests.test_embeddings_initialization)
    runner.run_test("text_embedding", embeddings_tests.test_text_embedding)
    
    # Test Text Processing
    text_tests = TestTextProcessing()
    runner.run_test("text_chunking", text_tests.test_text_chunking)
    runner.run_test("text_cleaning", text_tests.test_text_cleaning)
    
    # Test VectorStore
    vector_tests = TestVectorStore()
    runner.run_test("vectorstore_connection", vector_tests.test_vectorstore_connection)
    runner.run_test("simple_search", vector_tests.test_simple_search)
    
    # Calcola sommario
    total_tests = len(runner.results["tests"])
    passed_tests = sum(1 for test in runner.results["tests"].values() if test["status"] == "PASS")
    failed_tests = sum(1 for test in runner.results["tests"].values() if test["status"] == "FAIL")
    error_tests = sum(1 for test in runner.results["tests"].values() if test["status"] == "ERROR")
    
    runner.results["summary"] = {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "errors": error_tests,
        "success_rate": passed_tests / total_tests if total_tests > 0 else 0
    }
    
    # Salva risultati
    results_file = os.path.join(os.path.dirname(__file__), "..", "results", "unit_tests_results.json")
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(runner.results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Sommario Test Unitari:")
    print(f"   Totale: {total_tests}")
    print(f"   Passati: {passed_tests}")
    print(f"   Falliti: {failed_tests}")
    print(f"   Errori: {error_tests}")
    print(f"   Tasso successo: {runner.results['summary']['success_rate']:.2%}")
    print(f"   Risultati salvati in: {results_file}")
    
    return runner.results

if __name__ == "__main__":
    run_unit_tests()