"""
Script di test per misurare miglioramenti qualità risposte
Confronta performance prima/dopo ottimizzazioni
"""

import sys
import os
sys.path.append('src')
sys.path.append('evaluation')

from ollama_llm import OllamaLLM
from metriche_qualità import evaluate_chatbot_response
from local_embeddings import LocalEmbeddings
from creazione_vectorstore import search_vectorstore

class QualityTester:
    """Tester per misurare qualità risposte"""
    
    def __init__(self):
        self.llm = OllamaLLM()
        self.embedder = LocalEmbeddings()
        
        # Dataset di test strutturato
        self.test_cases = [
            {
                "question": "Come faccio a iscrivermi agli esami?",
                "category": "iscrizioni",
                "expected_elements": ["portale", "procedura", "scadenza", "passo"]
            },
            {
                "question": "Quanto costano le tasse universitarie?",
                "category": "tasse", 
                "expected_elements": ["importo", "scadenza", "pagamento", "euro"]
            },
            {
                "question": "Quali sono gli orari della segreteria studenti?",
                "category": "orari",
                "expected_elements": ["orario", "apertura", "giorni", "contatto"]
            },
            {
                "question": "Come richiedere un certificato di laurea?",
                "category": "certificati",
                "expected_elements": ["richiesta", "tempo", "documento", "costo"]
            },
            {
                "question": "Ci sono servizi per studenti con disabilità?",
                "category": "servizi",
                "expected_elements": ["servizi", "supporto", "agevolazioni", "contatto"]
            }
        ]
    
    def run_comprehensive_test(self):
        """Esegue test completo e genera report"""
        
        print("🧪 TEST QUALITÀ CHATBOT - MIGLIORAMENTI")
        print("=" * 60)
        print("📊 Testing su {} domande di esempio".format(len(self.test_cases)))
        print()
        
        results = []
        total_score = 0
        category_scores = {}
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"🔍 TEST {i}/{len(self.test_cases)}")
            print(f"Categoria: {test_case['category'].upper()}")
            print(f"Domanda: {test_case['question']}")
            print("-" * 40)
            
            # Esegui test singolo
            result = self._test_single_question(test_case)
            results.append(result)
            
            # Statistiche
            score = result['metrics']['overall_score']
            total_score += score
            
            if test_case['category'] not in category_scores:
                category_scores[test_case['category']] = []
            category_scores[test_case['category']].append(score)
            
            # Output risultati
            self._print_test_result(result, test_case)
            print()
        
        # Report finale
        self._print_final_report(results, total_score, category_scores)
        
        return results
    
    def _test_single_question(self, test_case):
        """Testa una singola domanda"""
        
        question = test_case['question']
        
        # Recupera contesto
        try:
            docs_result = search_vectorstore(question, k=3, embedder=self.embedder)
            if docs_result["documents"] and docs_result["documents"][0]:
                context = "\n\n".join(docs_result["documents"][0][:2])
            else:
                context = "Informazioni non trovate nei documenti."
        except Exception as e:
            print(f"   ⚠️ Errore ricerca documenti: {e}")
            context = ""
        
        # Genera risposta
        try:
            response = self.llm.generate(question, context)
        except Exception as e:
            print(f"   ❌ Errore generazione risposta: {e}")
            response = "Errore nella generazione della risposta."
        
        # Valuta qualità
        evaluation = evaluate_chatbot_response(question, response, context)
        
        # Verifica elementi attesi
        expected_score = self._check_expected_elements(response, test_case['expected_elements'])
        
        return {
            'question': question,
            'response': response,
            'context_length': len(context),
            'response_length': len(response),
            'evaluation': evaluation,
            'metrics': evaluation['metrics'],
            'expected_elements_score': expected_score,
            'category': test_case['category']
        }
    
    def _check_expected_elements(self, response, expected_elements):
        """Verifica presenza di elementi attesi nella risposta"""
        
        response_lower = response.lower()
        found_elements = 0
        
        for element in expected_elements:
            if element.lower() in response_lower:
                found_elements += 1
        
        return found_elements / len(expected_elements) if expected_elements else 0.0
    
    def _print_test_result(self, result, test_case):
        """Stampa risultati di un singolo test"""
        
        metrics = result['metrics']
        evaluation = result['evaluation']
        
        print(f"📝 Risposta ({result['response_length']} caratteri):")
        print(f"   {result['response'][:150]}{'...' if len(result['response']) > 150 else ''}")
        print()
        
        print("📊 METRICHE QUALITÀ:")
        print(f"   🎯 Score Complessivo: {metrics['overall_score']:.3f} ({evaluation['quality_label']})")
        print(f"   🔍 Rilevanza: {metrics.get('semantic_similarity', 0):.3f} ({evaluation['main_areas']['rilevanza']})")
        print(f"   📋 Completezza: {metrics.get('completeness_score', 0):.3f} ({evaluation['main_areas']['completezza']})")
        print(f"   ✨ Chiarezza: {metrics.get('clarity_score', 0):.3f} ({evaluation['main_areas']['chiarezza']})")
        print(f"   🎓 Professionalità: {metrics.get('professional_tone', 0):.3f}")
        print(f"   📚 Uso Contesto: {metrics.get('context_utilization', 0):.3f}")
        print(f"   ✅ Elementi Attesi: {result['expected_elements_score']:.1%}")
        
        # Indicatore visuale
        score = metrics['overall_score']
        if score >= 0.8:
            indicator = "🟢 ECCELLENTE"
        elif score >= 0.6:
            indicator = "🟡 BUONO"
        elif score >= 0.4:
            indicator = "🟠 SUFFICIENTE"
        else:
            indicator = "🔴 DA MIGLIORARE"
        
        print(f"   {indicator}")
    
    def _print_final_report(self, results, total_score, category_scores):
        """Stampa report finale dei test"""
        
        avg_score = total_score / len(results)
        baseline_score = 0.633  # Il tuo score precedente
        
        print("=" * 60)
        print("📈 REPORT FINALE - MIGLIORAMENTI QUALITÀ")
        print("=" * 60)
        
        print(f"🎯 PERFORMANCE GENERALE:")
        print(f"   Score Medio Attuale: {avg_score:.3f}")
        print(f"   Score Baseline: {baseline_score:.3f}")
        
        improvement = ((avg_score - baseline_score) / baseline_score) * 100
        if improvement > 0:
            print(f"   📈 Miglioramento: +{improvement:.1f}%")
        else:
            print(f"   📉 Peggioramento: {improvement:.1f}%")
        
        print(f"\n📊 PERFORMANCE PER CATEGORIA:")
        for category, scores in category_scores.items():
            avg_cat_score = sum(scores) / len(scores)
            print(f"   {category.capitalize()}: {avg_cat_score:.3f}")
        
        print(f"\n🔍 ANALISI DETTAGLIATA:")
        
        # Metriche aggregate
        all_metrics = {}
        for result in results:
            for metric, value in result['metrics'].items():
                if metric not in all_metrics:
                    all_metrics[metric] = []
                all_metrics[metric].append(value)
        
        for metric, values in all_metrics.items():
            if metric != 'overall_score':
                avg_value = sum(values) / len(values)
                print(f"   {metric}: {avg_value:.3f}")
        
        # Raccomandazioni
        print(f"\n💡 RACCOMANDAZIONI:")
        
        worst_metric = min(all_metrics.items(), key=lambda x: sum(x[1])/len(x[1]) if x[0] != 'overall_score' else 1)
        best_metric = max(all_metrics.items(), key=lambda x: sum(x[1])/len(x[1]) if x[0] != 'overall_score' else 0)
        
        print(f"   🔴 Area da migliorare: {worst_metric[0]} ({sum(worst_metric[1])/len(worst_metric[1]):.3f})")
        print(f"   🟢 Punto di forza: {best_metric[0]} ({sum(best_metric[1])/len(best_metric[1]):.3f})")
        
        if avg_score > baseline_score + 0.05:
            print("   ✅ Ottimizzazioni efficaci - continuare su questa strada")
        elif avg_score > baseline_score:
            print("   🟡 Miglioramento lieve - considerare ulteriori ottimizzazioni")
        else:
            print("   ⚠️ Necessarie ulteriori ottimizzazioni")

def run_quick_test():
    """Test rapido per verifica funzionamento"""
    
    print("⚡ QUICK TEST")
    print("=" * 30)
    
    tester = QualityTester()
    
    # Test su una sola domanda
    test_case = {
        "question": "Come faccio a iscrivermi agli esami?",
        "category": "test",
        "expected_elements": ["portale", "procedura"]
    }
    
    result = tester._test_single_question(test_case)
    tester._print_test_result(result, test_case)
    
    return result['metrics']['overall_score']

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Test rapido
        score = run_quick_test()
        print(f"\n🎯 Quick Test Score: {score:.3f}")
    else:
        # Test completo
        tester = QualityTester()
        results = tester.run_comprehensive_test()
        
        # Salva risultati per analisi successiva
        import json
        with open("test_results.json", "w", encoding="utf-8") as f:
            # Converti risultati in formato serializzabile
            serializable_results = []
            for result in results:
                serializable_results.append({
                    'question': result['question'],
                    'category': result['category'],
                    'response_length': result['response_length'],
                    'metrics': result['metrics'],
                    'expected_elements_score': result['expected_elements_score']
                })
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Risultati salvati in: test_results.json")