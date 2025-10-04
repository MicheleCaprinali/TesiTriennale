"""
Calcola metriche RAG usando il dataset REALE estratto dai FAQ
"""

import sys
import os
import json
import time
import statistics
from pathlib import Path
from typing import Dict, List, Any

# Setup paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# metriche_qualita.py è obsoleto (dati inventati) - usa solo metriche base reali
METRICS_AVAILABLE = False


def evaluate_with_real_dataset(dataset_path: str, 
                               num_samples: int = None,
                               save_results: bool = True):
    """
    Valuta il chatbot usando il dataset REALE estratto dai FAQ
    """
    
    print("="*80)
    print("VALUTAZIONE RAG CON DATASET REALE")
    print("="*80)
    print(f"\n📁 Caricamento dataset: {dataset_path}\n")
    
    # Carica dataset reale
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    evaluation_set = dataset['evaluation_set']
    
    if num_samples:
        evaluation_set = evaluation_set[:num_samples]
    
    print(f"📊 Dataset info:")
    print(f"   - Fonte: {dataset['metadata']['source']}")
    print(f"   - Coppie totali disponibili: {dataset['metadata']['total_pairs']}")
    print(f"   - Coppie da valutare: {len(evaluation_set)}")
    print(f"   - Categorie: {', '.join(dataset['metadata']['categories'])}")
    
    # Cambia directory alla root del progetto (dove si trova vectordb/)
    original_dir = os.getcwd()
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"\n📂 Directory di lavoro: {os.getcwd()}")
    
    # Inizializza chatbot
    print(f"🤖 Inizializzazione chatbot...")
    try:
        from main import ChatbotRAG
        chatbot = ChatbotRAG()
        print("✅ Chatbot pronto\n")
    except Exception as e:
        print(f"❌ Errore inizializzazione chatbot: {e}")
        os.chdir(original_dir)  # Ripristina directory originale
        return None
    
    # Usa solo metriche base (dataset reale)
    quality_eval = None
    rag_eval = None
    print("📊 Calcolo metriche base con dati reali\n")
    
    # Risultati
    results = {
        'metadata': {
            'evaluation_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'dataset_source': dataset['metadata']['source'],
            'num_evaluated': len(evaluation_set),
            'metrics_full': METRICS_AVAILABLE
        },
        'individual_results': [],
        'aggregate_metrics': {}
    }
    
    # Valuta ogni query
    print(f"{'='*80}")
    print(f"VALUTAZIONE IN CORSO")
    print(f"{'='*80}\n")
    
    all_quality_scores = []
    all_rag_scores = []
    all_response_times = []
    all_bleu_scores = []
    all_rouge_scores = []
    all_bert_scores = []
    
    for i, item in enumerate(evaluation_set, 1):
        query = item['query']
        reference = item['reference_answer']
        category = item['category']
        
        print(f"[{i}/{len(evaluation_set)}] Categoria: {category}")
        print(f"Query: {query[:70]}...")
        
        start_time = time.time()
        
        try:
            # Recupera documenti
            retrieved_docs = chatbot.retrieve_documents(query, k=5)
            retrieved_content = [doc['content'] for doc in retrieved_docs] if retrieved_docs else []
            
            # Genera risposta
            response_dict = chatbot.chat(query)
            generated_response = response_dict['response']
            
            response_time = time.time() - start_time
            all_response_times.append(response_time)
            
            print(f"  ⏱️  Tempo: {response_time:.1f}s")
            print(f"  📝 Risposta: {generated_response[:100]}...")
            
            # Calcola metriche se disponibili
            if METRICS_AVAILABLE and quality_eval and rag_eval:
                # Metriche qualità
                quality_metrics = quality_eval.evaluate_response(
                    query,
                    generated_response,
                    reference
                )
                
                # Metriche RAG
                rag_metrics = rag_eval.evaluate_rag_system(
                    query=query,
                    generated_response=generated_response,
                    reference_response=reference,
                    retrieved_documents=retrieved_content,
                    relevant_documents=[item['source_file']]
                )
                
                all_quality_scores.append(quality_metrics['overall_score'])
                all_rag_scores.append(rag_metrics['rag_overall_score'])
                
                if 'bleu_score' in rag_metrics:
                    all_bleu_scores.append(rag_metrics['bleu_score'])
                if 'rouge_l' in rag_metrics:
                    all_rouge_scores.append(rag_metrics['rouge_l'])
                if 'bert_score' in rag_metrics:
                    all_bert_scores.append(rag_metrics['bert_score'])
                
                print(f"  📊 Quality Score: {quality_metrics['overall_score']:.3f}")
                print(f"  📊 RAG Score: {rag_metrics['rag_overall_score']:.3f}")
                
                result = {
                    'query': query,
                    'category': category,
                    'reference_answer': reference,
                    'generated_answer': generated_response,
                    'response_time': response_time,
                    'quality_metrics': quality_metrics,
                    'rag_metrics': rag_metrics
                }
            else:
                # Solo metriche base
                result = {
                    'query': query,
                    'category': category,
                    'reference_answer': reference,
                    'generated_answer': generated_response,
                    'response_time': response_time,
                    'response_length': len(generated_response),
                    'reference_length': len(reference)
                }
                
                print(f"  ℹ️  Lunghezza risposta: {len(generated_response)} char")
            
            results['individual_results'].append(result)
            print()
            
        except Exception as e:
            print(f"  ❌ Errore: {e}\n")
            continue
    
    # Calcola metriche aggregate
    print(f"\n{'='*80}")
    print(f"METRICHE AGGREGATE")
    print(f"{'='*80}\n")
    
    results['aggregate_metrics'] = {
        'num_successful': len(results['individual_results']),
        'num_failed': len(evaluation_set) - len(results['individual_results']),
        'success_rate': (len(results['individual_results']) / len(evaluation_set)) * 100
    }
    
    if all_response_times:
        results['aggregate_metrics']['response_times'] = {
            'mean': statistics.mean(all_response_times),
            'median': statistics.median(all_response_times),
            'min': min(all_response_times),
            'max': max(all_response_times),
            'std': statistics.stdev(all_response_times) if len(all_response_times) > 1 else 0
        }
        
        print(f"⏱️  Tempi di Risposta:")
        print(f"   Media: {results['aggregate_metrics']['response_times']['mean']:.1f}s")
        print(f"   Mediana: {results['aggregate_metrics']['response_times']['median']:.1f}s")
        print(f"   Range: {results['aggregate_metrics']['response_times']['min']:.1f}s - {results['aggregate_metrics']['response_times']['max']:.1f}s")
    
    if all_quality_scores:
        results['aggregate_metrics']['quality_scores'] = {
            'mean': statistics.mean(all_quality_scores),
            'median': statistics.median(all_quality_scores),
            'min': min(all_quality_scores),
            'max': max(all_quality_scores),
            'std': statistics.stdev(all_quality_scores) if len(all_quality_scores) > 1 else 0
        }
        
        print(f"\n📊 Quality Scores:")
        print(f"   Media: {results['aggregate_metrics']['quality_scores']['mean']:.3f}")
        print(f"   Mediana: {results['aggregate_metrics']['quality_scores']['median']:.3f}")
    
    if all_rag_scores:
        results['aggregate_metrics']['rag_scores'] = {
            'mean': statistics.mean(all_rag_scores),
            'median': statistics.median(all_rag_scores),
            'min': min(all_rag_scores),
            'max': max(all_rag_scores),
            'std': statistics.stdev(all_rag_scores) if len(all_rag_scores) > 1 else 0
        }
        
        print(f"\n📊 RAG Scores:")
        print(f"   Media: {results['aggregate_metrics']['rag_scores']['mean']:.3f}")
        print(f"   Mediana: {results['aggregate_metrics']['rag_scores']['median']:.3f}")
    
    if all_bleu_scores:
        results['aggregate_metrics']['bleu_score'] = {
            'mean': statistics.mean(all_bleu_scores),
            'std': statistics.stdev(all_bleu_scores) if len(all_bleu_scores) > 1 else 0
        }
        print(f"\n📈 BLEU Score: {results['aggregate_metrics']['bleu_score']['mean']:.3f}")
    
    if all_rouge_scores:
        results['aggregate_metrics']['rouge_l'] = {
            'mean': statistics.mean(all_rouge_scores),
            'std': statistics.stdev(all_rouge_scores) if len(all_rouge_scores) > 1 else 0
        }
        print(f"📈 ROUGE-L: {results['aggregate_metrics']['rouge_l']['mean']:.3f}")
    
    if all_bert_scores:
        results['aggregate_metrics']['bert_score'] = {
            'mean': statistics.mean(all_bert_scores),
            'std': statistics.stdev(all_bert_scores) if len(all_bert_scores) > 1 else 0
        }
        print(f"📈 BERT Score: {results['aggregate_metrics']['bert_score']['mean']:.3f}")
    
    # Salva risultati
    if save_results:
        output_dir = Path(__file__).parent.parent / 'results'
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / 'metriche_rag_dataset_reale.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"💾 Risultati salvati: {output_file}")
        print(f"{'='*80}")
    
    # Ripristina directory originale
    if 'original_dir' in locals():
        os.chdir(original_dir)
    
    return results


