#!/usr/bin/env python3
"""
Test - Performance e Accuratezza
"""

import json
import time
import sys
import os
from datetime import datetime
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sys.path.append('src')
from chatbot import ChatbotRAG

class ThesisEvaluator:
    def __init__(self, test_dataset_path="test_dataset.json"):
        """Inizializza l'evaluator per la tesi"""
        self.chatbot = None
        self.results = []
        self.test_dataset = self.load_dataset(test_dataset_path)
        
    def load_dataset(self, path):
        """Carica il dataset di test"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data['queries']
        except Exception as e:
            print(f"❌ Errore nel caricamento dataset: {e}")
            return []
    
    def setup_chatbot(self):
        """Inizializza il chatbot per i test"""
        print("Inizializzazione chatbot...")
        try:
            self.chatbot = ChatbotRAG()
            print("✅ Chatbot inizializzato")
            return True
        except Exception as e:
            print(f"❌ Errore inizializzazione: {e}")
            return False
    
    def run_performance_test(self, sample_size=20):
        """Test di performance completo"""
        print(f"\nPERFORMANCE TEST ({sample_size} queries)")
        print("=" * 50)
        
        if not self.chatbot:
            if not self.setup_chatbot():
                return None
        
        results = {
            'response_times': [],
            'token_counts': [],
            'redirect_accuracy': [],
            'queries_tested': [],
            'timestamps': []
        }
        
        # Prendi un campione casuale
        import random
        sample_queries = random.sample(self.test_dataset, min(sample_size, len(self.test_dataset)))
        
        for i, query_data in enumerate(sample_queries, 1):
            query = query_data['query']
            expected_redirect = query_data['expected_redirect']
            
            print(f"Test {i}/{sample_size}: {query[:50]}...")
            
            # Misura tempo di risposta
            start_time = time.time()
            try:
                result = self.chatbot.chat(query)
                response = result['response']
                end_time = time.time()
                
                response_time = end_time - start_time
                results['response_times'].append(response_time)
                results['token_counts'].append(len(response.split()))
                results['timestamps'].append(datetime.now().isoformat())
                results['queries_tested'].append(query)
                
                # Verifica accuratezza redirect
                is_redirect = result.get('should_redirect', False)
                correct_redirect = (is_redirect == expected_redirect)
                results['redirect_accuracy'].append(correct_redirect)
                
                status = "✅" if correct_redirect else "❌"
                print(f"   {status} Tempo: {response_time:.2f}s | Redirect: {is_redirect} (expected: {expected_redirect})")
                
            except Exception as e:
                print(f"   ❌ Errore: {e}")
                continue
        
        return self.analyze_performance(results)
    
    def analyze_performance(self, results):
        """Analizza i risultati dei test"""
        if not results['response_times']:
            return None
            
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': len(results['response_times']),
            'avg_response_time': statistics.mean(results['response_times']),
            'median_response_time': statistics.median(results['response_times']),
            'min_response_time': min(results['response_times']),
            'max_response_time': max(results['response_times']),
            'avg_tokens': statistics.mean(results['token_counts']),
            'redirect_accuracy': sum(results['redirect_accuracy']) / len(results['redirect_accuracy']) * 100,
            'raw_data': results
        }
        
        print(f"\nRISULTATI PERFORMANCE:")
        print(f"Tempo medio risposta: {analysis['avg_response_time']:.2f}s")
        print(f"Tempo mediano: {analysis['median_response_time']:.2f}s") 
        print(f"Range: {analysis['min_response_time']:.2f}s - {analysis['max_response_time']:.2f}s")
        print(f"Token medi per risposta: {analysis['avg_tokens']:.1f}")
        print(f"Accuratezza redirect: {analysis['redirect_accuracy']:.1f}%")
        
        return analysis
    
    def generate_thesis_charts(self, results):
        """Genera grafici per la tesi"""
        if not results or not results['raw_data']['response_times']:
            return
            
        print("\nGenerazione grafici per tesi...")
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 1. Distribuzione tempi di risposta
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.hist(results['raw_data']['response_times'], bins=10, edgecolor='black', alpha=0.7)
        plt.title('Distribuzione Tempi di Risposta', fontsize=12, fontweight='bold')
        plt.xlabel('Tempo (secondi)')
        plt.ylabel('Frequenza')
        plt.grid(True, alpha=0.3)
        
        # 2. Lunghezza risposte
        plt.subplot(2, 2, 2)
        plt.hist(results['raw_data']['token_counts'], bins=10, edgecolor='black', alpha=0.7, color='orange')
        plt.title('Distribuzione Lunghezza Risposte', fontsize=12, fontweight='bold')
        plt.xlabel('Numero di Token')
        plt.ylabel('Frequenza')
        plt.grid(True, alpha=0.3)
        
        # 3. Performance nel tempo
        plt.subplot(2, 2, 3)
        plt.plot(range(1, len(results['raw_data']['response_times'])+1), 
                results['raw_data']['response_times'], marker='o', alpha=0.7)
        plt.title('Performance nel Tempo', fontsize=12, fontweight='bold')
        plt.xlabel('Query #')
        plt.ylabel('Tempo di Risposta (s)')
        plt.grid(True, alpha=0.3)
        
        # 4. Accuratezza
        plt.subplot(2, 2, 4)
        accuracy_data = ['Corretti', 'Errati']
        correct = sum(results['raw_data']['redirect_accuracy'])
        total = len(results['raw_data']['redirect_accuracy'])
        values = [correct, total - correct]
        
        plt.pie(values, labels=accuracy_data, autopct='%1.1f%%', startangle=90)
        plt.title('Accuratezza Classificazione Redirect', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('thesis_performance_charts.png', dpi=300, bbox_inches='tight')
        print("Grafici salvati in: thesis_performance_charts.png")
        
        with open('thesis_performance_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Risultati dettagliati salvati in: thesis_performance_results.json")
    
    def run_complete_evaluation(self):
        """Esegue evaluation completa"""
        print("EVALUATION COMPLETA")
        print("=" * 60)
        
        results = self.run_performance_test(sample_size=30)
        
        if results:
            self.generate_thesis_charts(results)
            
            print(f"\nSUMMARY FINALE:")
            print(f"Sistema testato su {results['total_queries']} query")
            print(f"Performance media: {results['avg_response_time']:.2f}s per query")
            print(f"Accuratezza routing: {results['redirect_accuracy']:.1f}%")
            print(f"Completezza risposte: {results['avg_tokens']:.0f} token medi")
            
            if results['avg_response_time'] < 3.0:
                print("✅ Performance: ECCELLENTE (< 3s)")
            elif results['avg_response_time'] < 5.0:
                print("✅ Performance: BUONA (< 5s)")
            else:
                print("⚠️ Performance: DA MIGLIORARE (> 5s)")
                
            if results['redirect_accuracy'] > 80:
                print("✅ Accuratezza: ECCELLENTE (> 80%)")
            elif results['redirect_accuracy'] > 60:
                print("✅ Accuratezza: BUONA (> 60%)")
            else:
                print("⚠️ Accuratezza: DA MIGLIORARE (< 60%)")
        
        return results

if __name__ == "__main__":
    evaluator = ThesisEvaluator()
    results = evaluator.run_complete_evaluation()