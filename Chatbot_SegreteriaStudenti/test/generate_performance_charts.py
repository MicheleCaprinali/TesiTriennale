#!/usr/bin/env python3
"""
Generatore di Grafici per Test Prestazionali - Tesi Triennale
Crea visualizzazioni dei risultati dei test per documentazione tesi
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import os

# Configurazione stile grafici
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

def load_test_results():
    """Carica i risultati dei test da file JSON"""
    results_path = Path("results/real_performance_results.json")
    
    if not results_path.exists():
        print(f"❌ File risultati non trovato: {results_path}")
        return None
    
    with open(results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Caricati risultati: {data['queries_total']} query")
    return data

def create_response_time_distribution(data):
    """Grafico distribuzione tempi di risposta"""
    times = data['response_times']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Istogramma
    ax1.hist(times, bins=15, alpha=0.7, color='skyblue', edgecolor='navy')
    ax1.axvline(np.mean(times), color='red', linestyle='--', 
                label=f'Media: {np.mean(times):.1f}s')
    ax1.axvline(np.median(times), color='orange', linestyle='--', 
                label=f'Mediana: {np.median(times):.1f}s')
    ax1.set_xlabel('Tempo di Risposta (secondi)')
    ax1.set_ylabel('Frequenza')
    ax1.set_title('Distribuzione Tempi di Risposta')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2.boxplot(times, patch_artist=True, 
                boxprops=dict(facecolor='lightblue', alpha=0.7))
    ax2.set_ylabel('Tempo di Risposta (secondi)')
    ax2.set_title('Box Plot Tempi di Risposta')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/response_time_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("📊 Generato: response_time_distribution.png")

def create_performance_overview(data):
    """Grafico panoramica performance"""
    perf = data['performance_data']
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Tasso di successo (gauge-like)
    success_rate = perf['success_rate']
    colors = ['red' if success_rate < 70 else 'orange' if success_rate < 90 else 'green']
    ax1.pie([success_rate, 100-success_rate], 
            labels=[f'Successo\n{success_rate:.1f}%', f'Fallite\n{100-success_rate:.1f}%'],
            colors=['lightgreen', 'lightcoral'], startangle=90,
            wedgeprops=dict(width=0.3))
    ax1.set_title('Tasso di Successo Query')
    
    # 2. Metriche temporali
    metrics = ['Media', 'Mediana', 'Min', 'Max']
    values = [perf['avg_response_time'], perf['median_response_time'],
              perf['min_response_time'], perf['max_response_time']]
    bars = ax2.bar(metrics, values, color=['skyblue', 'lightgreen', 'gold', 'salmon'])
    ax2.set_ylabel('Tempo (secondi)')
    ax2.set_title('Statistiche Tempi di Risposta')
    ax2.grid(True, alpha=0.3)
    
    # Aggiungi valori sopra le barre
    for bar, value in zip(bars, values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{value:.1f}s', ha='center', va='bottom')
    
    # 3. Performance nel tempo (simulato)
    query_nums = list(range(1, len(data['response_times']) + 1))
    ax3.plot(query_nums, data['response_times'], 'b-', alpha=0.7, linewidth=2)
    ax3.fill_between(query_nums, data['response_times'], alpha=0.3)
    ax3.set_xlabel('Numero Query')
    ax3.set_ylabel('Tempo di Risposta (s)')
    ax3.set_title('Performance nel Tempo')
    ax3.grid(True, alpha=0.3)
    
    # 4. Valutazione finale
    grade_colors = {'A': 'green', 'B': 'lightgreen', 'C': 'orange', 'D': 'red', 'F': 'darkred'}
    grade = perf['grade']
    ax4.text(0.5, 0.7, f"Valutazione\n{grade}", ha='center', va='center',
             fontsize=24, fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor=grade_colors[grade], alpha=0.7))
    ax4.text(0.5, 0.3, perf['recommendation'], ha='center', va='center',
             fontsize=12, wrap=True)
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Valutazione Complessiva')
    
    plt.tight_layout()
    plt.savefig('results/performance_overview.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("📊 Generato: performance_overview.png")

def create_comparison_chart(data):
    """Grafico comparativo con benchmark ideali"""
    perf = data['performance_data']
    
    # Benchmark di riferimento
    benchmarks = {
        'Sistema Attuale': {
            'tempo_medio': perf['avg_response_time'],
            'successo': perf['success_rate'],
            'qps': perf['queries_per_second']
        },
        'Target Produzione': {
            'tempo_medio': 3.0,
            'successo': 95.0,
            'qps': 0.33
        },
        'Sistema Ideale': {
            'tempo_medio': 1.0,
            'successo': 99.0,
            'qps': 1.0
        }
    }
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    systems = list(benchmarks.keys())
    colors = ['lightcoral', 'gold', 'lightgreen']
    
    # Tempo medio
    times = [benchmarks[sys]['tempo_medio'] for sys in systems]
    bars1 = ax1.bar(systems, times, color=colors)
    ax1.set_ylabel('Tempo Medio (secondi)')
    ax1.set_title('Confronto Tempi di Risposta')
    ax1.grid(True, alpha=0.3)
    for bar, time in zip(bars1, times):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{time:.1f}s', ha='center', va='bottom')
    
    # Tasso successo
    success_rates = [benchmarks[sys]['successo'] for sys in systems]
    bars2 = ax2.bar(systems, success_rates, color=colors)
    ax2.set_ylabel('Tasso di Successo (%)')
    ax2.set_title('Confronto Affidabilità')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    for bar, rate in zip(bars2, success_rates):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom')
    
    # Query per secondo
    qps_values = [benchmarks[sys]['qps'] for sys in systems]
    bars3 = ax3.bar(systems, qps_values, color=colors)
    ax3.set_ylabel('Query per Secondo')
    ax3.set_title('Confronto Throughput')
    ax3.grid(True, alpha=0.3)
    for bar, qps in zip(bars3, qps_values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{qps:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('results/performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("📊 Generato: performance_comparison.png")

def create_summary_dashboard(data):
    """Dashboard riassuntivo per la tesi"""
    perf = data['performance_data']
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
    
    # Titolo principale
    fig.suptitle('Dashboard Performance Chatbot RAG - Tesi Triennale', 
                fontsize=16, fontweight='bold', y=0.95)
    
    # Metriche principali (cards)
    metrics = [
        ('Query Totali', data['queries_total'], 'blue'),
        ('Successo Rate', f"{perf['success_rate']:.1f}%", 'green'),
        ('Tempo Medio', f"{perf['avg_response_time']:.1f}s", 'orange'),
        ('Grade', perf['grade'], 'red' if perf['grade'] in ['D', 'F'] else 'green')
    ]
    
    for i, (label, value, color) in enumerate(metrics):
        ax = fig.add_subplot(gs[0, i])
        ax.text(0.5, 0.5, str(value), ha='center', va='center',
               fontsize=20, fontweight='bold', color=color)
        ax.text(0.5, 0.1, label, ha='center', va='bottom',
               fontsize=12, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, 
                                  fill=False, edgecolor=color, linewidth=2))
    
    # Distribuzione tempi (media riga)
    ax_hist = fig.add_subplot(gs[1, :2])
    ax_hist.hist(data['response_times'], bins=12, alpha=0.7, color='skyblue')
    ax_hist.axvline(np.mean(data['response_times']), color='red', linestyle='--')
    ax_hist.set_xlabel('Tempo di Risposta (s)')
    ax_hist.set_ylabel('Frequenza')
    ax_hist.set_title('Distribuzione Tempi di Risposta')
    ax_hist.grid(True, alpha=0.3)
    
    # Timeline performance
    ax_timeline = fig.add_subplot(gs[1, 2:])
    query_nums = list(range(1, len(data['response_times']) + 1))
    ax_timeline.plot(query_nums, data['response_times'], 'b-', linewidth=2)
    ax_timeline.fill_between(query_nums, data['response_times'], alpha=0.3)
    ax_timeline.set_xlabel('Numero Query')
    ax_timeline.set_ylabel('Tempo (s)')
    ax_timeline.set_title('Performance Timeline')
    ax_timeline.grid(True, alpha=0.3)
    
    # Statistiche dettagliate (bottom)
    ax_stats = fig.add_subplot(gs[2, :])
    stats_text = f"""
