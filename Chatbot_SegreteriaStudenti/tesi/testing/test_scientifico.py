# tesi/testing/test_scientifico.py

"""
Sistema Test Automatizzato - Validazione Scientifica Chatbot
Test rigoroso con 30+ domande e metriche avanzate
"""

import json
import time
import sys
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import re

# Aggiungi path per importare il chatbot
sys.path.append(str(Path(__file__).parent.parent.parent))

@dataclass
class TestResult:
    """Risultato di un singolo test"""
    question_id: str
    question: str
    response: str
    response_time: float
    links_found: List[str]
    expected_links: List[str]
    category: str
    difficulty: str
    quality_score: float
    completeness_score: float
    link_accuracy: float
    overall_score: float

class ChatbotTester:
    """Sistema di test automatizzato per il chatbot"""
    
    def __init__(self, dataset_path: str = "ground_truth_responses.json"):
        self.dataset_path = Path(dataset_path)
        self.results_dir = Path("risultati_test")
        self.results_dir.mkdir(exist_ok=True)
        
        # Carica dataset
        self.dataset_data = self._load_dataset()
        self.dataset = self.dataset_data['dataset']
        self.ground_truth = self.dataset_data['ground_truth']
        
        # Inizializza chatbot (simulazione se non disponibile)
        self.chatbot = self._initialize_chatbot()
        
        print(f"✅ Tester inizializzato con {self._count_total_questions()} domande")
    
    def _load_dataset(self) -> Dict:
        """Carica dataset di test"""
        if not self.dataset_path.exists():
            print("❌ Dataset non trovato, creo dataset di esempio...")
            # Se non esiste, crea dataset base
            return self._create_fallback_dataset()
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_fallback_dataset(self) -> Dict:
        """Crea dataset di fallback se non disponibile"""
        return {
            'dataset': {
                'iscrizioni_esami': [
                    {
                        'id': 'ISC_001',
                        'question': 'Come posso iscrivermi all\'esame di Analisi Matematica I?',
                        'expected_keywords': ['iscrizione', 'esame', 'portale'],
                        'expected_links': ['portale_studente'],
                        'difficulty': 'facile',
                        'category': 'iscrizioni'
                    }
                ]
            },
            'ground_truth': {
                'ISC_001': {
                    'quality_score': 0.8,
                    'completeness': 'completa',
                    'link_count_expected': 1
                }
            }
        }
    
    def _initialize_chatbot(self):
        """Inizializza il chatbot per il testing"""
        try:
            # Prova a importare il chatbot reale
            from src.ollama_llm import ChatbotOllama  # Adatta al tuo import
            return ChatbotOllama()
        except ImportError:
            print("⚠️ Chatbot non disponibile, uso simulazione per testing")
            return MockChatbot()
    
    def _count_total_questions(self) -> int:
        """Conta domande totali nel dataset"""
        return sum(len(questions) for questions in self.dataset.values())
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Esegue test completo su tutte le domande"""
        print("\n🧪 AVVIO TEST SCIENTIFICO COMPLETO")
        print("=" * 50)
        
        start_time = time.time()
        all_results = []
        
        # Test per ogni categoria
        for category_name, questions in self.dataset.items():
            print(f"\n📋 Testing categoria: {category_name.upper()}")
            
            for question_data in questions:
                result = self._test_single_question(question_data)
                all_results.append(result)
                
                # Progress feedback
                print(f"   ✅ {result.question_id}: Score {result.overall_score:.3f}")
        
        total_time = time.time() - start_time
        
        # Calcola metriche aggregate
        metrics = self._calculate_comprehensive_metrics(all_results)
        
        # Salva risultati
        test_report = {
            'metadata': {
                'test_date': datetime.now().isoformat(),
                'total_questions': len(all_results),
                'total_time_seconds': total_time,
                'avg_time_per_question': total_time / len(all_results)
            },
            'individual_results': [self._result_to_dict(r) for r in all_results],
            'aggregate_metrics': metrics,
            'performance_by_category': self._analyze_by_category(all_results),
            'performance_by_difficulty': self._analyze_by_difficulty(all_results)
        }
        
        # Salva JSON dettagliato
        results_file = self.results_dir / f"test_results_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(test_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n🏆 TEST COMPLETATO!")
        print(f"📊 Risultati salvati in: {results_file}")
        print(f"⏱️ Tempo totale: {total_time:.2f}s")
        print(f"📈 Score medio: {metrics['overall_accuracy']:.3f}")
        
        return test_report
    
    def _test_single_question(self, question_data: Dict) -> TestResult:
        """Testa una singola domanda"""
        question_id = question_data['id']
        question = question_data['question']
        
        # Misura tempo di risposta
        start_time = time.time()
        
        try:
            # Ottieni risposta dal chatbot
            response = self.chatbot.get_response(question)
            response_time = time.time() - start_time
            
            # Estrai link dalla risposta
            links_found = self._extract_links_from_response(response)
            
        except Exception as e:
            print(f"❌ Errore durante test {question_id}: {e}")
            response = f"ERRORE: {str(e)}"
            response_time = 0.0
            links_found = []
        
        # Calcola metriche qualità
        quality_score = self._calculate_response_quality(response, question_data)
        completeness_score = self._calculate_completeness(response, question_data)
        link_accuracy = self._calculate_link_accuracy(links_found, question_data.get('expected_links', []))
        
        # Score complessivo
        overall_score = (quality_score * 0.4 + completeness_score * 0.3 + link_accuracy * 0.3)
        
        return TestResult(
            question_id=question_id,
            question=question,
            response=response,
            response_time=response_time,
            links_found=links_found,
            expected_links=question_data.get('expected_links', []),
            category=question_data['category'],
            difficulty=question_data['difficulty'],
            quality_score=quality_score,
            completeness_score=completeness_score,
            link_accuracy=link_accuracy,
            overall_score=overall_score
        )
    
    def _extract_links_from_response(self, response: str) -> List[str]:
        """Estrae link/riferimenti dalla risposta"""
        # Pattern per identificare link comuni
        link_patterns = [
            r'portale[_\s]*studente',
            r'email[_\s]*segreteria',
            r'telefono[_\s]*segreteria', 
            r'sito[_\s]*università',
            r'calendario[_\s]*accademico',
            r'regolamento',
            r'modulo[_\s]*',
            r'ufficio[_\s]*',
            r'biblioteca',
            r'laboratori'
        ]
        
        found_links = []
        response_lower = response.lower()
        
        for pattern in link_patterns:
            if re.search(pattern, response_lower):
                found_links.append(pattern.replace(r'[_\s]*', '_'))
        
        return list(set(found_links))  # Rimuovi duplicati
    
    def _calculate_response_quality(self, response: str, question_data: Dict) -> float:
        """Calcola qualità della risposta basata su keywords attese"""
        if not response or response.startswith('ERRORE'):
            return 0.0
        
        expected_keywords = question_data.get('expected_keywords', [])
        if not expected_keywords:
            return 0.7  # Score neutro se non ci sono keywords attese
        
        response_lower = response.lower()
        found_keywords = sum(1 for keyword in expected_keywords 
                           if keyword.lower() in response_lower)
        
        keyword_score = found_keywords / len(expected_keywords)
        
        # Bonus per lunghezza appropriata (50-500 caratteri ideale)
        length_score = 1.0
        if len(response) < 30:
            length_score = 0.5  # Troppo corta
        elif len(response) > 800:
            length_score = 0.8  # Troppo lunga
        
        return min(keyword_score * length_score, 1.0)
    
    def _calculate_completeness(self, response: str, question_data: Dict) -> float:
        """Calcola completezza della risposta"""
        if not response or response.startswith('ERRORE'):
            return 0.0
        
        # Criteri completezza
        completeness_indicators = [
            len(response) > 50,  # Minima lunghezza
            '.' in response,     # Frasi complete
            any(word in response.lower() for word in ['devi', 'puoi', 'è possibile', 'per']),  # Azione chiara
            not response.lower().startswith('non so')  # Non incertezza
        ]
        
        return sum(completeness_indicators) / len(completeness_indicators)
    
    def _calculate_link_accuracy(self, found_links: List[str], expected_links: List[str]) -> float:
        """Calcola accuratezza dei link trovati"""
        if not expected_links:
            return 1.0  # Perfetto se non ci sono link attesi
        
        if not found_links:
            return 0.0  # Zero se non trova link ma sono attesi
        
        # Calcola overlap tra link trovati e attesi
        found_set = set(link.lower() for link in found_links)
        expected_set = set(link.lower() for link in expected_links)
        
        if not expected_set:
            return 1.0
        
        intersection = len(found_set.intersection(expected_set))
        precision = intersection / len(found_set) if found_set else 0
        recall = intersection / len(expected_set) if expected_set else 0
        
        # F1-score
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    def _calculate_comprehensive_metrics(self, results: List[TestResult]) -> Dict[str, float]:
        """Calcola metriche aggregate complete"""
        if not results:
            return {}
        
        scores = [r.overall_score for r in results]
        quality_scores = [r.quality_score for r in results]
        completeness_scores = [r.completeness_score for r in results]
        link_accuracies = [r.link_accuracy for r in results]
        response_times = [r.response_time for r in results]
        
        return {
            'overall_accuracy': np.mean(scores),
            'overall_std': np.std(scores),
            'quality_avg': np.mean(quality_scores),
            'completeness_avg': np.mean(completeness_scores),
            'link_accuracy_avg': np.mean(link_accuracies),
            'avg_response_time': np.mean(response_times),
            'median_response_time': np.median(response_times),
            'min_score': min(scores),
            'max_score': max(scores),
            'questions_above_threshold': sum(1 for score in scores if score >= 0.7),
            'success_rate': sum(1 for score in scores if score >= 0.7) / len(scores),
            'confidence_interval_95': {
                'lower': np.mean(scores) - 1.96 * np.std(scores) / np.sqrt(len(scores)),
                'upper': np.mean(scores) + 1.96 * np.std(scores) / np.sqrt(len(scores))
            }
        }
    
    def _analyze_by_category(self, results: List[TestResult]) -> Dict[str, Dict]:
        """Analizza performance per categoria"""
        categories = {}
        
        for result in results:
            cat = result.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        analysis = {}
        for cat, cat_results in categories.items():
            scores = [r.overall_score for r in cat_results]
            analysis[cat] = {
                'count': len(cat_results),
                'avg_score': np.mean(scores),
                'std_score': np.std(scores),
                'min_score': min(scores),
                'max_score': max(scores),
                'success_rate': sum(1 for score in scores if score >= 0.7) / len(scores)
            }
        
        return analysis
    
    def _analyze_by_difficulty(self, results: List[TestResult]) -> Dict[str, Dict]:
        """Analizza performance per difficoltà"""
        difficulties = {}
        
        for result in results:
            diff = result.difficulty
            if diff not in difficulties:
                difficulties[diff] = []
            difficulties[diff].append(result)
        
        analysis = {}
        for diff, diff_results in difficulties.items():
            scores = [r.overall_score for r in diff_results]
            analysis[diff] = {
                'count': len(diff_results),
                'avg_score': np.mean(scores),
                'std_score': np.std(scores),
                'success_rate': sum(1 for score in scores if score >= 0.7) / len(scores)
            }
        
        return analysis
    
    def _result_to_dict(self, result: TestResult) -> Dict:
        """Converte TestResult in dizionario"""
        return {
            'question_id': result.question_id,
            'question': result.question,
            'response': result.response,
            'response_time': result.response_time,
            'links_found': result.links_found,
            'expected_links': result.expected_links,
            'category': result.category,
            'difficulty': result.difficulty,
            'scores': {
                'quality': result.quality_score,
                'completeness': result.completeness_score,
                'link_accuracy': result.link_accuracy,
                'overall': result.overall_score
            }
        }
    
    def generate_performance_report(self, test_report: Dict) -> str:
        """Genera report testuale dei risultati"""
        metrics = test_report['aggregate_metrics']
        
        report = f"""
