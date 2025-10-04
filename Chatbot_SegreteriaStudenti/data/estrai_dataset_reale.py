"""
Estrae dataset REALE di domande e risposte dai file FAQ per metriche RAG affidabili
Questo script legge i file FAQ originali e crea un dataset ground truth verificato
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict

def parse_faq_file(file_path: str) -> List[Dict[str, str]]:
    """
    Estrae coppie domanda-risposta da un file FAQ
    Formato file FAQ: domanda seguita da risposta, separate da newline
    """
    qa_pairs = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split su pattern domanda (termina con ?)
    # Ogni sezione è: domanda\nrisposta\n\n
    sections = re.split(r'\n(?=[A-Z].*\?)', content)
    
    current_question = None
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        lines = section.split('\n', 1)
        
        if len(lines) == 2:
            question = lines[0].strip()
            answer = lines[1].strip()
            
            # Verifica che sia una domanda valida (contiene ?)
            if '?' in question and answer:
                qa_pairs.append({
                    'question': question,
                    'answer': answer,
                    'source_file': os.path.basename(file_path)
                })
        elif len(lines) == 1 and '?' in lines[0]:
            # Domanda senza risposta esplicita (da skippare)
            continue
    
    return qa_pairs


def extract_all_faq_pairs(faq_dir: str) -> Dict[str, List[Dict[str, str]]]:
    """Estrae tutte le coppie Q&A da tutti i file FAQ, organizzate per categoria"""
    
    faq_path = Path(faq_dir)
    
    # Mapping file -> categoria
    file_categories = {
        'iscrizioni_anno_accademico.txt': 'iscrizioni',
        'tasse.txt': 'tasse',
        'lezioni_esami.txt': 'esami_lezioni',
        'lauree.txt': 'laurea',
        'richiesta_attestati_documenti.txt': 'certificati',
        'servizio_disabilità_dsa.txt': 'servizi_dsa',
        'servizio_diritto_studio.txt': 'servizi_diritto_studio',
        'servizio_orientamento.txt': 'servizi_orientamento',
        'carriera.txt': 'carriera',
        'tessera_universitaria.txt': 'tessera',
        'tirocini.txt': 'tirocini',
        'corsi_singoli.txt': 'corsi_singoli',
        'contatti_utili_problematiche_varie.txt': 'contatti',
        'varie.txt': 'varie',
        'sito_web_unibg.txt': 'sito_web'
    }
    
    all_pairs_by_category = {}
    all_pairs_flat = []
    
    print("="*80)
    print("ESTRAZIONE DATASET REALE DA FAQ")
    print("="*80)
    
    for filename, category in file_categories.items():
        file_path = faq_path / filename
        
        if not file_path.exists():
            print(f"⚠️  File non trovato: {filename}")
            continue
        
        print(f"\n📄 Processando: {filename}")
        
        pairs = parse_faq_file(str(file_path))
        
        if pairs:
            # Aggiungi categoria a ogni coppia
            for pair in pairs:
                pair['category'] = category
            
            all_pairs_by_category[category] = pairs
            all_pairs_flat.extend(pairs)
            
            print(f"   ✅ Estratte {len(pairs)} coppie Q&A")
            
            # Mostra prima domanda come esempio
            if pairs:
                print(f"   Esempio: {pairs[0]['question'][:70]}...")
        else:
            print(f"   ⚠️  Nessuna coppia estratta")
    
    print(f"\n{'='*80}")
    print(f"TOTALE: {len(all_pairs_flat)} coppie Q&A estratte da {len(all_pairs_by_category)} categorie")
    print('='*80)
    
    return all_pairs_by_category, all_pairs_flat


def select_evaluation_dataset(all_pairs: List[Dict[str, str]], 
                              num_samples: int = 25) -> List[Dict[str, str]]:
    """
    Seleziona un subset bilanciato per evaluation
    Cerca di prendere samples da diverse categorie
    """
    
    # Raggruppa per categoria
    by_category = {}
    for pair in all_pairs:
        cat = pair.get('category', 'unknown')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(pair)
    
    # Calcola quanti samples per categoria (bilanciato)
    samples_per_category = num_samples // len(by_category)
    remaining = num_samples % len(by_category)
    
    evaluation_set = []
    
    print(f"\n📊 Selezione {num_samples} samples bilanciati per evaluation:")
    
    for i, (category, pairs) in enumerate(sorted(by_category.items())):
        # Prendi n samples per categoria
        n_to_take = samples_per_category
        if i < remaining:  # Distribuisci il resto
            n_to_take += 1
        
        n_to_take = min(n_to_take, len(pairs))
        selected = pairs[:n_to_take]
        evaluation_set.extend(selected)
        
        print(f"   {category:25s}: {n_to_take:2d} samples (disponibili: {len(pairs)})")
    
    return evaluation_set


def create_rag_evaluation_dataset(faq_dir: str, 
                                  output_file: str,
                                  num_evaluation_samples: int = 25):
    """
    Crea dataset completo per evaluation RAG
    """
    
    # Estrai tutte le coppie
    by_category, all_pairs = extract_all_faq_pairs(faq_dir)
    
    if not all_pairs:
        print("❌ Nessuna coppia Q&A estratta!")
        return None
    
    # Seleziona subset per evaluation
    evaluation_set = select_evaluation_dataset(all_pairs, num_evaluation_samples)
    
    # Prepara dataset finale in formato compatibile con metriche RAG
    dataset = {
        'metadata': {
            'source': 'FAQ UniBG - Dataset Reale',
            'extraction_date': '2025-10-04',
            'total_pairs': len(all_pairs),
            'evaluation_pairs': len(evaluation_set),
            'categories': list(by_category.keys()),
            'description': 'Dataset estratto dai file FAQ ufficiali della Segreteria Studenti UniBG'
        },
        'evaluation_set': [],
        'full_dataset': []
    }
    
    # Formato per evaluation (compatibile con metriche RAG)
    for pair in evaluation_set:
        dataset['evaluation_set'].append({
            'query': pair['question'],
            'reference_answer': pair['answer'],
            'category': pair['category'],
            'source_file': pair['source_file'],
            'relevant_docs': [pair['source_file']]  # Il file da cui proviene
        })
    
    # Dataset completo (per futuri usi)
    for pair in all_pairs:
        dataset['full_dataset'].append({
            'query': pair['question'],
            'reference_answer': pair['answer'],
            'category': pair['category'],
            'source_file': pair['source_file']
        })
    
    # Salva
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"✅ DATASET SALVATO: {output_path}")
    print(f"{'='*80}")
    print(f"📊 Statistiche:")
    print(f"   - Coppie totali: {len(all_pairs)}")
    print(f"   - Coppie evaluation: {len(evaluation_set)}")
    print(f"   - Categorie: {len(by_category)}")
    print(f"\n💡 Questo dataset contiene SOLO domande e risposte REALI")
    print(f"   estratte dai documenti ufficiali della Segreteria Studenti.")
    print(f"   È scientificamente valido per calcolare metriche RAG.")
    print('='*80)
    
    return dataset


def print_dataset_samples(dataset: Dict, num_samples: int = 3):
    """Stampa alcuni esempi dal dataset"""
    
    print(f"\n{'='*80}")
    print(f"ESEMPI DAL DATASET ({num_samples} campioni)")
    print('='*80)
    
    for i, item in enumerate(dataset['evaluation_set'][:num_samples], 1):
        print(f"\n[Esempio {i}]")
        print(f"Categoria: {item['category']}")
        print(f"Fonte: {item['source_file']}")
        print(f"\nDomanda:")
        print(f"  {item['query']}")
        print(f"\nRisposta Reference:")
        print(f"  {item['reference_answer'][:300]}...")
        print("-" * 80)


if __name__ == "__main__":
    # Percorsi
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    faq_directory = project_root / 'data' / 'FAQ'
    output_file = project_root / 'data' / 'dataset_rag_reale.json'
    
    print("\n🚀 Avvio estrazione dataset REALE per evaluation RAG")
    print(f"📁 Directory FAQ: {faq_directory}")
    print(f"💾 Output file: {output_file}\n")
    
    # Crea dataset
    dataset = create_rag_evaluation_dataset(
        faq_dir=str(faq_directory),
        output_file=str(output_file),
        num_evaluation_samples=25
    )
    
    if dataset:
        # Mostra esempi
        print_dataset_samples(dataset, num_samples=5)
        
        print(f"\n✅ OPERAZIONE COMPLETATA!")

