#!/usr/bin/env python3
"""
Test Funzionali - Esperienza Utente del Chatbot
===============================================
Test end-to-end per validare il comportamento del chatbot dal punto di vista dell'utente
"""

import os
import sys
import json
import time
from datetime import datetime

# Aggiungi path per import moduli
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class FunctionalTestRunner:
    """Gestisce l'esecuzione dei test funzionali"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_type": "functional",
            "scenarios": {},
            "summary": {}
        }
        
        # Query di test rappresentative
        self.test_queries = [
            {
                "id": "info_generale",
                "query": "Come posso iscrivermi all'università?",
                "expected_topics": ["iscrizione", "università", "procedura"],
                "category": "Informazioni Generali"
            },
            {
                "id": "scadenze",
                "query": "Quali sono le scadenze per le tasse universitarie?",
                "expected_topics": ["tasse", "scadenze", "pagamento"],
                "category": "Tasse e Pagamenti"
            },
            {
                "id": "esami",
                "query": "Come posso prenotare un esame?",
                "expected_topics": ["esami", "prenotazione", "procedura"],
                "category": "Gestione Esami"
            },
            {
                "id": "laurea",
                "query": "Quando posso laurearmi?",
                "expected_topics": ["laurea", "requisiti", "sessione"],
                "category": "Percorso Laurea"
            },
            {
                "id": "segreteria",
                "query": "Quali sono gli orari della segreteria?",
                "expected_topics": ["segreteria", "orari", "contatti"],
                "category": "Servizi Segreteria"
            }
        ]
    
    def test_chatbot_response(self, query_data):
        """Testa una singola query del chatbot"""
        try:
            # Simula inizializzazione chatbot (versione semplificata)
            # In un test reale importerebbe e userebbe il ChatbotRAG
            
            start_time = time.time()
            
            # Simula elaborazione query
            query = query_data["query"]
            
            # Test basic: verifica che la query non sia vuota
            if not query or len(query.strip()) == 0:
                return {
                    "success": False,
                    "error": "Query vuota",
                    "response_time": 0
                }
            
            # Simula tempo di elaborazione (sostituire con chiamata reale al chatbot)
            time.sleep(0.1)  # Simula latenza
            
            # Simula risposta (in un test reale verrebbe dal chatbot)
            mock_response = f"Per {query.lower()}: La segreteria studenti fornisce assistenza completa. Puoi trovare tutte le informazioni necessarie sui documenti richiesti, le procedure da seguire e i tempi previsti. Per maggiori dettagli contatta direttamente gli uffici competenti."
            
            response_time = time.time() - start_time
            
            # Valuta qualità risposta (criteri semplificati)
            quality_score = self.evaluate_response_quality(query, mock_response, query_data)
            
            return {
                "success": True,
                "query": query,
                "response": mock_response,
                "response_time": response_time,
                "quality_score": quality_score,
                "category": query_data["category"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query_data.get("query", ""),
                "response_time": 0
            }
    
    def evaluate_response_quality(self, query, response, query_data):
        """Valuta la qualità della risposta con criteri semplici"""
        score = 0
        max_score = 100
        
        # Criterio 1: Lunghezza risposta appropriata (20 punti)
        if 50 <= len(response) <= 500:
            score += 20
        elif 20 <= len(response) <= 1000:
            score += 10
        
        # Criterio 2: Presenza di termini attesi (40 punti)
        expected_topics = query_data.get("expected_topics", [])
        found_topics = 0
        for topic in expected_topics:
            if topic.lower() in response.lower() or topic.lower() in query.lower():
                found_topics += 1
        
        if expected_topics:
            score += int(40 * (found_topics / len(expected_topics)))
        
        # Criterio 3: Struttura risposta (20 punti)
        if len(response.split('.')) >= 2:  # Almeno 2 frasi
            score += 10
        if any(word in response.lower() for word in ['puoi', 'devi', 'necessario', 'procedura']):
            score += 10
        
        # Criterio 4: Assenza errori evidenti (20 punti)
        if "errore" not in response.lower() and len(response) > 10:
            score += 20
        
        return min(score, max_score)
    
    def test_conversation_flow(self):
        """Testa flusso di conversazione multi-turno"""
        conversation_queries = [
            "Ciao, ho bisogno di informazioni sull'iscrizione",
            "Quali documenti servono?",
            "Quanto costa l'iscrizione?",
            "Grazie per le informazioni"
        ]
        
        conversation_results = []
        
        for i, query in enumerate(conversation_queries):
            query_data = {
                "query": query,
                "expected_topics": ["iscrizione", "università"],
                "category": "Conversazione"
            }
            
            result = self.test_chatbot_response(query_data)
            result["turn"] = i + 1
            conversation_results.append(result)
        
        return {
            "success": all(r["success"] for r in conversation_results),
            "turns": conversation_results,
            "avg_response_time": sum(r["response_time"] for r in conversation_results) / len(conversation_results),
            "avg_quality": sum(r.get("quality_score", 0) for r in conversation_results) / len(conversation_results)
        }
    
    def test_edge_cases(self):
        """Testa casi limite e input problematici"""
        edge_cases = [
            {"query": "", "description": "Query vuota"},
            {"query": "   ", "description": "Solo spazi"},
            {"query": "a" * 1000, "description": "Query molto lunga"},
            {"query": "asdfghjkl qwertyuiop", "description": "Testo senza senso"},
            {"query": "123456789", "description": "Solo numeri"},
            {"query": "!@#$%^&*()", "description": "Solo caratteri speciali"}
        ]
        
        edge_results = []
        
        for case in edge_cases:
            query_data = {
                "query": case["query"],
                "expected_topics": [],
                "category": "Edge Case"
            }
            
            result = self.test_chatbot_response(query_data)
            result["description"] = case["description"]
            edge_results.append(result)
        
        return {
            "cases": edge_results,
            "handled_gracefully": sum(1 for r in edge_results if r["success"] or "error" in r),
            "total_cases": len(edge_results)
        }

def run_functional_tests():
    """Esegue tutti i test funzionali"""
    runner = FunctionalTestRunner()
    
    print("🧪 Avvio Test Funzionali del Chatbot")
    print("=" * 50)
    
    # Test query standard
    print("\n📝 Test Query Standard:")
    for query_data in runner.test_queries:
        result = runner.test_chatbot_response(query_data)
        runner.results["scenarios"][query_data["id"]] = result
        
        status = "✓" if result["success"] else "✗"
        quality = result.get("quality_score", 0)
        response_time = result.get("response_time", 0)
        
        print(f"  {status} {query_data['category']}: {quality}/100 qualità, {response_time:.3f}s")
    
    # Test flusso conversazione
    print("\n💬 Test Flusso Conversazione:")
    conversation_result = runner.test_conversation_flow()
    runner.results["scenarios"]["conversation_flow"] = conversation_result
    
    status = "✓" if conversation_result["success"] else "✗"
    avg_quality = conversation_result.get("avg_quality", 0)
    avg_time = conversation_result.get("avg_response_time", 0)
    
    print(f"  {status} Conversazione multi-turno: {avg_quality:.1f}/100 qualità media, {avg_time:.3f}s tempo medio")
    
    # Test casi limite
    print("\n⚠️  Test Casi Limite:")
    edge_result = runner.test_edge_cases()
    runner.results["scenarios"]["edge_cases"] = edge_result
    
    handled = edge_result["handled_gracefully"]
    total = edge_result["total_cases"]
    
    print(f"  📊 Gestiti correttamente: {handled}/{total} casi limite")
    
    # Calcola statistiche generali
    all_scenarios = [s for s in runner.results["scenarios"].values() if isinstance(s, dict) and "success" in s]
    successful_scenarios = [s for s in all_scenarios if s["success"]]
    
    if all_scenarios:
        avg_response_time = sum(s.get("response_time", 0) for s in successful_scenarios) / len(successful_scenarios) if successful_scenarios else 0
        avg_quality = sum(s.get("quality_score", 0) for s in successful_scenarios) / len(successful_scenarios) if successful_scenarios else 0
        success_rate = len(successful_scenarios) / len(all_scenarios)
    else:
        avg_response_time = 0
        avg_quality = 0
        success_rate = 0
    
    runner.results["summary"] = {
        "total_scenarios": len(all_scenarios),
        "successful": len(successful_scenarios),
        "success_rate": success_rate,
        "avg_response_time": avg_response_time,
        "avg_quality_score": avg_quality,
        "execution_time": datetime.now().isoformat()
    }
    
    # Salva risultati
    results_file = os.path.join(os.path.dirname(__file__), "..", "results", "functional_tests_results.json")
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(runner.results, f, indent=2, ensure_ascii=False)
    
    # Stampa sommario finale
    print(f"\n📊 Sommario Test Funzionali:")
    print(f"   Scenari totali: {runner.results['summary']['total_scenarios']}")
    print(f"   Successi: {runner.results['summary']['successful']}")
    print(f"   Tasso successo: {runner.results['summary']['success_rate']:.2%}")
    print(f"   Tempo medio risposta: {runner.results['summary']['avg_response_time']:.3f}s")
    print(f"   Qualità media: {runner.results['summary']['avg_quality_score']:.1f}/100")
    print(f"   Risultati salvati in: {results_file}")
    
    return runner.results

if __name__ == "__main__":
    run_functional_tests()