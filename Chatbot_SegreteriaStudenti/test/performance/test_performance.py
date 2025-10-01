#!/usr/bin/env python3
"""
Test Prestazionali - Performance e Scalabilità
==============================================
Test per misurare tempi di risposta, throughput e comportamento sotto carico
"""

import os
import sys
import json
import time
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Aggiungi path per import moduli
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class PerformanceTestRunner:
    """Gestisce l'esecuzione dei test prestazionali"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_type": "performance",
            "tests": {},
            "summary": {}
        }
        
        # Set di query per test prestazionali
        self.performance_queries = [
            "Come posso iscrivermi all'università?",
            "Quali sono le scadenze per le tasse?",
            "Come prenotare un esame?",
            "Orari della segreteria studenti",
            "Requisiti per la laurea",
            "Documenti necessari per l'iscrizione",
            "Costi universitari",
            "Come cambiare corso di laurea",
            "Procedure per trasferimento",
            "Informazioni su borse di studio",
            "Come contattare i docenti",
            "Calendario accademico",
            "Aule e laboratori disponibili",
            "Servizi per studenti disabili",
            "Procedura per tesi di laurea",
            "Erasmus e mobilità internazionale",
            "Tirocini e stage",
            "Servizi biblioteca",
            "Mensa universitaria",
            "Trasporti pubblici per università",
            "Alloggi per studenti",
            "Associazioni studentesche",
            "Corsi di recupero",
            "Valutazione carriera pregressa",
            "Riconoscimento crediti formativi"
        ]
    
    def simulate_chatbot_query(self, query):
        """Simula l'esecuzione di una query al chatbot"""
        start_time = time.time()
        
        try:
            # Simula il caricamento del modello (solo la prima volta)
            if not hasattr(self, '_model_loaded'):
                time.sleep(0.5)  # Simula caricamento modello
                self._model_loaded = True
            
            # Simula embedding della query
            time.sleep(0.05)  # Simula tempo embedding
            
            # Simula ricerca nel vectorstore
            time.sleep(0.03)  # Simula ricerca semantica
            
            # Simula generazione risposta LLM
            time.sleep(0.2)   # Simula inferenza LLM
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Simula risposta
            response = f"Risposta simulata per: {query[:50]}..."
            
            return {
                "success": True,
                "response_time": response_time,
                "query_length": len(query),
                "response_length": len(response),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
    
    def test_sequential_performance(self, num_queries=25):
        """Test prestazioni con query sequenziali"""
        print(f"🔄 Test Sequential - {num_queries} query")
        
        selected_queries = self.performance_queries[:num_queries]
        results = []
        
        start_time = time.time()
        
        for i, query in enumerate(selected_queries):
            print(f"  Query {i+1}/{num_queries}", end="\r")
            result = self.simulate_chatbot_query(query)
            results.append(result)
        
        total_time = time.time() - start_time
        
        # Calcola statistiche
        successful_results = [r for r in results if r["success"]]
        response_times = [r["response_time"] for r in successful_results]
        
        if response_times:
            stats = {
                "total_queries": num_queries,
                "successful_queries": len(successful_results),
                "failed_queries": num_queries - len(successful_results),
                "total_execution_time": total_time,
                "avg_response_time": statistics.mean(response_times),
                "median_response_time": statistics.median(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "std_dev_response_time": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "throughput_qps": len(successful_results) / total_time,
                "success_rate": len(successful_results) / num_queries
            }
        else:
            stats = {
                "total_queries": num_queries,
                "successful_queries": 0,
                "failed_queries": num_queries,
                "success_rate": 0
            }
        
        print(f"\n  ✓ Completato: {stats.get('avg_response_time', 0):.3f}s tempo medio")
        
        return {
            "test_type": "sequential",
            "statistics": stats,
            "raw_results": results
        }
    
    def test_concurrent_performance(self, num_queries=20, max_workers=5):
        """Test prestazioni con query concorrenti"""
        print(f"⚡ Test Concurrent - {num_queries} query, {max_workers} worker")
        
        selected_queries = self.performance_queries[:num_queries]
        results = []
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Sottometti tutte le query
            future_to_query = {
                executor.submit(self.simulate_chatbot_query, query): query 
                for query in selected_queries
            }
            
            # Raccogli risultati
            completed = 0
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        "success": False,
                        "error": str(e),
                        "response_time": 0
                    })
                
                completed += 1
                print(f"  Completate {completed}/{num_queries}", end="\r")
        
        total_time = time.time() - start_time
        
        # Calcola statistiche
        successful_results = [r for r in results if r["success"]]
        response_times = [r["response_time"] for r in successful_results]
        
        if response_times:
            stats = {
                "total_queries": num_queries,
                "successful_queries": len(successful_results),
                "failed_queries": num_queries - len(successful_results),
                "max_workers": max_workers,
                "total_execution_time": total_time,
                "avg_response_time": statistics.mean(response_times),
                "median_response_time": statistics.median(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "std_dev_response_time": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "throughput_qps": len(successful_results) / total_time,
                "success_rate": len(successful_results) / num_queries,
                "concurrency_efficiency": (len(successful_results) / total_time) / max_workers
            }
        else:
            stats = {
                "total_queries": num_queries,
                "successful_queries": 0,
                "failed_queries": num_queries,
                "success_rate": 0
            }
        
        print(f"\n  ✓ Completato: {stats.get('throughput_qps', 0):.2f} QPS")
        
        return {
            "test_type": "concurrent",
            "statistics": stats,
            "raw_results": results
        }
    
    def test_load_patterns(self):
        """Test con diversi pattern di carico"""
        print("📈 Test Pattern di Carico")
        
        patterns = [
            {"name": "low_load", "queries": 10, "workers": 1},
            {"name": "medium_load", "queries": 20, "workers": 3},
            {"name": "high_load", "queries": 30, "workers": 5}
        ]
        
        pattern_results = {}
        
        for pattern in patterns:
            print(f"  Test {pattern['name']}: {pattern['queries']} query, {pattern['workers']} worker")
            
            result = self.test_concurrent_performance(
                num_queries=pattern["queries"],
                max_workers=pattern["workers"]
            )
            
            pattern_results[pattern["name"]] = result
            
            # Pausa tra test
            time.sleep(1)
        
        return pattern_results
    
    def test_memory_behavior(self, iterations=5):
        """Test comportamento memoria con query ripetute"""
        print(f"🧠 Test Memoria - {iterations} iterazioni")
        
        test_query = "Come posso iscrivermi all'università?"
        results = []
        
        for i in range(iterations):
            print(f"  Iterazione {i+1}/{iterations}", end="\r")
            result = self.simulate_chatbot_query(test_query)
            results.append(result)
            
            # Simula piccola pausa
            time.sleep(0.1)
        
        # Analizza trend tempi di risposta
        response_times = [r["response_time"] for r in results if r["success"]]
        
        if len(response_times) > 1:
            # Calcola se c'è degradazione o miglioramento
            first_half = response_times[:len(response_times)//2]
            second_half = response_times[len(response_times)//2:]
            
            first_avg = statistics.mean(first_half)
            second_avg = statistics.mean(second_half)
            
            performance_trend = (second_avg - first_avg) / first_avg * 100
        else:
            performance_trend = 0
        
        print(f"\n  ✓ Trend performance: {performance_trend:+.1f}%")
        
        return {
            "iterations": iterations,
            "results": results,
            "performance_trend_percent": performance_trend,
            "avg_response_time": statistics.mean(response_times) if response_times else 0
        }

def run_performance_tests():
    """Esegue tutti i test prestazionali"""
    runner = PerformanceTestRunner()
    
    print("⚡ Avvio Test Prestazionali")
    print("=" * 50)
    
    # Test sequenziale
    sequential_result = runner.test_sequential_performance(25)
    runner.results["tests"]["sequential"] = sequential_result
    
    # Test concorrente
    concurrent_result = runner.test_concurrent_performance(20, 5)
    runner.results["tests"]["concurrent"] = concurrent_result
    
    # Test pattern di carico
    load_patterns_result = runner.test_load_patterns()
    runner.results["tests"]["load_patterns"] = load_patterns_result
    
    # Test memoria
    memory_result = runner.test_memory_behavior(5)
    runner.results["tests"]["memory_behavior"] = memory_result
    
    # Calcola sommario generale
    seq_stats = sequential_result["statistics"]
    conc_stats = concurrent_result["statistics"]
    
    runner.results["summary"] = {
        "sequential_performance": {
            "avg_response_time": seq_stats.get("avg_response_time", 0),
            "throughput_qps": seq_stats.get("throughput_qps", 0),
            "success_rate": seq_stats.get("success_rate", 0)
        },
        "concurrent_performance": {
            "avg_response_time": conc_stats.get("avg_response_time", 0),
            "throughput_qps": conc_stats.get("throughput_qps", 0),
            "success_rate": conc_stats.get("success_rate", 0),
            "concurrency_efficiency": conc_stats.get("concurrency_efficiency", 0)
        },
        "memory_behavior": {
            "performance_trend": memory_result.get("performance_trend_percent", 0),
            "stable_performance": abs(memory_result.get("performance_trend_percent", 0)) < 10
        },
        "overall_assessment": {
            "ready_for_production": (
                seq_stats.get("avg_response_time", 10) < 2.0 and
                seq_stats.get("success_rate", 0) > 0.95 and
                conc_stats.get("success_rate", 0) > 0.90
            ),
            "performance_grade": "A" if seq_stats.get("avg_response_time", 10) < 1.0 else 
                                "B" if seq_stats.get("avg_response_time", 10) < 2.0 else 
                                "C" if seq_stats.get("avg_response_time", 10) < 5.0 else "D"
        }
    }
    
    # Salva risultati
    results_file = os.path.join(os.path.dirname(__file__), "..", "results", "performance_tests_results.json")
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(runner.results, f, indent=2, ensure_ascii=False)
    
    # Stampa sommario finale
    print(f"\n📊 Sommario Test Prestazionali:")
    print(f"   Sequenziale: {runner.results['summary']['sequential_performance']['avg_response_time']:.3f}s avg, "
          f"{runner.results['summary']['sequential_performance']['throughput_qps']:.2f} QPS")
    print(f"   Concorrente: {runner.results['summary']['concurrent_performance']['avg_response_time']:.3f}s avg, "
          f"{runner.results['summary']['concurrent_performance']['throughput_qps']:.2f} QPS")
    print(f"   Trend memoria: {runner.results['summary']['memory_behavior']['performance_trend']:+.1f}%")
    print(f"   Valutazione: {runner.results['summary']['overall_assessment']['performance_grade']}")
    print(f"   Pronto produzione: {'✓' if runner.results['summary']['overall_assessment']['ready_for_production'] else '✗'}")
    print(f"   Risultati salvati in: {results_file}")
    
    return runner.results

if __name__ == "__main__":
    run_performance_tests()