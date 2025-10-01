#!/usr/bin/env python3
"""
Test Prestazionali - Chatbot Reale
==================================
Test performance del chatbot reale con 20-30 query in sequenza rapida
"""

import os
import sys
import json
import time
import statistics
from datetime import datetime

# Aggiungi path per import moduli
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class RealChatbotPerformanceTest:
    """Test prestazionali sul chatbot reale"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_type": "real_performance",
            "chatbot": None,
            "queries": [],
            "summary": {}
        }
        
        # Query realistiche per test prestazionali
        self.test_queries = [
            "Come posso iscrivermi all'università?",
            "Quali sono le scadenze per le tasse universitarie?",
            "Come prenotare un esame?",
            "Quali documenti servono per l'immatricolazione?",
            "Orari di apertura della segreteria studenti",
            "Come posso cambiare corso di laurea?",
            "Informazioni su borse di studio disponibili",
            "Procedura per il trasferimento da altra università",
            "Come contattare i docenti del mio corso?",
            "Quando iniziano le lezioni?",
            "Dove posso trovare l'orario delle lezioni?",
            "Come funziona il sistema di prenotazione esami?",
            "Cosa fare in caso di problemi con il libretto online?",
            "Informazioni sui tirocini curriculari",
            "Come richiedere certificati e documenti?",
            "Procedura per la laurea triennale",
            "Informazioni sui corsi di recupero",
            "Come accedere alla biblioteca universitaria?",
            "Servizi disponibili per studenti disabili",
            "Informazioni sulla mensa universitaria",
            "Come partecipare al programma Erasmus?",
            "Procedura per il riconoscimento crediti",
            "Informazioni sulle associazioni studentesche",
            "Come richiedere la carta studente?",
            "Servizi di orientamento disponibili",
            "Informazioni sui laboratori informatici",
            "Come segnalare un problema tecnico?",
            "Procedure per l'interruzione degli studi",
            "Informazioni sui corsi di dottorato",
            "Come ottenere supporto per la tesi?"
        ]
    
    def initialize_chatbot(self):
        """Inizializza il chatbot reale"""
        try:
            print("🤖 Inizializzazione chatbot reale...")
            
            from main import ChatbotRAG
            
            # Inizializza il chatbot
            self.chatbot = ChatbotRAG()
            
            print("✅ Chatbot inizializzato con successo")
            return True
            
        except Exception as e:
            print(f"❌ Errore inizializzazione chatbot: {e}")
            self.results["initialization_error"] = str(e)
            return False
    
    def execute_single_query(self, query, query_index):
        """Esegue una singola query e misura le performance"""
        
        start_time = time.time()
        
        try:
            # Esegui query sul chatbot reale
            response = self.chatbot.chat(query)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Analizza la risposta
            response_length = len(response) if response else 0
            has_content = bool(response and response.strip())
            
            result = {
                "query_index": query_index,
                "query": query,
                "response": response[:200] + "..." if len(response) > 200 else response,
                "response_length": response_length,
                "response_time": response_time,
                "success": has_content,
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                "query_index": query_index,
                "query": query,
                "response": "",
                "response_length": 0,
                "response_time": response_time,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_sequential_performance_test(self, num_queries=25):
        """Esegue test prestazionale con query in sequenza"""
        
        print(f"🔄 Test Prestazionale Sequenziale - {num_queries} query")
        print("-" * 50)
        
        if not self.initialize_chatbot():
            return {
                "success": False,
                "error": "Impossibile inizializzare chatbot"
            }
        
        # Seleziona query per il test
        selected_queries = self.test_queries[:num_queries]
        
        results = []
        start_test_time = time.time()
        
        for i, query in enumerate(selected_queries):
            print(f"  Query {i+1}/{num_queries}: {query[:50]}...")
            
            result = self.execute_single_query(query, i+1)
            results.append(result)
            
            # Aggiungi piccola pausa per non sovraccaricare
            time.sleep(0.1)
        
        total_test_time = time.time() - start_test_time
        
        # Calcola statistiche
        successful_queries = [r for r in results if r["success"]]
        failed_queries = [r for r in results if not r["success"]]
        
        if successful_queries:
            response_times = [r["response_time"] for r in successful_queries]
            response_lengths = [r["response_length"] for r in successful_queries]
            
            stats = {
                "total_queries": num_queries,
                "successful_queries": len(successful_queries),
                "failed_queries": len(failed_queries),
                "success_rate": len(successful_queries) / num_queries,
                "total_execution_time": total_test_time,
                "avg_response_time": statistics.mean(response_times),
                "median_response_time": statistics.median(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "std_dev_response_time": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "avg_response_length": statistics.mean(response_lengths),
                "throughput_qpm": len(successful_queries) / (total_test_time / 60),  # Query per minuto
                "percentile_95": sorted(response_times)[int(0.95 * len(response_times))] if response_times else 0
            }
        else:
            stats = {
                "total_queries": num_queries,
                "successful_queries": 0,
                "failed_queries": num_queries,
                "success_rate": 0,
                "total_execution_time": total_test_time
            }
        
        self.results["queries"] = results
        self.results["statistics"] = stats
        
        return {
            "success": True,
            "statistics": stats,
            "detailed_results": results
        }
    
    def generate_performance_report(self):
        """Genera report delle performance"""
        
        if "statistics" not in self.results:
            return None
        
        stats = self.results["statistics"]
        
        # Valutazione performance
        avg_time = stats.get("avg_response_time", 10)
        success_rate = stats.get("success_rate", 0)
        
        if avg_time <= 2.0 and success_rate >= 0.95:
            grade = "A - Eccellente"
        elif avg_time <= 5.0 and success_rate >= 0.90:
            grade = "B - Buono"
        elif avg_time <= 10.0 and success_rate >= 0.80:
            grade = "C - Sufficiente"
        else:
            grade = "D - Da migliorare"
        
        self.results["summary"] = {
            "performance_grade": grade,
            "ready_for_production": avg_time <= 5.0 and success_rate >= 0.90,
            "avg_response_time": avg_time,
            "success_rate_percent": success_rate * 100,
            "total_queries_processed": stats.get("successful_queries", 0),
            "recommendation": self.get_recommendation(avg_time, success_rate)
        }
        
        return self.results["summary"]
    
    def get_recommendation(self, avg_time, success_rate):
        """Genera raccomandazione basata sui risultati"""
        
        if avg_time <= 2.0 and success_rate >= 0.95:
            return "Sistema pronto per produzione - performance eccellenti"
        elif avg_time > 5.0:
            return "Ottimizzare tempi di risposta - considerare hardware più potente o ottimizzazioni LLM"
        elif success_rate < 0.90:
            return "Migliorare affidabilità sistema - verificare gestione errori"
        else:
            return "Performance accettabili - monitorare in produzione"
    
    def save_results(self):
        """Salva i risultati del test"""
        
        results_file = os.path.join(os.path.dirname(__file__), "..", "results", "real_performance_results.json")
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Risultati salvati in: {results_file}")
        return results_file

def run_real_performance_test():
    """Funzione principale per eseguire il test prestazionale"""
    
    print("⚡ TEST PRESTAZIONALI CHATBOT REALE")
    print("=" * 60)
    
    tester = RealChatbotPerformanceTest()
    
    # Esegui test con 25 query
    result = tester.run_sequential_performance_test(25)
    
    if not result["success"]:
        print(f"❌ Test fallito: {result.get('error', 'Errore sconosciuto')}")
        return None
    
    # Genera report
    summary = tester.generate_performance_report()
    
    # Stampa risultati
    print("\n📊 RISULTATI TEST PRESTAZIONALI")
    print("=" * 60)
    
    stats = result["statistics"]
    print(f"📈 Query totali: {stats['total_queries']}")
    print(f"✅ Query riuscite: {stats['successful_queries']}")
    print(f"❌ Query fallite: {stats['failed_queries']}")
    print(f"📊 Tasso successo: {stats['success_rate']:.2%}")
    print(f"⏱️  Tempo medio risposta: {stats['avg_response_time']:.3f}s")
    print(f"📏 Tempo mediano: {stats['median_response_time']:.3f}s")
    print(f"� Tempo minimo: {stats['min_response_time']:.3f}s")
    print(f"🐌 Tempo massimo: {stats['max_response_time']:.3f}s")
    print(f"📊 95° percentile: {stats['percentile_95']:.3f}s")
    print(f"📈 Throughput: {stats['throughput_qpm']:.1f} query/min")
    
    if summary:
        print(f"\n🎯 VALUTAZIONE FINALE")
        print(f"   Voto: {summary['performance_grade']}")
        print(f"   Pronto produzione: {'✅ SÌ' if summary['ready_for_production'] else '❌ NO'}")
        print(f"   Raccomandazione: {summary['recommendation']}")
    
    # Salva risultati
    tester.save_results()
    
    return tester.results

if __name__ == "__main__":
    run_real_performance_test()