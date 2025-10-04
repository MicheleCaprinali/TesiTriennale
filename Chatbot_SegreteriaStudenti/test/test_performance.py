"""
Test prestazionali chatbot con dati reali
Esegue 25 query reali e raccoglie metriche di performance
"""
import sys
import os
import time
import statistics
import json

# Aggiungi il percorso del progetto
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Query realistiche estratte da casi d'uso reali
TEST_QUERIES = [
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


def run_performance_test():
    """Esegue test prestazionale completo con chatbot reale"""
    print("⚡ TEST PRESTAZIONALI CHATBOT")
    print("=" * 60)
    
    results = {
        'queries_total': len(TEST_QUERIES),
        'queries_successful': 0,
        'queries_failed': 0,
        'response_times': [],
        'error_details': []
    }
    
    # Inizializza chatbot
    try:
        original_dir = os.getcwd()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_root)
        
        from main import ChatbotRAG
        print("🤖 Inizializzazione chatbot...")
        chatbot = ChatbotRAG()
        print("✅ Chatbot pronto\n")
    except Exception as e:
        print(f"❌ Errore inizializzazione: {e}")
        os.chdir(original_dir)
        return None
    
    # Esegui test
    print(f"🔄 Esecuzione {len(TEST_QUERIES)} query reali...")
    print()
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"  [{i:2d}/{len(TEST_QUERIES)}] ", end="", flush=True)
        
        start_time = time.time()
        try:
            result = chatbot.chat(query)
            end_time = time.time()
            response_time = end_time - start_time
            
            # Valida risposta
            if isinstance(result, dict):
                response = result.get("response", "")
            else:
                response = str(result)
            
            if response and len(response.strip()) > 0:
                results['response_times'].append(response_time)
                results['queries_successful'] += 1
                print(f"✅ {response_time:.1f}s")
            else:
                results['queries_failed'] += 1
                results['error_details'].append(f"Query {i}: Risposta vuota")
                print(f"❌ {response_time:.1f}s - Vuota")
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            results['queries_failed'] += 1
            results['error_details'].append(f"Query {i}: {str(e)[:80]}")
            print(f"❌ {response_time:.1f}s - {str(e)[:40]}")
    
    # Calcola metriche
    if results['response_times']:
        times = results['response_times']
        avg_time = statistics.mean(times)
        success_rate = (results['queries_successful'] / results['queries_total']) * 100
        
        results['performance_metrics'] = {
            'avg_response_time': avg_time,
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'std_deviation': statistics.stdev(times) if len(times) > 1 else 0,
            'success_rate': success_rate,
            'total_time': sum(times),
            'queries_per_second': results['queries_successful'] / sum(times) if sum(times) > 0 else 0
        }
        
        # Valutazione qualitativa
        if success_rate >= 90 and avg_time <= 2.0:
            grade, recommendation = "A", "Eccellente - Pronto produzione"
        elif success_rate >= 80 and avg_time <= 3.0:
            grade, recommendation = "B", "Buono - Performance accettabili"
        elif success_rate >= 70 and avg_time <= 5.0:
            grade, recommendation = "C", "Sufficiente - Miglioramenti necessari"
        else:
            grade, recommendation = "D", "Insufficiente - Ottimizzazione richiesta"
        
        results['performance_metrics']['grade'] = grade
        results['performance_metrics']['recommendation'] = recommendation
        results['performance_metrics']['production_ready'] = grade in ['A', 'B']
    
    os.chdir(original_dir)
    
    # Stampa sommario
    print()
    print("=" * 60)
    print("📊 RISULTATI")
    print("=" * 60)
    print(f"Query totali:     {results['queries_total']}")
    print(f"✅ Successi:      {results['queries_successful']}")
    print(f"❌ Fallimenti:    {results['queries_failed']}")
    
    if results['response_times']:
        metrics = results['performance_metrics']
        print()
        print(f"Tempo medio:      {metrics['avg_response_time']:.2f}s")
        print(f"Tempo minimo:     {metrics['min_response_time']:.2f}s")
        print(f"Tempo massimo:    {metrics['max_response_time']:.2f}s")
        print(f"Mediana:          {metrics['median_response_time']:.2f}s")
        print(f"Dev. standard:    {metrics['std_deviation']:.2f}s")
        print(f"Tasso successo:   {metrics['success_rate']:.1f}%")
        print(f"Query/secondo:    {metrics['queries_per_second']:.3f}")
        print()
        print(f"🎯 Valutazione:   {metrics['grade']} - {metrics['recommendation']}")
        print(f"🏭 Produzione:    {'✅ SÌ' if metrics['production_ready'] else '❌ NO'}")
    
    return results


def save_results(results, output_path='results/performance_results.json'):
    """Salva risultati in JSON"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"💾 Risultati salvati: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    results = run_performance_test()
    
    if results:
        save_results(results)
        print()
        print("✅ Test completato!")
        print("📊 Esegui 'python generate_charts.py' per creare i grafici")
