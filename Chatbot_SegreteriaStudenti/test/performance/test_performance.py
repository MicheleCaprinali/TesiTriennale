import sys
import os
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Aggiungi il percorso del progetto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_real_chatbot_performance():
    """Test prestazionale con chatbot reale"""
    print("⚡ Avvio Test Prestazionali Chatbot Reale")
    print("=" * 50)
    
    # Query realistiche per test
    test_queries = [
        "Come posso iscrivermi all'università?",
        "Quali sono le tasse universitarie?",
        "Come si prenota un esame?",
        "Quando è il periodo di laurea?",
        "Dove si trova la segreteria studenti?",
        "Come si compila il piano di studi?",
        "Quali documenti servono per l'iscrizione?",
        "Come si richiede il certificato di laurea?",
        "Quando aprono le iscrizioni?",
        "Come si paga la prima rata?",
        "Dove trovo gli orari delle lezioni?",
        "Come si richiede una borsa di studio?",
        "Quali sono i requisiti per la laurea?",
        "Come si trasferisce da altra università?",
        "Dove si ritirano i diplomi?",
        "Come si modifica il piano di studi?",
        "Quando sono gli appelli d'esame?",
        "Come si richiede il duplicato libretto?",
        "Quali sono le scadenze amministrative?",
        "Come si rinuncia agli studi?",
        "Dove si trova l'ufficio tasse?",
        "Come si richiede il foglio congedo?",
        "Quando è possibile laurearsi?",
        "Come si prenota la discussione tesi?",
        "Quali documenti servono per laurearsi?"
    ]
    
    results = {
        'queries_total': len(test_queries),
        'queries_successful': 0,
        'queries_failed': 0,
        'response_times': [],
        'error_details': [],
        'performance_data': {}
    }
    
    # Inizializza il chatbot una sola volta
    try:
        # Assicurati di essere nella directory corretta
        original_dir = os.getcwd()
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        os.chdir(project_root)
        
        from main import ChatbotRAG
        print("🤖 Inizializzazione chatbot...")
        chatbot = ChatbotRAG()
        print("✅ Chatbot inizializzato")
    except Exception as e:
        print(f"❌ Errore inizializzazione chatbot: {e}")
        if 'original_dir' in locals():
            os.chdir(original_dir)
        return create_fallback_results(results, str(e))
    
    # Test sequenziale
    print(f"🔄 Esecuzione {len(test_queries)} query sequenziali...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"  Query {i}/{len(test_queries)}", end="", flush=True)
        
        start_time = time.time()
        try:
            # Esegui query sul chatbot reale
            result = chatbot.chat(query)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Estrai la risposta dal risultato
            if isinstance(result, dict):
                response = result.get("response", "")
            else:
                response = str(result)
            
            # Verifica che ci sia una risposta valida
            if response and len(response.strip()) > 0:
                results['response_times'].append(response_time)
                results['queries_successful'] += 1
                print(f" ✅ {response_time:.3f}s")
            else:
                results['queries_failed'] += 1
                results['error_details'].append(f"Query {i}: Risposta vuota")
                print(f" ❌ {response_time:.3f}s - Risposta vuota")
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            results['queries_failed'] += 1
            results['error_details'].append(f"Query {i}: {str(e)}")
            
            print(f" ❌ {response_time:.3f}s - {str(e)[:50]}...")
    
    # Calcola metriche se abbiamo almeno una risposta
    if results['response_times']:
        times = results['response_times']
        results['performance_data'] = {
            'avg_response_time': statistics.mean(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'success_rate': (results['queries_successful'] / results['queries_total']) * 100,
            'total_time': sum(times),
            'queries_per_second': results['queries_successful'] / sum(times) if sum(times) > 0 else 0
        }
        
        # Valutazione basata su tempo medio e tasso successo
        avg_time = results['performance_data']['avg_response_time']
        success_rate = results['performance_data']['success_rate']
        
        if success_rate >= 90 and avg_time <= 2.0:
            grade = "A"
            recommendation = "Eccellente - Pronto per produzione"
        elif success_rate >= 80 and avg_time <= 3.0:
            grade = "B"
            recommendation = "Buono - Performance accettabili"
        elif success_rate >= 70 and avg_time <= 5.0:
            grade = "C"
            recommendation = "Sufficiente - Necessari miglioramenti"
        else:
            grade = "D"
            recommendation = "Insufficiente - Richiede ottimizzazione"
        
        results['performance_data']['grade'] = grade
        results['performance_data']['recommendation'] = recommendation
        results['performance_data']['production_ready'] = grade in ['A', 'B']
    
    # Ripristina la directory originale
    if 'original_dir' in locals():
        os.chdir(original_dir)
    
    return results

def create_fallback_results(base_results, error_msg):
    """Crea risultati di fallback in caso di errore critico"""
    base_results['performance_data'] = {
        'avg_response_time': 0,
        'success_rate': 0,
        'grade': 'F',
        'recommendation': f'Errore critico: {error_msg}',
        'production_ready': False,
        'error': error_msg
    }
    return base_results

def print_performance_summary(results):
    """Stampa sommario risultati prestazionali"""
    print("\n📊 RISULTATI TEST PRESTAZIONALI")
    print("=" * 60)
    print(f"📈 Query totali: {results['queries_total']}")
    print(f"✅ Query riuscite: {results['queries_successful']}")
    print(f"❌ Query fallite: {results['queries_failed']}")
    
    if results['queries_successful'] > 0:
        perf = results['performance_data']
        print(f"📊 Tasso successo: {perf['success_rate']:.2f}%")
        print(f"⏱️ Tempo medio: {perf['avg_response_time']:.3f}s")
        print(f"🚀 Query/secondo: {perf['queries_per_second']:.2f}")
        print(f"🎯 Valutazione: {perf['grade']} - {perf['recommendation']}")
        print(f"🏭 Pronto produzione: {'✅ SÌ' if perf['production_ready'] else '❌ NO'}")
    else:
        print(f"📊 Tasso successo: 0.00%")
        print("❌ Nessuna query completata con successo")
        if results['error_details']:
            print("🔍 Primi errori:")
            for error in results['error_details'][:3]:
                print(f"   • {error}")

if __name__ == "__main__":
    results = test_real_chatbot_performance()
    print_performance_summary(results)
    
    # Salva risultati
    import json
    results_path = "../results/real_performance_results.json"
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Risultati salvati: {os.path.abspath(results_path)}")