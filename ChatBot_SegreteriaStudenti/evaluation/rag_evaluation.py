#!/usr/bin/env python3
"""
Evaluation Avanzata per Sistema RAG
Metriche specializzate per chatbot RAG universitario
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
from typing import Dict, List, Any
import numpy as np

sys.path.append('src')
from chatbot import ChatbotRAG

class RAGEvaluator:
    """Evaluator specializzato per sistemi RAG"""
    
    def __init__(self, test_dataset_path="test_dataset.json"):
        self.chatbot = None
        self.results = []
        self.test_dataset = self.load_dataset(test_dataset_path)
        
    def load_dataset(self, path):
        """Carica dataset con metriche avanzate"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data['queries']
        except Exception as e:
            print(f"❌ Errore caricamento dataset: {e}")
            return []
    
    def setup_chatbot(self):
        """Setup chatbot per evaluation"""
        print("🚀 Inizializzazione ChatBot RAG...")
        try:
            self.chatbot = ChatbotRAG()
            print("✅ ChatBot pronto per evaluation")
            return True
        except Exception as e:
            print(f"❌ Errore setup: {e}")
            return False
    
    def evaluate_retrieval_quality(self, query: str, retrieved_docs: List[str], expected_topics: List[str] = None) -> Dict[str, float]:
        """Valuta qualità del retrieval"""
        metrics = {
            'retrieval_diversity': 0.0,
            'context_relevance': 0.0,
            'topic_coverage': 0.0
        }
        
        if not retrieved_docs:
            return metrics
        
        # Diversity Score: quanto sono diversi i documenti recuperati
        unique_words = set()
        total_words = 0
        for doc in retrieved_docs:
            words = doc.lower().split()
            unique_words.update(words)
            total_words += len(words)
        
        metrics['retrieval_diversity'] = len(unique_words) / max(total_words, 1)
        
        # Context Relevance: quante parole della query compaiono nei documenti
        query_words = set(query.lower().split())
        doc_words = set(' '.join(retrieved_docs).lower().split())
        
        if query_words:
            metrics['context_relevance'] = len(query_words.intersection(doc_words)) / len(query_words)
        
        # Topic Coverage se fornito
        if expected_topics:
            topic_found = 0
            for topic in expected_topics:
                if any(topic.lower() in doc.lower() for doc in retrieved_docs):
                    topic_found += 1
            metrics['topic_coverage'] = topic_found / len(expected_topics)
        
        return metrics
    
    def evaluate_response_quality(self, response: str, query: str) -> Dict[str, float]:
        """Valuta qualità della risposta"""
        metrics = {
            'response_length': len(response.split()),
            'specificity': 0.0,
            'completeness': 0.0,
            'clarity': 0.0
        }
        
        # Specificity: presenza di informazioni specifiche
        specific_indicators = ['http', 'tel:', 'email', 'orari', 'sede', 'via', 'numero', 'data', 'euro', '€']
        found_indicators = sum(1 for indicator in specific_indicators if indicator in response.lower())
        metrics['specificity'] = min(found_indicators / 3, 1.0)
        
        # Completeness: lunghezza appropriata
        word_count = len(response.split())
        if 20 <= word_count <= 100:
            metrics['completeness'] = 1.0
        elif word_count < 20:
            metrics['completeness'] = word_count / 20
        else:
            metrics['completeness'] = max(0.5, 100 / word_count)
        
        # Clarity: assenza di errori comuni
        clarity_penalties = 0
        if 'REDIRECT_TO_HUMAN' in response:
            clarity_penalties += 0.5
        if response.count('?') > 2:  # Troppe domande nella risposta
            clarity_penalties += 0.3
        if len(response) < 10:
            clarity_penalties += 0.5
            
        metrics['clarity'] = max(0.0, 1.0 - clarity_penalties)
        
        return metrics
    
    def comprehensive_evaluation(self, sample_size=20, timeout_limit=15.0):
        """Evaluation completa con metriche RAG specializzate"""
        print(f"\n🎯 RAG EVALUATION COMPLETA ({sample_size} queries)")
        print("=" * 60)
        
        if not self.setup_chatbot():
            return None
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': 0,
            'performance': {
                'avg_response_time': 0.0,
                'median_response_time': 0.0,
                'timeout_rate': 0.0,
                'success_rate': 0.0
            },
            'retrieval_quality': {
                'avg_diversity': 0.0,
                'avg_relevance': 0.0,
                'avg_coverage': 0.0
            },
            'response_quality': {
                'avg_specificity': 0.0,
                'avg_completeness': 0.0,
                'avg_clarity': 0.0,
                'avg_length': 0.0
            },
            'routing_accuracy': {
                'correct_redirects': 0,
                'false_positives': 0,
                'false_negatives': 0,
                'accuracy': 0.0
            },
            'detailed_results': []
        }
        
        # Prendi campione casuale
        import random
        test_queries = random.sample(self.test_dataset, min(sample_size, len(self.test_dataset)))
        results['total_queries'] = len(test_queries)
        
        response_times = []
        retrieval_metrics = []
        response_metrics = []
        timeouts = 0
        successes = 0
        
        for i, query_data in enumerate(test_queries, 1):
            query = query_data['query']
            expected_redirect = query_data.get('should_redirect', False)
            expected_topics = query_data.get('topics', [])
            
            print(f"\n📝 Test {i}/{len(test_queries)}: {query[:50]}...")
            
            start_time = time.time()
            try:
                # Test con timeout ridotto
                result = self.chatbot.chat(query)
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                
                # Controlla timeout
                if response_time > timeout_limit:
                    timeouts += 1
                    print(f"   ⏰ TIMEOUT: {response_time:.1f}s > {timeout_limit}s")
                else:
                    successes += 1
                    print(f"   ⚡ OK: {response_time:.1f}s")
                
                # Valuta retrieval (se disponibile)
                retrieved_docs = getattr(result, 'retrieved_docs', [])
                if retrieved_docs:
                    ret_metrics = self.evaluate_retrieval_quality(query, retrieved_docs, expected_topics)
                    retrieval_metrics.append(ret_metrics)
                
                # Valuta risposta
                response = result['response']
                resp_metrics = self.evaluate_response_quality(response, query)
                response_metrics.append(resp_metrics)
                
                # Valuta routing
                actual_redirect = result.get('should_redirect', False)
                routing_correct = (actual_redirect == expected_redirect)
                
                # Salva risultato dettagliato
                detailed_result = {
                    'query': query,
                    'response': response,
                    'response_time': response_time,
                    'expected_redirect': expected_redirect,
                    'actual_redirect': actual_redirect,
                    'routing_correct': routing_correct,
                    'retrieval_metrics': ret_metrics if retrieved_docs else {},
                    'response_metrics': resp_metrics,
                    'timeout': response_time > timeout_limit
                }
                results['detailed_results'].append(detailed_result)
                
            except Exception as e:
                print(f"   ❌ ERRORE: {str(e)}")
                timeouts += 1
        
        # Calcola metriche aggregate
        if response_times:
            results['performance']['avg_response_time'] = statistics.mean(response_times)
            results['performance']['median_response_time'] = statistics.median(response_times)
            results['performance']['timeout_rate'] = timeouts / len(test_queries)
            results['performance']['success_rate'] = successes / len(test_queries)
        
        if retrieval_metrics:
            results['retrieval_quality']['avg_diversity'] = statistics.mean([m['retrieval_diversity'] for m in retrieval_metrics])
            results['retrieval_quality']['avg_relevance'] = statistics.mean([m['context_relevance'] for m in retrieval_metrics])
            results['retrieval_quality']['avg_coverage'] = statistics.mean([m['topic_coverage'] for m in retrieval_metrics])
        
        if response_metrics:
            results['response_quality']['avg_specificity'] = statistics.mean([m['specificity'] for m in response_metrics])
            results['response_quality']['avg_completeness'] = statistics.mean([m['completeness'] for m in response_metrics])
            results['response_quality']['avg_clarity'] = statistics.mean([m['clarity'] for m in response_metrics])
            results['response_quality']['avg_length'] = statistics.mean([m['response_length'] for m in response_metrics])
        
        # Calcola accuratezza routing
        correct_routes = sum(1 for r in results['detailed_results'] if r['routing_correct'])
        results['routing_accuracy']['accuracy'] = correct_routes / len(results['detailed_results']) if results['detailed_results'] else 0
        
        return results
    
    def generate_advanced_report(self, results: Dict[str, Any]):
        """Genera report avanzato con grafici"""
        print(f"\n📊 GENERAZIONE REPORT AVANZATO...")
        
        # Crea DataFrame per analisi
        df = pd.DataFrame(results['detailed_results'])
        
        # Setup matplotlib
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('RAG System Evaluation - Advanced Metrics', fontsize=16, fontweight='bold')
        
        # 1. Distribution of Response Times
        axes[0, 0].hist(df['response_time'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].axvline(results['performance']['avg_response_time'], color='red', linestyle='--', label=f'Media: {results["performance"]["avg_response_time"]:.1f}s')
        axes[0, 0].set_title('Distribuzione Tempi di Risposta')
        axes[0, 0].set_xlabel('Tempo (secondi)')
        axes[0, 0].set_ylabel('Frequenza')
        axes[0, 0].legend()
        
        # 2. Response Quality Metrics
        quality_metrics = ['specificity', 'completeness', 'clarity']
        quality_values = [results['response_quality'][f'avg_{metric}'] for metric in quality_metrics]
        axes[0, 1].bar(quality_metrics, quality_values, color=['lightcoral', 'lightgreen', 'lightblue'])
        axes[0, 1].set_title('Qualità delle Risposte')
        axes[0, 1].set_ylabel('Score (0-1)')
        axes[0, 1].set_ylim(0, 1)
        
        # 3. Response Length Distribution
        axes[0, 2].hist([r['response_metrics']['response_length'] for r in results['detailed_results']], 
                       bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 2].set_title('Distribuzione Lunghezza Risposte')
        axes[0, 2].set_xlabel('Numero di Parole')
        axes[0, 2].set_ylabel('Frequenza')
        
        # 4. Routing Accuracy
        routing_data = [
            sum(1 for r in results['detailed_results'] if r['routing_correct']),
            sum(1 for r in results['detailed_results'] if not r['routing_correct'])
        ]
        axes[1, 0].pie(routing_data, labels=['Corretto', 'Sbagliato'], autopct='%1.1f%%', 
                      colors=['lightgreen', 'lightcoral'])
        axes[1, 0].set_title('Accuratezza Routing')
        
        # 5. Performance vs Quality Scatter
        if results['detailed_results']:
            x_times = [r['response_time'] for r in results['detailed_results']]
            y_quality = [r['response_metrics']['clarity'] for r in results['detailed_results']]
            axes[1, 1].scatter(x_times, y_quality, alpha=0.6, color='purple')
            axes[1, 1].set_title('Performance vs Qualità')
            axes[1, 1].set_xlabel('Tempo di Risposta (s)')
            axes[1, 1].set_ylabel('Clarity Score')
        
        # 6. Success Rate Overview
        success_data = [
            results['performance']['success_rate'] * 100,
            results['performance']['timeout_rate'] * 100
        ]
        axes[1, 2].bar(['Successi', 'Timeout'], success_data, color=['green', 'red'], alpha=0.7)
        axes[1, 2].set_title('Tasso di Successo')
        axes[1, 2].set_ylabel('Percentuale (%)')
        axes[1, 2].set_ylim(0, 100)
        
        plt.tight_layout()
        
        # Salva risultati
        os.makedirs('results', exist_ok=True)
        plt.savefig('results/rag_evaluation_advanced.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Salva dati JSON
        with open('results/rag_evaluation_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Genera report testuale
        report = self.generate_text_report(results)
        with open('results/rag_evaluation_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✅ Report salvati:")
        print("   📊 results/rag_evaluation_advanced.png")
        print("   📄 results/rag_evaluation_report.md")
        print("   📁 results/rag_evaluation_results.json")
        
        return results
    
    def generate_text_report(self, results: Dict[str, Any]) -> str:
        """Genera report testuale dettagliato"""
        report = f"""# RAG SYSTEM EVALUATION REPORT

**Data Evaluation**: {results['timestamp']}
**Queries Testate**: {results['total_queries']}

## 🚀 PERFORMANCE METRICS

| Metrica | Valore | Benchmark |
|---------|--------|-----------|
| Tempo Medio Risposta | {results['performance']['avg_response_time']:.2f}s | < 10s (Ottimo) |
| Tempo Mediano | {results['performance']['median_response_time']:.2f}s | < 5s (Ottimo) |
| Tasso Successo | {results['performance']['success_rate']*100:.1f}% | > 90% (Ottimo) |
| Tasso Timeout | {results['performance']['timeout_rate']*100:.1f}% | < 10% (Ottimo) |

## 📝 QUALITÀ RISPOSTE

| Metrica | Score | Descrizione |
|---------|-------|-------------|
| Specificità | {results['response_quality']['avg_specificity']:.2f} | Presenza info specifiche (link, numeri, date) |
| Completezza | {results['response_quality']['avg_completeness']:.2f} | Lunghezza appropriata della risposta |
| Chiarezza | {results['response_quality']['avg_clarity']:.2f} | Assenza errori e ridirection inutili |
| Lunghezza Media | {results['response_quality']['avg_length']:.1f} parole | 20-100 parole ottimale |

## 🎯 ROUTING ACCURACY

| Metrica | Valore |
|---------|--------|
| Accuratezza Routing | {results['routing_accuracy']['accuracy']*100:.1f}% |

## 📊 RETRIEVAL QUALITY
"""

        if results['retrieval_quality']['avg_diversity'] > 0:
            report += f"""
| Metrica | Score | Descrizione |
|---------|-------|-------------|
| Diversità Documenti | {results['retrieval_quality']['avg_diversity']:.2f} | Varietà contenuti recuperati |
| Rilevanza Contesto | {results['retrieval_quality']['avg_relevance']:.2f} | Pertinenza documenti alla query |
| Copertura Topic | {results['retrieval_quality']['avg_coverage']:.2f} | Completezza argomenti trattati |
"""
        
        report += f"""
## 🎖️ CLASSIFICAZIONE PERFORMANCE

"""
        
        # Classificazione basata sui risultati
        avg_time = results['performance']['avg_response_time']
        success_rate = results['performance']['success_rate']
        clarity = results['response_quality']['avg_clarity']
        
        if avg_time < 10 and success_rate > 0.9 and clarity > 0.8:
            grade = "🥇 ECCELLENTE"
        elif avg_time < 20 and success_rate > 0.8 and clarity > 0.7:
            grade = "🥈 BUONO"
        elif avg_time < 30 and success_rate > 0.7 and clarity > 0.6:
            grade = "🥉 SUFFICIENTE"
        else:
            grade = "❌ DA MIGLIORARE"
        
        report += f"**Valutazione Complessiva**: {grade}\n\n"
        
        # Raccomandazioni
        report += "## 💡 RACCOMANDAZIONI\n\n"
        
        if avg_time > 15:
            report += "- ⚡ **Ottimizzare Performance**: Ridurre timeout LLM e parametri generazione\n"
        
        if success_rate < 0.9:
            report += "- 🔧 **Migliorare Stabilità**: Gestire meglio timeout e errori\n"
        
        if clarity < 0.8:
            report += "- 📝 **Migliorare Prompt**: Ottimizzare istruzioni per LLM\n"
        
        if results['routing_accuracy']['accuracy'] < 0.8:
            report += "- 🎯 **Calibrare Routing**: Migliorare logica di redirection\n"
        
        return report

def main():
    """Funzione principale per evaluation avanzata"""
    evaluator = RAGEvaluator()
    
    print("🧪 AVVIO RAG EVALUATION AVANZATA")
    print("=" * 50)
    
    # Esegui evaluation completa
    results = evaluator.comprehensive_evaluation(sample_size=25, timeout_limit=15.0)
    
    if results:
        # Genera report
        evaluator.generate_advanced_report(results)
        
        # Summary finale
        print(f"\n📋 SUMMARY FINALE:")
        print(f"   Tempo Medio: {results['performance']['avg_response_time']:.1f}s")
        print(f"   Tasso Successo: {results['performance']['success_rate']*100:.1f}%")
        print(f"   Qualità Chiarezza: {results['response_quality']['avg_clarity']:.2f}")
        print(f"   Accuratezza Routing: {results['routing_accuracy']['accuracy']*100:.1f}%")
        
        # Classificazione finale
        if (results['performance']['avg_response_time'] < 15 and 
            results['performance']['success_rate'] > 0.8 and 
            results['response_quality']['avg_clarity'] > 0.7):
            print("   🎉 SISTEMA: PRODUZIONE READY!")
        else:
            print("   ⚠️ SISTEMA: RICHIEDE OTTIMIZZAZIONI")
    
    else:
        print("❌ Evaluation fallita")

if __name__ == "__main__":
    main()
