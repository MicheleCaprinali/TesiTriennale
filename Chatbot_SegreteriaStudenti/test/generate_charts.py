"""
Genera grafico distribuzione tempi di risposta
Usa dati reali da performance_results.json
"""
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import os

# Configurazione grafico
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def load_results():
    """Carica risultati test da JSON"""
    results_path = Path("results/performance_results.json")
    
    if not results_path.exists():
        print(f"❌ File non trovato: {results_path}")
        print("⚠️  Esegui prima: python test_performance.py")
        return None
    
    with open(results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Caricati {data['queries_total']} risultati")
    return data


def generate_distribution_chart(data):
    """Genera grafico distribuzione tempi di risposta"""
    times = data['response_times']
    metrics = data['performance_metrics']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Istogramma con statistiche
    ax1.hist(times, bins=15, alpha=0.7, color='skyblue', edgecolor='navy')
    ax1.axvline(metrics['avg_response_time'], color='red', linestyle='--', 
                linewidth=2, label=f"Media: {metrics['avg_response_time']:.1f}s")
    ax1.axvline(metrics['median_response_time'], color='orange', linestyle='--', 
                linewidth=2, label=f"Mediana: {metrics['median_response_time']:.1f}s")
    ax1.set_xlabel('Tempo di Risposta (secondi)', fontsize=12)
    ax1.set_ylabel('Frequenza', fontsize=12)
    ax1.set_title('Distribuzione Tempi di Risposta', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # 2. Box plot con dettagli
    bp = ax2.boxplot(times, patch_artist=True, widths=0.6,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5))
    
    ax2.set_ylabel('Tempo di Risposta (secondi)', fontsize=12)
    ax2.set_title('Box Plot Tempi di Risposta', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Aggiungi etichette statistiche al box plot
    y_pos = max(times) * 1.05
    stats_text = (f"Min: {metrics['min_response_time']:.1f}s\n"
                  f"Q1: {np.percentile(times, 25):.1f}s\n"
                  f"Mediana: {metrics['median_response_time']:.1f}s\n"
                  f"Q3: {np.percentile(times, 75):.1f}s\n"
                  f"Max: {metrics['max_response_time']:.1f}s\n"
                  f"Dev.Std: {metrics['std_deviation']:.1f}s")
    
    ax2.text(1.35, np.median(times), stats_text, 
            fontsize=10, verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Titolo generale
    plt.suptitle('Test Prestazionali ChatBot UniBg',
             fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    # Salva grafico
    output_path = 'results/response_time_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Grafico salvato: {output_path}")
    return output_path


def main():
    """Funzione principale"""
    print("📊 GENERAZIONE GRAFICI PERFORMANCE")
    print("=" * 60)
    
    # Crea directory results se non esiste
    os.makedirs('results', exist_ok=True)
    
    # Carica dati
    data = load_results()
    if not data:
        return
    
    # Verifica che ci siano dati validi
    if not data.get('response_times'):
        print("❌ Nessun tempo di risposta disponibile nei risultati")
        return
    
    # Genera grafico
    print()
    generate_distribution_chart(data)
    
    print()
    print("✅ Grafico generato con successo!")
    print(f"📁 Disponibile in: results/response_time_distribution.png")


if __name__ == "__main__":
    main()
