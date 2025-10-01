"""
Generatore grafici PNG dai risultati JSON per tesi
Trasforma dati metriche in visualizzazioni professionali
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd

def genera_grafici_tesi():
    """Genera grafici PNG dai file JSON per inserimento in tesi"""
    
    results_dir = Path("../results")
    if not results_dir.exists():
        print("Cartella results non trovata. Esegui prima le analisi delle metriche.")
        return
    
    print("Generazione grafici per tesi...")
    
    # Configura stile grafici professionale
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Genera tutti i grafici
    _grafico_complessita_ciclomatica(results_dir)
    _grafico_wmc_lcom(results_dir)
    _grafico_metriche_software(results_dir)
    _grafico_metriche_rag(results_dir)
    _grafico_qualita_vs_rag(results_dir)
    
    print("Grafici salvati nella cartella results/")
    print("Grafici generati:")
    print("  • complessita_ciclomatica_distribuzione.png")
    print("  • wmc_lcom_analisi.png") 
    print("  • metriche_software_panoramica.png")
    print("  • metriche_rag_valutazione.png (se dati RAG disponibili)")
    print("  • confronto_qualita_rag.png (se dati disponibili)")

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
    
    print("Grafici WMC e LCOM salvati")

def _grafico_metriche_software(results_dir):
    """Grafico panoramico composizione e struttura progetto"""
    
    file_path = results_dir / 'metriche_software_results.json'
    if not file_path.exists():
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    summary = data['summary']
    
    # Grafico composizione righe di codice
    labels = ['Righe Codice', 'Righe Commenti', 'Righe Vuote']
    sizes = [
        data['detailed_metrics']['code_lines'],
        data['detailed_metrics']['comment_lines'],
        data['detailed_metrics']['blank_lines']
    ]
    colors = ['#3498db', '#2ecc71', '#95a5a6']
    
    plt.figure(figsize=(14, 6))
    
    # Grafico composizione (torta)
    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Composizione Linee di Codice', fontsize=14)
    
    # Grafico elementi strutturali (barre)
    plt.subplot(1, 2, 2)
    elementi = ['File Python', 'Funzioni', 'Classi']
    valori = [summary['total_files'], summary['total_functions'], summary['total_classes']]
    plt.bar(elementi, valori, color=['#9b59b6', '#f39c12', '#1abc9c'])
    plt.title('Elementi Strutturali Progetto', fontsize=14)
    plt.ylabel('Conteggio')
    
    # Aggiungi valori sopra le barre
    for i, v in enumerate(valori):
        plt.text(i, v + max(valori)*0.01, str(v), ha='center', va='bottom')
    
    plt.suptitle('Panoramica Metriche Software - ChatBot RAG UniBg\n(Analisi Completa Sistema)', fontsize=16)
    plt.tight_layout()
    plt.savefig(results_dir / 'metriche_software_panoramica.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Grafico panoramica metriche salvato")


def _grafico_metriche_rag(results_dir):
    """Grafico metriche specifiche sistema RAG"""
    
    file_path = results_dir / 'metriche_rag_results.json'
    if not file_path.exists():
        print("File metriche RAG non trovato - eseguire prima valutazione RAG")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metrics_summary = data.get('metrics_summary', {})
    
    # Grafico radar delle metriche RAG principali
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Metriche linguistiche (BLEU, ROUGE-L, BERT)
    linguistic_metrics = ['BLEU', 'ROUGE-L', 'BERT Score']
    linguistic_values = [
        metrics_summary.get('bleu_score', 0),
        metrics_summary.get('rouge_l', 0),
        metrics_summary.get('bert_score', 0)
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
        metrics_summary.get('answer_relevance', 0),
        metrics_summary.get('context_precision', 0),
        metrics_summary.get('faithfulness', 0)
    ]
    
    bars2 = ax2.bar(rag_metrics, rag_values, color=['#f39c12', '#1abc9c', '#e74c3c'])
    ax2.set_title('Metriche Sistema RAG', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Score (0-1)')
    ax2.set_ylim(0, 1)
    
    for bar, value in zip(bars2, rag_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{value:.3f}', ha='center', va='bottom')
    
    # 3. Recall@K se disponibile
    recall_metrics = metrics_summary.get('recall_metrics', {})
    if recall_metrics:
        k_values = []
        recall_values = []
        for key, value in recall_metrics.items():
            if key.startswith('recall_at_'):
                k = key.replace('recall_at_', '')
                k_values.append(f'Recall@{k}')
                recall_values.append(value)
        
        if k_values:
            bars3 = ax3.bar(k_values, recall_values, color=['#ff7675', '#fd79a8', '#fdcb6e'])
            ax3.set_title('Metriche Recall@K', fontsize=12, fontweight='bold')
            ax3.set_ylabel('Recall Score (0-1)')
            ax3.set_ylim(0, 1)
            
            for bar, value in zip(bars3, recall_values):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                        f'{value:.3f}', ha='center', va='bottom')
        else:
            ax3.text(0.5, 0.5, 'Dati Recall@K\nnon disponibili', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Metriche Recall@K', fontsize=12, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'Dati Recall@K\nnon disponibili', 
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Metriche Recall@K', fontsize=12, fontweight='bold')
    
    # 4. Score complessivo RAG
    overall_rag = metrics_summary.get('overall_rag_score', 0)
    
    # Grafico gauge semplificato
    ax4.pie([overall_rag, 1-overall_rag], 
           colors=['#00b894', '#ddd'], 
           startangle=90, 
           counterclock=False,
           wedgeprops=dict(width=0.3))
    
    ax4.text(0, 0, f'{overall_rag:.3f}', ha='center', va='center', 
            fontsize=20, fontweight='bold')
    ax4.set_title('Score RAG Complessivo', fontsize=12, fontweight='bold')
    
    plt.suptitle('Valutazione Sistema RAG - ChatBot UniBg\n(BLEU, ROUGE-L, BERT Score, Recall@K)', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(results_dir / 'metriche_rag_valutazione.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Grafico metriche RAG salvato")


def _grafico_qualita_vs_rag(results_dir):
    """Confronto metriche qualità tradizionali vs RAG"""
    
    # Verifica presenza entrambi i file
    rag_path = results_dir / 'metriche_rag_results.json'
    quality_path = results_dir / 'metriche_qualita_results.json'
    
    if not rag_path.exists() and not quality_path.exists():
        print("File metriche qualità/RAG non trovati")
        return
    
    # Carica dati disponibili
    rag_data = {}
    quality_data = {}
    
    if rag_path.exists():
        with open(rag_path, 'r', encoding='utf-8') as f:
            rag_data = json.load(f)
    
    if quality_path.exists():
        with open(quality_path, 'r', encoding='utf-8') as f:
            quality_data = json.load(f)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Confronto score complessivi
    if rag_data and quality_data:
        rag_overall = rag_data.get('evaluation_data', {}).get('overall_rag_score', 0)
        quality_overall = quality_data.get('evaluation_result', {}).get('metrics', {}).get('overall_score', 0)
        
        scores = [quality_overall, rag_overall]
        labels = ['Qualità\nTradizionale', 'Sistema\nRAG']
        colors = ['#3498db', '#e74c3c']
        
        bars1 = ax1.bar(labels, scores, color=colors)
        ax1.set_title('Confronto Score Complessivi', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Score (0-1)')
        ax1.set_ylim(0, 1)
        
        for bar, score in zip(bars1, scores):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                    f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
    else:
        ax1.text(0.5, 0.5, 'Dati confronto\nnon disponibili', 
                ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Confronto Score Complessivi', fontsize=12, fontweight='bold')
    
    # 2. Distribuzione metriche RAG principali
    if rag_data:
        metrics_summary = rag_data.get('metrics_summary', {})
        
        # Seleziona metriche chiave per il radar
        metric_names = ['BLEU', 'ROUGE-L', 'BERT Score', 'Answer\nRelevance', 'Faithfulness']
        metric_values = [
            metrics_summary.get('bleu_score', 0),
            metrics_summary.get('rouge_l', 0),
            metrics_summary.get('bert_score', 0),
            metrics_summary.get('answer_relevance', 0),
            metrics_summary.get('faithfulness', 0)
        ]
        
        # Grafico radar semplificato come grafico polare
        angles = [i * 2 * 3.14159 / len(metric_names) for i in range(len(metric_names))]
        angles += angles[:1]  # Chiudi il cerchio
        metric_values += metric_values[:1]
        
        ax2 = plt.subplot(122, projection='polar')
        ax2.plot(angles, metric_values, 'o-', linewidth=2, color='#e74c3c')
        ax2.fill(angles, metric_values, alpha=0.25, color='#e74c3c')
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(metric_names)
        ax2.set_ylim(0, 1)
        ax2.set_title('Profilo Metriche RAG', fontsize=12, fontweight='bold', pad=20)
        ax2.grid(True)
    else:
        ax2.text(0.5, 0.5, 'Dati RAG\nnon disponibili', 
                ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('Profilo Metriche RAG', fontsize=12, fontweight='bold')
    
    plt.suptitle('Analisi Comparativa Qualità vs RAG - ChatBot UniBg', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(results_dir / 'confronto_qualita_rag.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Grafico confronto qualità vs RAG salvato")

if __name__ == "__main__":
    try:
        genera_grafici_tesi()
        print("\nTutti i grafici PNG generati con successo!")
        print("Grafici pronti per inserimento in tesi LaTeX")
    except ImportError as e:
        print(f"Dipendenze mancanti: {e}")
        print("Installa con: pip install matplotlib seaborn pandas")
    except Exception as e:
        print(f"Errore generazione grafici: {e}")