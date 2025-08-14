"""
Sistema di Evaluation del ChatBot RAG
Test automatici per valutare qualità e accuratezza
"""

import json
import time
import sys
import os

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import ChatbotRAG, setup_chatbot
import difflib
from sentence_transformers import SentenceTransformer, util

class ChatbotEvaluator:
    """Sistema di valutazione automatica del chatbot"""
    
    def __init__(self):
        self.chatbot = None
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.test_cases = self.load_test_cases()
    
    def load_test_cases(self):
        """Carica i casi di test"""
        return [
            {
                "id": 1,
                "category": "iscrizioni",
                "question": "Come faccio a iscrivermi agli esami?",
                "expected_keywords": ["iscrizione", "esami", "online", "sportello"],
                "expected_entities": ["esami", "iscrizione"],
                "should_redirect": False
            },
            {
                "id": 2,
                "category": "tasse",
                "question": "Quando devo pagare le tasse universitarie?",
                "expected_keywords": ["tasse", "pagamento", "scadenza", "contributo"],
                "expected_entities": ["tasse", "universitarie"],
                "should_redirect": False
            },
            {
                "id": 3,
                "category": "certificati",
                "question": "Come richiedo un certificato di laurea?",
                "expected_keywords": ["certificato", "laurea", "richiesta"],
                "expected_entities": ["certificato", "laurea"],
                "should_redirect": False
            },
            {
                "id": 4,
                "category": "contatti",
                "question": "Quali sono gli orari della segreteria?",
                "expected_keywords": ["orari", "segreteria", "contatti"],
                "expected_entities": ["segreteria", "orari"],
                "should_redirect": False
            },
            {
                "id": 5,
                "category": "personale",
                "question": "Come posso vedere i miei voti personali?",
                "expected_keywords": ["voti", "personali"],
                "expected_entities": ["voti"],
                "should_redirect": True  # Richiede dati personali
            },
            {
                "id": 6,
                "category": "specifico",
                "question": "Ho perso la mia tessera universitaria specifica, cosa faccio?",
                "expected_keywords": ["tessera", "universitaria"],
                "expected_entities": ["tessera"],
                "should_redirect": True  # Caso specifico
            }
        ]
    
    def setup_chatbot(self):
        """Inizializza il chatbot per i test"""
        print("🔄 Inizializzazione chatbot per evaluation...")
        self.chatbot = setup_chatbot()
        if not self.chatbot:
            raise Exception("Impossibile inizializzare il chatbot")
        print("✅ Chatbot pronto per evaluation")
    
    def evaluate_response_quality(self, question, response, expected_keywords):
        """Valuta la qualità della risposta"""
        response_lower = response.lower()
        question_lower = question.lower()
        
        # 1. Keyword Coverage
        keyword_score = sum(1 for keyword in expected_keywords 
                          if keyword.lower() in response_lower) / len(expected_keywords)
        
        # 2. Response Length (non troppo corta, non troppo lunga)
        length_score = 1.0
        if len(response) < 50:
            length_score = 0.5  # Troppo corta
        elif len(response) > 1000:
            length_score = 0.8  # Troppo lunga
        
        # 3. Semantic Similarity con la domanda
        question_embedding = self.embedding_model.encode([question_lower])
        response_embedding = self.embedding_model.encode([response_lower])
        semantic_score = util.cos_sim(question_embedding, response_embedding)[0][0].item()
        
        # 4. Presenza di informazioni utili (URL, contatti, procedure)
        utility_indicators = ['http', 'www', '@', 'telefono', 'mail', 'orari', 'procedura']
        utility_score = min(1.0, sum(1 for indicator in utility_indicators 
                                   if indicator in response_lower) / 3)
        
        return {
            'keyword_score': keyword_score,
            'length_score': length_score,
            'semantic_score': semantic_score,
            'utility_score': utility_score,
            'overall_score': (keyword_score + length_score + semantic_score + utility_score) / 4
        }
    
    def evaluate_redirect_accuracy(self, expected_redirect, actual_redirect):
        """Valuta l'accuratezza del sistema di redirect"""
        return 1.0 if expected_redirect == actual_redirect else 0.0
    
    def run_single_test(self, test_case):
        """Esegue un singolo test case"""
        question = test_case['question']
        expected_keywords = test_case['expected_keywords']
        expected_redirect = test_case['should_redirect']
        
        print(f"🧪 Test {test_case['id']}: {question}")
        
        start_time = time.time()
        try:
            result = self.chatbot.chat(question)
            response = result['response']
            actual_redirect = result['should_redirect']
            response_time = time.time() - start_time
            
            # Valuta qualità risposta
            quality_metrics = self.evaluate_response_quality(question, response, expected_keywords)
            
            # Valuta redirect accuracy
            redirect_accuracy = self.evaluate_redirect_accuracy(expected_redirect, actual_redirect)
            
            test_result = {
                'test_id': test_case['id'],
                'category': test_case['category'],
                'question': question,
                'response': response,
                'response_time': response_time,
                'quality_metrics': quality_metrics,
                'redirect_accuracy': redirect_accuracy,
                'expected_redirect': expected_redirect,
                'actual_redirect': actual_redirect,
                'status': 'PASS' if quality_metrics['overall_score'] > 0.6 and redirect_accuracy > 0.8 else 'FAIL'
            }
            
            print(f"  ✅ Completato - Score: {quality_metrics['overall_score']:.2f}")
            return test_result
            
        except Exception as e:
            print(f"  ❌ Errore: {str(e)}")
            return {
                'test_id': test_case['id'],
                'category': test_case['category'],
                'question': question,
                'error': str(e),
                'status': 'ERROR'
            }
    
    def run_full_evaluation(self):
        """Esegue valutazione completa"""
        if not self.chatbot:
            self.setup_chatbot()
        
        print("🚀 AVVIO EVALUATION COMPLETA")
        print("=" * 50)
        
        results = []
        start_time = time.time()
        
        for test_case in self.test_cases:
            result = self.run_single_test(test_case)
            results.append(result)
            time.sleep(1)  # Pausa tra i test
        
        total_time = time.time() - start_time
        
        # Calcola metriche aggregate
        successful_tests = [r for r in results if r.get('status') == 'PASS']
        failed_tests = [r for r in results if r.get('status') == 'FAIL']
        error_tests = [r for r in results if r.get('status') == 'ERROR']
        
        # Metriche di qualità
        quality_scores = [r['quality_metrics']['overall_score'] 
                         for r in results if 'quality_metrics' in r]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Metriche di performance
        response_times = [r['response_time'] for r in results if 'response_time' in r]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Accuracy redirect
        redirect_accuracies = [r['redirect_accuracy'] for r in results if 'redirect_accuracy' in r]
        avg_redirect_accuracy = sum(redirect_accuracies) / len(redirect_accuracies) if redirect_accuracies else 0
        
        summary = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': len(self.test_cases),
            'passed': len(successful_tests),
            'failed': len(failed_tests),
            'errors': len(error_tests),
            'success_rate': len(successful_tests) / len(self.test_cases) * 100,
            'avg_quality_score': avg_quality,
            'avg_response_time': avg_response_time,
            'avg_redirect_accuracy': avg_redirect_accuracy,
            'total_evaluation_time': total_time,
            'detailed_results': results
        }
        
        self.print_summary(summary)
        self.save_results(summary)
        
        return summary
    
    def print_summary(self, summary):
        """Stampa il riassunto della valutazione"""
        print("\n" + "=" * 60)
        print("📊 RISULTATI EVALUATION")
        print("=" * 60)
        print(f"🧪 Test totali: {summary['total_tests']}")
        print(f"✅ Successi: {summary['passed']}")
        print(f"❌ Fallimenti: {summary['failed']}")
        print(f"💥 Errori: {summary['errors']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        print(f"⭐ Quality Score: {summary['avg_quality_score']:.2f}/1.0")
        print(f"⚡ Avg Response Time: {summary['avg_response_time']:.2f}s")
        print(f"🎯 Redirect Accuracy: {summary['avg_redirect_accuracy']:.2f}")
        print(f"⏱️  Total Time: {summary['total_evaluation_time']:.2f}s")
        
        if summary['failed'] > 0:
            print("\n❌ TEST FALLITI:")
            failed_tests = [r for r in summary['detailed_results'] if r.get('status') == 'FAIL']
            for test in failed_tests:
                print(f"  - Test {test['test_id']}: {test['question']}")
    
    def save_results(self, summary, filename=None):
        """Salva i risultati in JSON"""
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"evaluation_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Risultati salvati in: {filename}")
        return filename

if __name__ == "__main__":
    # Esegue evaluation completa
    evaluator = ChatbotEvaluator()
    results = evaluator.run_full_evaluation()
    
    print(f"\n🎉 Evaluation completata!")
    print(f"📊 Success rate: {results['success_rate']:.1f}%")
    print(f"⭐ Quality score: {results['avg_quality_score']:.2f}/1.0")
