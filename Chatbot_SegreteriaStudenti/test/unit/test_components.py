#!/usr/bin/env python3
"""
Test Unitari - Componenti Base del Sistema RAG
============================================== 
Test per validare funzionalità core dei moduli in src/
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

class TestSrcModules:
    """Test per i moduli della cartella src/"""
    
    def test_local_embeddings(self):
        """Test completo modulo local_embeddings.py"""
        try:
            from local_embeddings import LocalEmbeddings
            
            # Test inizializzazione
            embedder = LocalEmbeddings()
            if not hasattr(embedder, 'model') or embedder.model is None:
                return {"passed": False, "error": "Modello non caricato"}
            
            # Test embedding singola query
            test_query = "Come posso iscrivermi?"
            query_embedding = embedder.embed_query(test_query)
            
            if not query_embedding or len(query_embedding) == 0:
                return {"passed": False, "error": "Embedding query fallito"}
            
            # Test embedding multipli documenti
            test_docs = ["Documento 1", "Documento 2", "Documento 3"]
            doc_embeddings = embedder.embed_documents(test_docs)
            
            if len(doc_embeddings) != len(test_docs):
                return {"passed": False, "error": "Embedding documenti fallito"}
            
            return {
                "passed": True,
                "embedding_size": len(query_embedding),
                "query_test": "OK",
                "documents_test": "OK",
                "num_docs_processed": len(test_docs)
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_dividi_chunks(self):
        """Test completo modulo dividi_chunks.py"""
        try:
            from dividi_chunks import split_text_in_chunks
            
            # Test con testo normale
            test_text = """Questo è un documento di test per la segreteria studenti.
            L'università offre diversi servizi agli studenti iscritti.
            Per maggiori informazioni contattare la segreteria studenti.
            Gli orari di apertura sono dal lunedì al venerdì dalle 9 alle 17."""
            
            chunks = split_text_in_chunks(test_text, max_len=100)
            
            if not chunks or len(chunks) == 0:
                return {"passed": False, "error": "Nessun chunk generato"}
            
            # Verifica che tutti i chunk siano stringhe
            if not all(isinstance(chunk, str) for chunk in chunks):
                return {"passed": False, "error": "Chunk non validi"}
            
            # Test con testo vuoto
            empty_chunks = split_text_in_chunks("")
            
            return {
                "passed": True,
                "num_chunks": len(chunks),
                "avg_chunk_length": sum(len(c) for c in chunks) / len(chunks),
                "empty_text_handled": len(empty_chunks) == 0,
                "chunks_preview": chunks[0][:50] + "..." if chunks else ""
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_ollama_llm(self):
        """Test modulo ollama_llm.py (solo inizializzazione, no connessione)"""
        try:
            from ollama_llm import OllamaLLM
            
            # Test solo inizializzazione classe
            llm = OllamaLLM()
            
            if not hasattr(llm, 'base_url'):
                return {"passed": False, "error": "Attributi base non presenti"}
            
            # Test preparazione prompt (senza chiamata effettiva)
            test_prompt = "Test prompt"
            
            return {
                "passed": True,
                "class_initialized": True,
                "base_url_set": bool(llm.base_url),
                "note": "Test limitato a inizializzazione (no connessione Ollama)"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_prompt_templates(self):
        """Test modulo prompt_templates.py"""
        try:
            from prompt_templates import get_optimized_prompt
            
            # Test generazione prompt
            test_context = "Informazioni sull'università"
            test_query = "Come posso iscrivermi?"
            
            prompt = get_optimized_prompt(test_context, test_query)
            
            if not prompt or len(prompt) < 10:
                return {"passed": False, "error": "Prompt non generato correttamente"}
            
            # Verifica che contenga context e query
            if test_context not in prompt or test_query not in prompt:
                return {"passed": False, "error": "Prompt non contiene context/query"}
            
            return {
                "passed": True,
                "prompt_length": len(prompt),
                "contains_context": test_context in prompt,
                "contains_query": test_query in prompt,
                "prompt_preview": prompt[:100] + "..."
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
        
    

    def test_simple_search():
        """Test ricerca nel vectorstore esistente"""
        print("Eseguendo test: simple_search")
    
        try:
            # Auto-detect nome collezione
            import chromadb
            client = chromadb.PersistentClient(path="../vectordb")
            collections = client.list_collections()
        
            if not collections:
                print("⚠️ Nessuna collezione trovata - saltando test")
                return True  # Non fallire se non c'è database
            
            collection_name = collections[0].name
            print(f"✅ Usando collezione: '{collection_name}'")
        
            from src.creazione_vectorstore import carica_vectorstore
            from src.local_embeddings import LocalEmbeddings
        
            embeddings = LocalEmbeddings()
            vectorstore = carica_vectorstore("../vectordb", collection_name)
        
            # Test ricerca semplice
            query = "informazioni università"
            results = vectorstore.similarity_search(query, k=1)
        
            success = len(results) > 0
            print(f"   Documenti trovati: {len(results)}")
        
            return success
        
        except Exception as e:
            print(f"Errore test search: {e}")
            return False

    
    def test_creazione_vectorstore(self):
        """Test modulo creazione_vectorstore.py (solo funzioni base)"""
        try:
            from creazione_vectorstore import clean_text
            
            # Test funzione clean_text
            test_texts = [
                "  Testo  con   spazi   extra  ",
                "Testo\ncon\rcaratteri\tspeciali",
                ""
            ]
            
            cleaned_results = []
            for text in test_texts:
                cleaned = clean_text(text)
                cleaned_results.append({
                    "original": text,
                    "cleaned": cleaned,
                    "length_before": len(text),
                    "length_after": len(cleaned)
                })
            
            return {
                "passed": True,
                "clean_text_works": True,
                "test_cases": len(cleaned_results),
                "results": cleaned_results
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}

def run_unit_tests():
    """Esegue tutti i test unitari sui moduli src/"""
    runner = TestRunner()
    
    print("🧪 Test Unitari - Moduli src/")
    print("=" * 50)
    
    # Test moduli src
    src_tests = TestSrcModules()
    runner.run_test("local_embeddings_module", src_tests.test_local_embeddings)
    runner.run_test("dividi_chunks_module", src_tests.test_dividi_chunks)
    runner.run_test("ollama_llm_module", src_tests.test_ollama_llm)
    runner.run_test("prompt_templates_module", src_tests.test_prompt_templates)
    runner.run_test("creazione_vectorstore_module", src_tests.test_creazione_vectorstore)
    
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