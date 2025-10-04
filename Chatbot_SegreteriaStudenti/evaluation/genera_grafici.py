"""
Generazione grafici per tesi - Sistema ChatBot RAG UniBg

✅ AGGIORNATO: Usa metriche RAG calcolate su DATASET REALE
   File: results/metriche_rag_dataset_reale.json
   Dataset: 68 coppie Q&A estratte da FAQ UniBG
   
Genera 3 grafici principali:
1. Distribuzione complessità ciclomatica
2. WMC e LCOM per classi
3. Metriche RAG (BLEU, ROUGE, BERT, Recall@K) con dati REALI
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd

def genera_grafici_tesi():

    results_dir = Path("../results")
    if not results_dir.exists():
        print("Cartella results non trovata. Esegui prima le analisi delle metriche.")
        return
    
    print("Generazione grafici per tesi...")
    
    # Configura stile grafici professionale
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Genera solo i 3 grafici richiesti per la tesi
    _grafico_complessita_ciclomatica(results_dir)
    _grafico_wmc_lcom(results_dir)
    _grafico_metriche_rag(results_dir)
    
    print("Grafici salvati nella cartella results/")

def _grafico_complessita_ciclomatica(results_dir):
    """Grafico a torta distribuzione complessità ciclomatica"""
    
    file_path = results_dir / 'metriche_software_results.json'
    if not file_path.exists():
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    distribution = data['complexity_analysis']['distribution']
    
    # Dati per grafico a torta
    labels = ['Bassa (1-5)', 'Media (6-10)', 'Alta (11-15)', 'Molto Alta (16+)']
    sizes = [
        distribution.get('bassa_1_5', 0),
        distribution.get('media_6_10', 0), 
        distribution.get('alta_11_15', 0),
        distribution.get('molto_alta_16+', 0)
    ]
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
    
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Distribuzione Complessità Ciclomatica\nSistema ChatBot RAG UniBg\n(main.py, src/, interfaccia/streamlit.py)', fontsize=16, pad=20)
    plt.axis('equal')
    
    plt.tight_layout()
    plt.savefig(results_dir / 'complessita_ciclomatica_distribuzione.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Grafico complessità ciclomatica salvato")

def _grafico_wmc_lcom(results_dir):
    """Grafici a barre WMC e LCOM per classi"""
    
    file_path = results_dir / 'metriche_avanzate_results.json'
    if not file_path.exists():
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metrics = data['metrics']
    classi = metrics['dettagli_classi']
    
    if not classi:
        return
    
    # Estrae dati per grafici
    nomi_classi = [c['nome_classe'] for c in classi]
    wmc_scores = [c['wmc'] for c in classi]
    lcom_scores = [c['lcom'] for c in classi]
    
    # Crea subplot con due grafici affiancati
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar(range(len(nomi_classi)), wmc_scores, color='#3498db')
    plt.title('WMC (Weighted Methods per Class)', fontsize=14)
    plt.xlabel('Classi')
    plt.ylabel('Score WMC')
    plt.xticks(range(len(nomi_classi)), nomi_classi, rotation=45, ha='right')
    
    plt.subplot(1, 2, 2)
    plt.bar(range(len(nomi_classi)), lcom_scores, color='#e74c3c')
    plt.title('LCOM (Lack of Cohesion of Methods)', fontsize=14)
    plt.xlabel('Classi')
    plt.ylabel('Score LCOM (%)')
    plt.xticks(range(len(nomi_classi)), nomi_classi, rotation=45, ha='right')
    
    plt.suptitle('Metriche WMC e LCOM - Sistema ChatBot RAG UniBg\n(Analisi Completa: main.py, src/, interfaccia/)', fontsize=16)
    plt.tight_layout()
    plt.savefig(results_dir / 'wmc_lcom_analisi.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Grafico WMC e LCOM salvato")


def _grafico_metriche_rag(results_dir):
    """Grafico metriche specifiche sistema RAG (USA DATASET REALE)"""
    
    # ✅ USA IL NUOVO FILE CON DATI REALI
    file_path = results_dir / 'metriche_rag_dataset_reale.json'
    if not file_path.exists():
        print("⚠️  File metriche RAG reali non trovato")
        print("   Esegui: python evaluation/valuta_con_dataset_reale.py")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # ✅ Estrai metriche aggregate dal nuovo formato
    metrics_summary = data.get('aggregate_metrics', {})
    individual_results = data.get('individual_results', [])
    
    # Calcola medie per metriche non aggregate
    answer_relevance_mean = sum(r['rag_metrics'].get('answer_relevance', 0) for r in individual_results) / len(individual_results) if individual_results else 0
    context_precision_mean = sum(r['rag_metrics'].get('context_precision', 0) for r in individual_results) / len(individual_results) if individual_results else 0
    faithfulness_mean = sum(r['rag_metrics'].get('faithfulness', 0) for r in individual_results) / len(individual_results) if individual_results else 0
    recall_at_1_mean = sum(r['rag_metrics'].get('recall_at_1', 0) for r in individual_results) / len(individual_results) if individual_results else 0
    recall_at_3_mean = sum(r['rag_metrics'].get('recall_at_3', 0) for r in individual_results) / len(individual_results) if individual_results else 0
    recall_at_5_mean = sum(r['rag_metrics'].get('recall_at_5', 0) for r in individual_results) / len(individual_results) if individual_results else 0
    
    # Grafico radar delle metriche RAG principali
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Metriche linguistiche (BLEU, ROUGE-L, BERT)
    linguistic_metrics = ['BLEU', 'ROUGE-L', 'BERT Score']
    linguistic_values = [
        metrics_summary.get('bleu_score', {}).get('mean', 0),
        metrics_summary.get('rouge_l', {}).get('mean', 0),
        metrics_summary.get('bert_score', {}).get('mean', 0)
    ]
    
    bars1 = ax1.bar(linguistic_metrics, linguistic_values, color=['#3498db', '#2ecc71', '#9b59b6'])
    ax1.set_title('Metriche Qualità Linguistica', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Score (0-1)')
    ax1.set_ylim(0, 1)
    
    # Aggiungi valori sopra le barre
    for bar, value in zip(bars1, linguistic_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{value:.3f}', ha='center', va='bottom')
    
    # 2. Metriche RAG specifiche (Rilevanza, Precisione, Fedeltà)
    rag_metrics = ['Answer\nRelevance', 'Context\nPrecision', 'Faithfulness']
    rag_values = [
        answer_relevance_mean,
        context_precision_mean,
        faithfulness_mean
    ]
    
    bars2 = ax2.bar(rag_metrics, rag_values, color=['#f39c12', '#1abc9c', '#e74c3c'])
    ax2.set_title('Metriche Sistema RAG', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Score (0-1)')
    ax2.set_ylim(0, 1)
    
    for bar, value in zip(bars2, rag_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{value:.3f}', ha='center', va='bottom')
    
    # 3. Recall@K
    k_values = ['Recall@1', 'Recall@3', 'Recall@5']
    recall_values = [recall_at_1_mean, recall_at_3_mean, recall_at_5_mean]
    
    bars3 = ax3.bar(k_values, recall_values, color=['#ff7675', '#fd79a8', '#fdcb6e'])
    ax3.set_title('Metriche Recall@K', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Recall Score (0-1)')
    ax3.set_ylim(0, 1)
    
    for bar, value in zip(bars3, recall_values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{value:.3f}', ha='center', va='bottom')
    
    # 4. Score complessivo RAG
    overall_rag = sum(r['rag_metrics'].get('rag_overall_score', 0) for r in individual_results) / len(individual_results) if individual_results else 0
    
    # Grafico gauge semplificato
    ax4.pie([overall_rag, 1-overall_rag], 
           colors=['#00b894', '#ddd'], 
           startangle=90, 
           counterclock=False,
           wedgeprops=dict(width=0.3))
    
    ax4.text(0, 0, f'{overall_rag:.3f}', ha='center', va='center', 
            fontsize=20, fontweight='bold')
    ax4.set_title('Score RAG Complessivo', fontsize=12, fontweight='bold')
    
    # ✅ TITOLO AGGIORNATO: indica dataset reale
    plt.suptitle('Valutazione Sistema RAG - ChatBot UniBg\n(Dataset Reale: 25 Q&A da FAQ UniBG)', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(results_dir / 'metriche_rag_valutazione.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Grafico metriche RAG salvato (basato su dataset REALE)")


if __name__ == "__main__":
    try:
        genera_grafici_tesi()
        print("\nTutti i grafici generati con successo!")
    except ImportError as e:
        print(f"Dipendenze mancanti: {e}")
        print("Installa con: pip install matplotlib seaborn pandas")
    except Exception as e:
        print(f"Errore generazione grafici: {e}")