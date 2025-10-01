#!/usr/bin/env python3
"""
Generatore Risultati e Grafici per Test
======================================
Genera visualizzazioni e report per i risultati dei test per la documentazione della tesi
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns

# Configura matplotlib per non richiedere display
plt.switch_backend('Agg')
sns.set_style("whitegrid")

class TestResultsVisualizer:
    """Genera visualizzazioni per i risultati dei test"""
    
    def __init__(self):
        self.results_dir = os.path.join(os.path.dirname(__file__), "results")  # Corretto path relativo
        self.graphs_dir = os.path.join(self.results_dir, "graphs")
        
        # Crea directory se non esiste
        os.makedirs(self.graphs_dir, exist_ok=True)
        
        # Colori per i grafici
        self.colors = {
            "primary": "#2E86AB",
            "secondary": "#A23B72",
            "success": "#F18F01",
            "warning": "#C73E1D",
            "info": "#6C757D"
        }
    
    def load_test_results(self):
        """Carica tutti i risultati dei test"""
        results = {}
        
        # File dei risultati
        result_files = [
            ("unit", "unit_tests_results.json"),
            ("functional", "functional_tests_results.json"),
            ("performance", "performance_tests_results.json")
        ]
        
        for test_type, filename in result_files:
            filepath = os.path.join(self.results_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        results[test_type] = json.load(f)
                    print(f"✓ Caricati risultati {test_type}")
                except Exception as e:
                    print(f"✗ Errore caricamento {test_type}: {e}")
                    results[test_type] = None
            else:
                print(f"⚠ File non trovato: {filename}")
                results[test_type] = None
        
        return results
    
    def create_test_summary_chart(self, results):
        """Crea grafico riassuntivo di tutti i test"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Riassunto Completo Test Suite Chatbot', fontsize=16, fontweight='bold')
        
        # 1. Tasso di successo per tipo di test
        if results["unit"] and results["functional"] and results["performance"]:
            test_types = ["Unit", "Functional", "Performance"]
            success_rates = [
                results["unit"]["summary"].get("success_rate", 0) * 100,
                results["functional"]["summary"].get("success_rate", 0) * 100,
                results["performance"]["tests"]["sequential"]["statistics"].get("success_rate", 0) * 100
            ]
            
            bars = ax1.bar(test_types, success_rates, color=[self.colors["primary"], self.colors["secondary"], self.colors["success"]])
            ax1.set_title('Tasso di Successo per Tipo di Test')
            ax1.set_ylabel('Percentuale Successo (%)')
            ax1.set_ylim(0, 100)
            
            # Aggiungi valori sulle barre
            for bar, rate in zip(bars, success_rates):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{rate:.1f}%', ha='center', va='bottom')
        
        # 2. Distribuzione tempi di risposta (Performance)
        if results["performance"]:
            perf_data = results["performance"]["tests"]["sequential"]["raw_results"]
            response_times = [r["response_time"] for r in perf_data if r["success"]]
            
            if response_times:
                ax2.hist(response_times, bins=10, color=self.colors["info"], alpha=0.7, edgecolor='black')
                ax2.set_title('Distribuzione Tempi di Risposta')
                ax2.set_xlabel('Tempo di Risposta (secondi)')
                ax2.set_ylabel('Frequenza')
                ax2.axvline(np.mean(response_times), color=self.colors["warning"], 
                           linestyle='--', label=f'Media: {np.mean(response_times):.3f}s')
                ax2.legend()
        
        # 3. Confronto Performance Sequenziale vs Concorrente
        if results["performance"]:
            categories = ['Sequenziale', 'Concorrente']
            seq_stats = results["performance"]["tests"]["sequential"]["statistics"]
            conc_stats = results["performance"]["tests"]["concurrent"]["statistics"]
            
            avg_times = [seq_stats.get("avg_response_time", 0), conc_stats.get("avg_response_time", 0)]
            throughput = [seq_stats.get("throughput_qps", 0), conc_stats.get("throughput_qps", 0)]
            
            x = np.arange(len(categories))
            width = 0.35
            
            bars1 = ax3.bar(x - width/2, avg_times, width, label='Tempo Medio (s)', color=self.colors["primary"])
            ax3_twin = ax3.twinx()
            bars2 = ax3_twin.bar(x + width/2, throughput, width, label='Throughput (QPS)', color=self.colors["success"])
            
            ax3.set_title('Performance: Sequenziale vs Concorrente')
            ax3.set_xlabel('Tipo di Test')
            ax3.set_ylabel('Tempo Medio (secondi)', color=self.colors["primary"])
            ax3_twin.set_ylabel('Throughput (Query/sec)', color=self.colors["success"])
            ax3.set_xticks(x)
            ax3.set_xticklabels(categories)
            
            # Legenda combinata
            lines1, labels1 = ax3.get_legend_handles_labels()
            lines2, labels2 = ax3_twin.get_legend_handles_labels()
            ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        # 4. Test Funzionali - Qualità per Categoria
        if results["functional"]:
            scenarios = results["functional"]["scenarios"]
            categories = []
            quality_scores = []
            
            for scenario_id, scenario_data in scenarios.items():
                if isinstance(scenario_data, dict) and "quality_score" in scenario_data:
                    categories.append(scenario_data.get("category", scenario_id).replace("_", " ").title())
                    quality_scores.append(scenario_data["quality_score"])
            
            if categories and quality_scores:
                bars = ax4.barh(categories, quality_scores, color=self.colors["secondary"])
                ax4.set_title('Qualità Risposta per Categoria')
                ax4.set_xlabel('Punteggio Qualità (0-100)')
                ax4.set_xlim(0, 100)
                
                # Aggiungi valori alle barre
                for i, (bar, score) in enumerate(zip(bars, quality_scores)):
                    width = bar.get_width()
                    ax4.text(width + 1, bar.get_y() + bar.get_height()/2,
                            f'{score:.0f}', ha='left', va='center')
        
        plt.tight_layout()
        
        # Salva grafico
        summary_path = os.path.join(self.graphs_dir, "test_summary_complete.png")
        plt.savefig(summary_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Grafico riassuntivo salvato: {summary_path}")
        return summary_path
    
    def create_performance_details_chart(self, results):
        """Crea grafici dettagliati delle performance"""
        if not results["performance"]:
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Analisi Dettagliata Performance', fontsize=16, fontweight='bold')
        
        perf_data = results["performance"]
        
        # 1. Timeline tempi di risposta sequenziali
        seq_results = perf_data["tests"]["sequential"]["raw_results"]
        seq_times = [r["response_time"] for r in seq_results if r["success"]]
        
        if seq_times:
            ax1.plot(range(1, len(seq_times) + 1), seq_times, 
                    marker='o', linewidth=2, markersize=4, color=self.colors["primary"])
            ax1.set_title('Timeline Tempi di Risposta Sequenziali')
            ax1.set_xlabel('Numero Query')
            ax1.set_ylabel('Tempo di Risposta (s)')
            ax1.grid(True, alpha=0.3)
            
            # Linea media
            mean_time = np.mean(seq_times)
            ax1.axhline(y=mean_time, color=self.colors["warning"], 
                       linestyle='--', label=f'Media: {mean_time:.3f}s')
            ax1.legend()
        
        # 2. Confronto Pattern di Carico
        if "load_patterns" in perf_data["tests"]:
            load_patterns = perf_data["tests"]["load_patterns"]
            pattern_names = []
            avg_times = []
            throughputs = []
            
            for pattern_name, pattern_data in load_patterns.items():
                if "statistics" in pattern_data:
                    stats = pattern_data["statistics"]
                    pattern_names.append(pattern_name.replace("_", " ").title())
                    avg_times.append(stats.get("avg_response_time", 0))
                    throughputs.append(stats.get("throughput_qps", 0))
            
            if pattern_names:
                x = np.arange(len(pattern_names))
                bars = ax2.bar(x, throughputs, color=[self.colors["success"], self.colors["secondary"], self.colors["warning"]])
                ax2.set_title('Throughput per Pattern di Carico')
                ax2.set_xlabel('Pattern di Carico')
                ax2.set_ylabel('Throughput (Query/sec)')
                ax2.set_xticks(x)
                ax2.set_xticklabels(pattern_names)
                
                # Valori sulle barre
                for bar, throughput in zip(bars, throughputs):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                            f'{throughput:.2f}', ha='center', va='bottom')
        
        # 3. Statistiche Distribuzione
        if seq_times:
            stats_data = {
                'Min': min(seq_times),
                'Q1': np.percentile(seq_times, 25),
                'Mediana': np.median(seq_times),
                'Q3': np.percentile(seq_times, 75),
                'Max': max(seq_times),
                'Media': np.mean(seq_times)
            }
            
            ax3.boxplot(seq_times, vert=True, patch_artist=True,
                       boxprops=dict(facecolor=self.colors["info"], alpha=0.7))
            ax3.set_title('Distribuzione Tempi di Risposta')
            ax3.set_ylabel('Tempo di Risposta (s)')
            ax3.set_xticklabels(['Tempi di Risposta'])
            
            # Aggiungi statistiche come testo
            stats_text = '\n'.join([f'{k}: {v:.3f}s' for k, v in stats_data.items()])
            ax3.text(1.3, max(seq_times) * 0.7, stats_text, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # 4. Trend Memoria
        if "memory_behavior" in perf_data["tests"]:
            memory_data = perf_data["tests"]["memory_behavior"]
            memory_results = memory_data.get("results", [])
            
            if memory_results:
                times = [r["response_time"] for r in memory_results if r["success"]]
                iterations = range(1, len(times) + 1)
                
                ax4.plot(iterations, times, marker='s', linewidth=2, 
                        markersize=6, color=self.colors["warning"])
                ax4.set_title('Trend Performance Memoria')
                ax4.set_xlabel('Iterazione')
                ax4.set_ylabel('Tempo di Risposta (s)')
                ax4.grid(True, alpha=0.3)
                
                # Linea di tendenza
                if len(times) > 1:
                    z = np.polyfit(list(iterations), times, 1)
                    p = np.poly1d(z)
                    ax4.plot(iterations, p(list(iterations)), linestyle='--', 
                            color=self.colors["primary"], alpha=0.8, label='Tendenza')
                    
                    trend = memory_data.get("performance_trend_percent", 0)
                    ax4.text(0.02, 0.98, f'Trend: {trend:+.1f}%', 
                            transform=ax4.transAxes, va='top',
                            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
                    ax4.legend()
        
        plt.tight_layout()
        
        # Salva grafico
        performance_path = os.path.join(self.graphs_dir, "performance_details.png")
        plt.savefig(performance_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Grafico performance dettagliato salvato: {performance_path}")
        return performance_path
    
    def create_consolidated_report(self, results):
        """Crea report JSON consolidato per la tesi"""
        
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "test_suite_version": "1.0",
                "purpose": "Documentazione Tesi Triennale - Chatbot Segreteria Studenti"
            },
            "executive_summary": {},
            "detailed_results": {
                "unit_tests": results.get("unit"),
                "functional_tests": results.get("functional"),
                "performance_tests": results.get("performance")
            },
            "recommendations": []
        }
        
        # Calcola sommario esecutivo
        total_tests = 0
        total_passed = 0
        
        if results["unit"]:
            unit_total = results["unit"]["summary"]["total_tests"]
            unit_passed = results["unit"]["summary"]["passed"]
            total_tests += unit_total
            total_passed += unit_passed
        
        if results["functional"]:
            func_total = results["functional"]["summary"]["total_scenarios"]
            func_passed = results["functional"]["summary"]["successful"]
            total_tests += func_total
            total_passed += func_passed
        
        if results["performance"]:
            perf_seq = results["performance"]["tests"]["sequential"]["statistics"]
            if perf_seq.get("success_rate", 0) > 0.95:
                total_passed += 1
            total_tests += 1
        
        report["executive_summary"] = {
            "overall_success_rate": total_passed / total_tests if total_tests > 0 else 0,
            "total_tests_executed": total_tests,
            "tests_passed": total_passed,
            "system_ready_for_production": total_passed / total_tests > 0.9 if total_tests > 0 else False,
            "key_metrics": {
                "avg_response_time": results["performance"]["tests"]["sequential"]["statistics"].get("avg_response_time", 0) if results["performance"] else 0,
                "max_throughput": results["performance"]["tests"]["concurrent"]["statistics"].get("throughput_qps", 0) if results["performance"] else 0,
                "functional_quality_avg": results["functional"]["summary"].get("avg_quality_score", 0) if results["functional"] else 0
            }
        }
        
        # Raccomandazioni basate sui risultati
        if results["performance"]:
            avg_time = results["performance"]["tests"]["sequential"]["statistics"].get("avg_response_time", 0)
            if avg_time > 2.0:
                report["recommendations"].append("Ottimizzare tempi di risposta - attualmente oltre 2 secondi")
            
            success_rate = results["performance"]["tests"]["sequential"]["statistics"].get("success_rate", 0)
            if success_rate < 0.95:
                report["recommendations"].append("Migliorare affidabilità - tasso successo sotto 95%")
        
        if results["functional"]:
            quality = results["functional"]["summary"].get("avg_quality_score", 0)
            if quality < 70:
                report["recommendations"].append("Migliorare qualità risposte - punteggio sotto 70/100")
        
        if not report["recommendations"]:
            report["recommendations"].append("Sistema performante e pronto per deployment")
        
        # Salva report
        report_path = os.path.join(self.results_dir, "consolidated_test_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Report consolidato salvato: {report_path}")
        return report_path

def generate_test_visualizations():
    """Funzione principale per generare tutte le visualizzazioni"""
    
    print("📊 Generazione Visualizzazioni Test")
    print("=" * 50)
    
    visualizer = TestResultsVisualizer()
    
    # Carica risultati
    results = visualizer.load_test_results()
    
    # Genera grafici
    summary_chart = visualizer.create_test_summary_chart(results)
    performance_chart = visualizer.create_performance_details_chart(results)
    
    # Genera report consolidato
    consolidated_report = visualizer.create_consolidated_report(results)
    
    print(f"\n✅ Generazione completata!")
    print(f"   📈 Grafici salvati in: {visualizer.graphs_dir}")
    print(f"   📄 Report consolidato: {consolidated_report}")
    
    return {
        "summary_chart": summary_chart,
        "performance_chart": performance_chart,
        "consolidated_report": consolidated_report
    }

if __name__ == "__main__":
    generate_test_visualizations()