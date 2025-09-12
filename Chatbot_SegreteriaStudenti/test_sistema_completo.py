# Crea: test_sistema_completo.py

"""
Test finale del sistema completo con tutte le ottimizzazioni
"""

import sys
sys.path.append('src')
sys.path.append('evaluation')

from ollama_llm import OllamaLLM
from metriche_qualità import evaluate_chatbot_response
from local_embeddings import LocalEmbeddings
from creazione_vectorstore import search_vectorstore
import time
import json

class SystemTester:
    """Tester per sistema completo ottimizzato"""
    
    def __init__(self):
        self.llm = OllamaLLM()
        self.embedder = LocalEmbeddings()
        self.results = []
    
    def test_complete_system(self):
        """Test sistema completo con tutte le ottimizzazioni"""
        
        print("🎯 TEST SISTEMA COMPLETO - TUTTE LE OTTIMIZZAZIONI")
        print("=" * 60)
        
        # Test cases ottimizzati
        test_cases = [
            {
                "question": "Come faccio a iscrivermi agli esami?",
                "category": "iscrizioni_esami",
                "expected_elements": ["portale", "procedura", "passo", "iscrizione"]
            },
            {
                "question": "Quanto costano le tasse universitarie?", 
                "category": "tasse_pagamenti",
                "expected_elements": ["importo", "scadenza", "pagamento"]
            },
            {
                "question": "Quali sono gli orari della segreteria studenti?",
                "category": "orari_contatti", 
                "expected_elements": ["orario", "lunedì", "venerdì"]
            },
            {
                "question": "Come richiedere un certificato di laurea?",
                "category": "certificati_documenti",
                "expected_elements": ["richiesta", "documento", "procedura"]
            },
            {
                "question": "Ci sono servizi per studenti con disabilità?",
                "category": "servizi_studenti",
                "expected_elements": ["servizi", "supporto", "agevolazioni"]
            }
        ]
        
        total_score = 0
        total_links = 0
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n🔍 TEST {i}/{len(test_cases)} - {case['category'].upper()}")
            print(f"Domanda: {case['question']}")
            print("-" * 50)
            
            # Cerca contesto
            try:
                docs = search_vectorstore(case['question'], k=3, embedder=self.embedder)
                context = "\n".join(docs["documents"][0][:2]) if docs["documents"][0] else ""
                print(f"✅ Contesto: {len(context)} caratteri")
            except Exception as e:
                print(f"⚠️ Errore ricerca: {e}")
                context = ""
            
            # Genera risposta con TUTTE le ottimizzazioni
            start_time = time.time()
            try:
                response = self.llm.generate(case['question'], context)
                response_time = time.time() - start_time
                print(f"✅ Risposta generata ({len(response)} caratteri, {response_time:.1f}s)")
            except Exception as e:
                print(f"❌ Errore generazione: {e}")
                continue
            
            # Conta link (nuova metrica!)
            link_count = self.llm.link_enhancer.count_links(response) if hasattr(self.llm, 'link_enhancer') else 0
            total_links += link_count
            
            # Valuta qualità
            evaluation = evaluate_chatbot_response(case['question'], response, context)
            metrics = evaluation['metrics']
            score = metrics['overall_score']
            total_score += score
            
            # Anteprima risposta
            print(f"\n📝 Risposta ({len(response)} caratteri):")
            print(f"   {response[:120]}...")
            
            # Metriche dettagliate
            print(f"\n📊 METRICHE QUALITÀ:")
            print(f"   🎯 Score Complessivo: {score:.3f} ({evaluation['quality_label']})")
            print(f"   🔍 Rilevanza: {metrics.get('semantic_similarity', 0):.3f}")
            print(f"   📋 Completezza: {metrics.get('completeness_score', 0):.3f}")
            print(f"   ✨ Chiarezza: {metrics.get('clarity_score', 0):.3f}")
            print(f"   🎓 Professionalità: {metrics.get('professional_tone', 0):.3f}")
            print(f"   🔗 Link: {link_count} link")
            
            # Salva risultato
            self.results.append({
                'category': case['category'],
                'question': case['question'],
                'score': score,
                'links': link_count,
                'response_time': response_time,
                'response_length': len(response),
                'metrics': metrics
            })
            
            # Indicatore qualità
            if score >= 0.8:
                print("   🟢 ECCELLENTE")
            elif score >= 0.65:
                print("   🟡 BUONO")
            else:
                print("   🟠 SUFFICIENTE")
        
        # Calcola risultati finali
        avg_score = total_score / len(test_cases)
        avg_links = total_links / len(test_cases)
        baseline_score = 0.633
        improvement = ((avg_score - baseline_score) / baseline_score) * 100
        
        print(f"\n🎯 RISULTATI FINALI SISTEMA COMPLETO")
        print("=" * 60)
        print(f"📈 PERFORMANCE GENERALE:")
        print(f"   Score Medio Finale: {avg_score:.3f}")
        print(f"   Score Baseline: {baseline_score:.3f}")
        print(f"   🚀 MIGLIORAMENTO TOTALE: +{improvement:.1f}%")
        print(f"   🔗 Link medi per risposta: {avg_links:.1f}")
        
        print(f"\n📊 BREAKDOWN PER CATEGORIA:")
        for result in self.results:
            cat_improvement = ((result['score'] - baseline_score) / baseline_score) * 100
            print(f"   {result['category']}: {result['score']:.3f} (+{cat_improvement:.1f}%) - {result['links']} link")
        
        # Confronto con obiettivi
        print(f"\n🎯 VALUTAZIONE VS OBIETTIVI:")
        if improvement >= 20:
            print(f"   ✅ ECCELLENTE: +{improvement:.1f}% (target era +15-20%)")
        elif improvement >= 15:
            print(f"   ✅ OTTIMO: +{improvement:.1f}% (target raggiunto)")
        elif improvement >= 10:
            print(f"   🟡 BUONO: +{improvement:.1f}% (vicino al target)")
        else:
            print(f"   🟠 SUFFICIENTE: +{improvement:.1f}% (sotto target)")
        
        # Link enhancement success
        if avg_links >= 3:
            print(f"   ✅ LINK SYSTEM: {avg_links:.1f} link/risposta (eccellente)")
        elif avg_links >= 1:
            print(f"   🟡 LINK SYSTEM: {avg_links:.1f} link/risposta (buono)")
        else:
            print(f"   🟠 LINK SYSTEM: {avg_links:.1f} link/risposta (da migliorare)")
        
        # Salva risultati
        self._save_results(avg_score, improvement, avg_links)
        
        return avg_score, improvement, avg_links
    
    def _save_results(self, avg_score, improvement, avg_links):
        """Salva risultati per la tesi"""
        
        results_summary = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'system_version': 'Complete Optimized System v2.0',
            'optimizations_applied': [
                'Template prompt ottimizzati',
                'Sistema link automatico', 
                'Context enhancement',
                'Response post-processing'
            ],
            'performance': {
                'final_score': avg_score,
                'baseline_score': 0.633,
                'improvement_percentage': improvement,
                'average_links_per_response': avg_links
            },
            'detailed_results': self.results
        }
        
        with open('sistema_completo_results.json', 'w', encoding='utf-8') as f:
            json.dump(results_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Risultati salvati in: sistema_completo_results.json")

if __name__ == "__main__":
    tester = SystemTester()
    score, improvement, links = tester.test_complete_system()
    
    print(f"\n🏆 SISTEMA PRONTO PER STEP 5!")
    print(f"   Score: {score:.3f} (+{improvement:.1f}%)")
    print(f"   Links: {links:.1f}/risposta")