if __name__ == "__main__":
    print("\n🚀 VALUTAZIONE RAG CON DATASET REALE")
    print("="*80)
    print("Questo script usa SOLO domande e risposte REALI estratte dai FAQ.")
    print("Le metriche calcolate sono scientificamente VALIDE per la tesi.")
    print("="*80 + "\n")
    
    # Percorsi
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    dataset_file = project_root / 'data' / 'dataset_rag_reale.json'
    
    if not dataset_file.exists():
        print(f"❌ Dataset non trovato: {dataset_file}")
        print(f"\n📝 Esegui prima:")
        print(f"   python data/estrai_dataset_reale.py")
        sys.exit(1)
    
    try:
        # Chiedi quanti samples valutare
        print(f"Il dataset contiene 25 coppie Q&A per evaluation.\n")
        choice = input("Quanti samples vuoi valutare? (1-25, ENTER per tutti): ").strip()
        
        num_samples = None
        if choice:
            try:
                num_samples = int(choice)
                if num_samples < 1 or num_samples > 25:
                    print("⚠️  Valore non valido, uso tutti i 25 samples")
                    num_samples = None
            except:
                print("⚠️  Input non valido, uso tutti i 25 samples")
        
        print(f"\n⏳ Avvio valutazione (può richiedere 10-30 minuti)...\n")
        
        # Esegui valutazione
        results = evaluate_with_real_dataset(
            dataset_path=str(dataset_file),
            num_samples=num_samples,
            save_results=True
        )
        
        if results:
            print(f"\n✅ VALUTAZIONE COMPLETATA!")
            print(f"\n🎯 Risultati finali:")
            print(f"   - Valutazioni riuscite: {results['aggregate_metrics']['num_successful']}")
            print(f"   - Success rate: {results['aggregate_metrics']['success_rate']:.1f}%")
            
            if 'response_times' in results['aggregate_metrics']:
                print(f"   - Tempo medio: {results['aggregate_metrics']['response_times']['mean']:.1f}s")
            
            if 'rag_scores' in results['aggregate_metrics']:
                print(f"   - RAG Score medio: {results['aggregate_metrics']['rag_scores']['mean']:.3f}")
            
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Valutazione interrotta dall'utente")
    except Exception as e:
        print(f"\n\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