# 📊 REPORT TEST SCIENTIFICO CHATBOT SEGRETERIA STUDENTI

## 📈 METRICHE GENERALI
- **Accuracy Complessiva**: {metrics['overall_accuracy']:.3f} ± {metrics['overall_std']:.3f}
- **Tasso di Successo**: {metrics['success_rate']:.1%} (soglia ≥ 0.7)
- **Tempo Risposta Medio**: {metrics['avg_response_time']:.2f}s
- **Tempo Risposta Mediano**: {metrics['median_response_time']:.2f}s

## 🎯 INTERVALLO DI CONFIDENZA (95%)
- **Range**: [{metrics['confidence_interval_95']['lower']:.3f}, {metrics['confidence_interval_95']['upper']:.3f}]

## 📊 PERFORMANCE PER COMPONENTE
- **Qualità Contenuto**: {metrics['quality_avg']:.3f}
- **Completezza Risposta**: {metrics['completeness_avg']:.3f}  
- **Accuratezza Link**: {metrics['link_accuracy_avg']:.3f}

## 📋 PERFORMANCE PER CATEGORIA
"""
        
        for cat, data in test_report['performance_by_category'].items():
            report += f"- **{cat.title()}**: {data['avg_score']:.3f} (n={data['count']}, successo={data['success_rate']:.1%})\n"
        
        report += f"""
