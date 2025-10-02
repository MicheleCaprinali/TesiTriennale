#!/usr/bin/env python3
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

def main():    
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

if __name__ == "__main__":
    main()