# Crea file: test_iscrizioni_quick.py
"""Test rapido per categoria iscrizioni migliorata"""

import sys
sys.path.append('src')
sys.path.append('evaluation')

from ollama_llm import OllamaLLM
from metriche_qualità import evaluate_chatbot_response
from local_embeddings import LocalEmbeddings
from creazione_vectorstore import search_vectorstore

def test_iscrizioni_improvement():
    """Test miglioramento template iscrizioni"""
    
    print("🧪 TEST MIGLIORAMENTO TEMPLATE ISCRIZIONI")
    print("=" * 50)
    
    # Setup
    llm = OllamaLLM()
    embedder = LocalEmbeddings()
    
    question = "Come faccio a iscrivermi agli esami?"
    
    print(f"📝 Domanda: {question}")
    print("🔍 Cercando documenti rilevanti...")
    
    # Trova contesto
    try:
        docs = search_vectorstore(question, k=3, embedder=embedder)
        context = "\n".join(docs["documents"][0][:2]) if docs["documents"][0] else ""
        print(f"✅ Contesto trovato ({len(context)} caratteri)")
    except Exception as e:
        print(f"⚠️ Errore ricerca: {e}")
        context = ""
    
    print("\n🔧 Generando risposta con template ottimizzato...")
    
    # Genera risposta
    try:
        response = llm.generate(question, context)
        print(f"✅ Risposta generata ({len(response)} caratteri)")
    except Exception as e:
        print(f"❌ Errore generazione: {e}")
        return
    
    print(f"\n📝 RISPOSTA OTTENUTA:")
    print("-" * 30)
    print(response[:300] + "..." if len(response) > 300 else response)
    print("-" * 30)
    
    # Valuta qualità
    evaluation = evaluate_chatbot_response(question, response, context)
    metrics = evaluation['metrics']
    
    print(f"\n📊 METRICHE QUALITÀ:")
    print(f"   🎯 Score Complessivo: {metrics['overall_score']:.3f}")
    print(f"   🔍 Rilevanza: {metrics.get('semantic_similarity', 0):.3f}")
    print(f"   📋 Completezza: {metrics.get('completeness_score', 0):.3f}")
    print(f"   ✨ Chiarezza: {metrics.get('clarity_score', 0):.3f}")
    print(f"   🎓 Professionalità: {metrics.get('professional_tone', 0):.3f}")
    
    # Confronto con baseline
    baseline_score = 0.637  # Score precedente categoria iscrizioni
    current_score = metrics['overall_score']
    improvement = ((current_score - baseline_score) / baseline_score) * 100
    
    print(f"\n📈 RISULTATI:")
    print(f"   Score precedente: {baseline_score:.3f}")
    print(f"   Score attuale: {current_score:.3f}")
    if improvement > 0:
        print(f"   🚀 Miglioramento: +{improvement:.1f}%")
    else:
        print(f"   📉 Peggioramento: {improvement:.1f}%")
    
    # Controllo rilevanza semantica specifica
    rilevanza = metrics.get('semantic_similarity', 0)
    print(f"\n🎯 ANALISI RILEVANZA:")
    print(f"   Rilevanza precedente: ~0.506")
    print(f"   Rilevanza attuale: {rilevanza:.3f}")
    rilevanza_improvement = ((rilevanza - 0.506) / 0.506) * 100
    if rilevanza_improvement > 0:
        print(f"   ✅ Miglioramento rilevanza: +{rilevanza_improvement:.1f}%")
    else:
        print(f"   ⚠️ Rilevanza: {rilevanza_improvement:.1f}%")
    
    return current_score, rilevanza

if __name__ == "__main__":
    test_iscrizioni_improvement()