## 🎯 PERFORMANCE PER DIFFICOLTÀ
"""
        
        for diff, data in test_report['performance_by_difficulty'].items():
            report += f"- **{diff.title()}**: {data['avg_score']:.3f} (n={data['count']}, successo={data['success_rate']:.1%})\n"
        
        report += f"""
## 🏆 RISULTATI ECCELLENTI
- **Score Massimo**: {metrics['max_score']:.3f}
- **Score Minimo**: {metrics['min_score']:.3f}
- **Domande Sopra Soglia**: {metrics['questions_above_threshold']}/{len(test_report['individual_results'])}

## 📊 STATISTICHE TEST
- **Domande Totali**: {test_report['metadata']['total_questions']}
- **Tempo Totale**: {test_report['metadata']['total_time_seconds']:.1f}s
- **Data Test**: {test_report['metadata']['test_date']}
        """
        
        return report


class MockChatbot:
    """Chatbot simulato per testing quando il vero chatbot non è disponibile"""
    
    def __init__(self):
        self.responses = {
            'iscrizione': "Per iscriverti all'esame devi accedere al portale studente con le tue credenziali. La scadenza è 7 giorni prima dell'appello. Contatta la segreteria per assistenza.",
            'tasse': "Le tasse universitarie vanno pagate in tre rate secondo il calendario accademico. Puoi utilizzare il portale pagamenti online o bonifico bancario.",
            'certificato': "I certificati possono essere richiesti online tramite il portale certificati. Il documento è disponibile in formato PDF dopo la richiesta.",
            'orari': "La segreteria è aperta dal lunedì al venerdì dalle 9:00 alle 13:00. Per urgenze contatta l'email segreteria o il telefono diretto.",
            'servizi': "La biblioteca universitaria offre servizi di consultazione, prestito e accesso alle banche dati. Presentati con la tessera studente."
        }
    
    def get_response(self, question: str) -> str:
        """Simula risposta del chatbot basata su keywords"""
        question_lower = question.lower()
        
        # Aggiungi delay realistico
        time.sleep(np.random.uniform(0.5, 2.0))
        
        # Identifica categoria dalla domanda
        if any(word in question_lower for word in ['iscri', 'esame']):
            return self.responses['iscrizione']
        elif any(word in question_lower for word in ['tasse', 'pagam']):
            return self.responses['tasse']
        elif any(word in question_lower for word in ['certificat', 'diplom', 'document']):
            return self.responses['certificato']
        elif any(word in question_lower for word in ['orari', 'apertur', 'contatt']):
            return self.responses['orari']
        elif any(word in question_lower for word in ['biblioteca', 'serviz', 'laboratori']):
            return self.responses['servizi']
        else:
            return "Mi dispiace, non ho informazioni specifiche su questo argomento. Ti consiglio di contattare direttamente la segreteria studenti."


if __name__ == "__main__":
    print("🧪 AVVIO SISTEMA TEST SCIENTIFICO")
    
    # Inizializza tester
    tester = ChatbotTester()
    
    # Esegui test completo
    results = tester.run_comprehensive_test()
    
    # Genera report
    report_text = tester.generate_performance_report(results)
    
    # Salva report
    report_file = Path("risultati_test/performance_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"📄 Report salvato in: {report_file}")
    print("\n🎉 TEST SCIENTIFICO COMPLETATO!")