STATISTICHE DETTAGLIATE:
• Tempo Minimo: {perf['min_response_time']:.2f}s
• Tempo Massimo: {perf['max_response_time']:.2f}s  
• Tempo Mediano: {perf['median_response_time']:.2f}s
• Query per Secondo: {perf['queries_per_second']:.3f}
• Tempo Totale: {perf['total_time']:.1f}s
• Valutazione: {perf['grade']} - {perf['recommendation']}
• Pronto Produzione: {'SÌ' if perf['production_ready'] else 'NO'}

SISTEMA: ChatBot RAG con Mistral 7B + SentenceTransformers + ChromaDB
DATASET: {data['queries_total']} query realistiche di assistenza universitaria
HARDWARE: Sistema locale con Ollama
    """
    
    ax_stats.text(0.05, 0.95, stats_text, transform=ax_stats.transAxes,
                 fontsize=11, verticalalignment='top', fontfamily='monospace',
                 bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    ax_stats.axis('off')
    
    plt.savefig('results/performance_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("📊 Generato: performance_dashboard.png")

def main():
    """Funzione principale - Genera solo i 2 grafici essenziali per la tesi"""
    print("📈 Generazione Grafici Performance per Tesi")
    print("=" * 50)
    
    # Crea directory results se non esiste
    os.makedirs('results', exist_ok=True)
    
    # Carica dati
    data = load_test_results()
    if not data:
        return
    
    # Genera solo i 2 grafici richiesti per la tesi
    create_response_time_distribution(data)
    create_comparison_chart(data)
    
    print("\n🎉 Grafici generati con successo!")
    print("📁 Disponibili in: results/")
    print("   • response_time_distribution.png")
    print("   • performance_comparison.png")
    print("\n💡 Grafici ottimizzati per inserimento in tesi LaTeX")

if __name__ == "__main__":
    main()