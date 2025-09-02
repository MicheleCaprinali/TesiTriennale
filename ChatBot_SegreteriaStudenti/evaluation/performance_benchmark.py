#!/usr/bin/env python3
"""
Benchmark Performance ChatBot
Test velocità e ottimizzazioni
"""

import time
import sys
import os
import statistics
import json
from datetime import datetime

sys.path.append('src')
from chatbot import ChatbotRAG

class PerformanceBenchmark:
    """Benchmark specializzato per performance"""
    
    def __init__(self):
        self.chatbot = None
        self.results = []
        
    def setup(self):
        """Setup veloce chatbot"""
        print("🚀 Setup ChatBot per benchmark...")
        try:
            self.chatbot = ChatbotRAG()
            print("✅ ChatBot pronto")
            return True
        except Exception as e:
            print(f"❌ Errore: {e}")
            return False
    
    def quick_performance_test(self, iterations=10):
        """Test rapido di performance"""
        print(f"\n⚡ BENCHMARK VELOCITÀ ({iterations} test)")
        print("=" * 50)
        
        if not self.setup():
            return None
        
        # Query test velocità
        test_queries = [
            "Orari segreteria?",
            "Come pagare tasse?", 
            "Certificato laurea?",
            "Contatti università?",
            "Iscrizione esami?"
        ]
        
        all_times = []
        successes = 0
        timeouts = 0
        
        for i in range(iterations):
            query = test_queries[i % len(test_queries)]
            print(f"\nTest {i+1}/{iterations}: {query}")
            
            start = time.time()
            try:
                result = self.chatbot.chat(query)
                end = time.time()
                
                response_time = end - start
                all_times.append(response_time)
                
                if response_time < 10:  # Target: sotto 10s
                    print(f"   ✅ {response_time:.1f}s - VELOCE")
                    successes += 1
                elif response_time < 20:
                    print(f"   ⚠️ {response_time:.1f}s - ACCETTABILE")
                    successes += 1
                else:
                    print(f"   ❌ {response_time:.1f}s - LENTO")
                    timeouts += 1
                    
            except Exception as e:
                print(f"   💥 ERRORE: {str(e)}")
                timeouts += 1
        
        # Calcola statistiche
        if all_times:
            avg_time = statistics.mean(all_times)
            median_time = statistics.median(all_times)
            min_time = min(all_times)
            max_time = max(all_times)
            
            success_rate = successes / iterations * 100
            
            print(f"\n📊 RISULTATI BENCHMARK:")
            print(f"   Tempo Medio: {avg_time:.1f}s")
            print(f"   Tempo Mediano: {median_time:.1f}s")
            print(f"   Range: {min_time:.1f}s - {max_time:.1f}s")
            print(f"   Tasso Successo: {success_rate:.0f}%")
            
            # Valutazione finale
            if avg_time < 8 and success_rate > 80:
                grade = "🥇 ECCELLENTE"
            elif avg_time < 15 and success_rate > 70:
                grade = "🥈 BUONO"
            elif avg_time < 25 and success_rate > 50:
                grade = "🥉 SUFFICIENTE"
            else:
                grade = "❌ CRITICO"
            
            print(f"   Valutazione: {grade}")
            
            # Salva risultati
            benchmark_data = {
                'timestamp': datetime.now().isoformat(),
                'iterations': iterations,
                'avg_time': avg_time,
                'median_time': median_time,
                'min_time': min_time,
                'max_time': max_time,
                'success_rate': success_rate,
                'grade': grade,
                'times': all_times
            }
            
            os.makedirs('results', exist_ok=True)
            with open('results/performance_benchmark.json', 'w') as f:
                json.dump(benchmark_data, f, indent=2)
            
            print(f"\n💾 Risultati salvati in: results/performance_benchmark.json")
            
            return benchmark_data
        
        return None

def main():
    """Esegui benchmark performance"""
    benchmark = PerformanceBenchmark()
    
    print("🎯 CHATBOT PERFORMANCE BENCHMARK")
    print("=" * 40)
    
    # Test rapido
    results = benchmark.quick_performance_test(iterations=5)
    
    if results:
        print(f"\n🎖️ SUMMARY:")
        print(f"   Performance media: {results['avg_time']:.1f}s")
        print(f"   Successo: {results['success_rate']:.0f}%")
        print(f"   Classificazione: {results['grade']}")
        
        if results['avg_time'] < 10:
            print(f"\n🎉 SISTEMA PRONTO PER PRODUZIONE!")
        else:
            print(f"\n⚠️ SISTEMA RICHIEDE OTTIMIZZAZIONI")
            print(f"   Target: < 10s per query")
            print(f"   Attuale: {results['avg_time']:.1f}s")
    
    else:
        print("\n❌ Benchmark fallito")

if __name__ == "__main__":
    main()
