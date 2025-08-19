#!/usr/bin/env python3
"""
Analisi Metriche Software - ChatBot RAG
Calcola CC, WMC, LCOM e altre metriche per la tesi

Metriche implementate:
- CC (Cyclomatic Complexity)
- WMC (Weighted Methods per Class)  
- LCOM (Lack of Cohesion in Methods)
- Robert Martin's Metrics (Ca, Ce, Instability)
- Lines of Code, Function Count, etc.
"""

import ast
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class CodeMetricsAnalyzer:
    """Analizzatore di metriche software per Python"""
    
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.metrics = {}
        
    def analyze_cyclomatic_complexity(self, node) -> int:
        """Calcola Cyclomatic Complexity (CC)"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Decision points che aumentano la complessità
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
                
        return complexity
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analizza un singolo file Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            
            metrics = {
                'file': str(file_path),
                'lines_of_code': len(content.splitlines()),
                'classes': [],
                'functions': [],
                'imports': [],
                'total_cc': 0
            }
            
            # Analizza classi e metodi
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_metrics = self.analyze_class(node)
                    metrics['classes'].append(class_metrics)
                    
                elif isinstance(node, ast.FunctionDef):
                    if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree) if hasattr(parent, 'body') and node in getattr(parent, 'body', [])):
                        func_metrics = self.analyze_function(node)
                        metrics['functions'].append(func_metrics)
                        metrics['total_cc'] += func_metrics['cc']
                        
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    metrics['imports'].append(self.get_import_name(node))
            
            return metrics
            
        except Exception as e:
            print(f"❌ Errore analisi {file_path}: {e}")
            return {'file': str(file_path), 'error': str(e)}
    
    def analyze_class(self, class_node) -> Dict[str, Any]:
        """Analizza una classe e calcola WMC, LCOM"""
        methods = []
        total_cc = 0
        instance_variables = set()
        method_variables = {}
        
        # Analizza tutti i metodi della classe
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                method_metrics = self.analyze_function(node)
                methods.append(method_metrics)
                total_cc += method_metrics['cc']
                
                # Raccoglie variabili per LCOM
                variables = self.get_method_variables(node)
                method_variables[node.name] = variables
                instance_variables.update(variables)
        
        # Calcola WMC (Weighted Methods per Class)
        wmc = total_cc
        
        # Calcola LCOM (Lack of Cohesion in Methods)
        lcom = self.calculate_lcom(method_variables)
        
        return {
            'name': class_node.name,
            'methods': methods,
            'method_count': len(methods),
            'wmc': wmc,
            'lcom': lcom,
            'instance_variables': len(instance_variables)
        }
    
    def analyze_function(self, func_node) -> Dict[str, Any]:
        """Analizza una funzione"""
        cc = self.analyze_cyclomatic_complexity(func_node)
        
        return {
            'name': func_node.name,
            'cc': cc,
            'lines': len(func_node.body) if hasattr(func_node, 'body') else 0,
            'parameters': len(func_node.args.args) if hasattr(func_node, 'args') else 0
        }
    
    def get_method_variables(self, method_node) -> set:
        """Estrae variabili di istanza usate in un metodo"""
        variables = set()
        
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id == 'self':
                    variables.add(node.attr)
                    
        return variables
    
    def calculate_lcom(self, method_variables: Dict[str, set]) -> float:
        """Calcola LCOM (Lack of Cohesion in Methods)"""
        if len(method_variables) < 2:
            return 0
        
        methods = list(method_variables.keys())
        total_pairs = 0
        sharing_pairs = 0
        
        # Confronta ogni coppia di metodi
        for i in range(len(methods)):
            for j in range(i + 1, len(methods)):
                total_pairs += 1
                vars_i = method_variables[methods[i]]
                vars_j = method_variables[methods[j]]
                
                # Se condividono almeno una variabile
                if vars_i.intersection(vars_j):
                    sharing_pairs += 1
        
        if total_pairs == 0:
            return 0
        
        # LCOM = 1 - (sharing_pairs / total_pairs)
        return 1 - (sharing_pairs / total_pairs)
    
    def get_import_name(self, import_node) -> str:
        """Estrae nome del modulo importato"""
        if isinstance(import_node, ast.Import):
            return import_node.names[0].name if import_node.names else "unknown"
        elif isinstance(import_node, ast.ImportFrom):
            return import_node.module or "relative"
        return "unknown"
    
    def analyze_project(self) -> Dict[str, Any]:
        """Analizza tutto il progetto"""
        print("🔍 Analisi Metriche Software del Progetto")
        print("=" * 50)
        
        project_metrics = {
            'files': [],
            'summary': {
                'total_files': 0,
                'total_lines': 0,
                'total_classes': 0,
                'total_functions': 0,
                'average_cc': 0,
                'max_cc': 0,
                'total_imports': 0
            }
        }
        
        # Analizza file Python del progetto
        python_files = list(self.project_root.rglob("*.py"))
        
        # Filtra file di sistema/venv
        python_files = [f for f in python_files if not any(
            exclude in str(f) for exclude in 
            ['venv', '__pycache__', '.git', 'site-packages']
        )]
        
        total_cc = 0
        cc_values = []
        
        for file_path in python_files:
            print(f"📝 Analizzando: {file_path.name}")
            file_metrics = self.analyze_file(file_path)
            
            if 'error' not in file_metrics:
                project_metrics['files'].append(file_metrics)
                
                # Aggiorna summary
                project_metrics['summary']['total_lines'] += file_metrics['lines_of_code']
                project_metrics['summary']['total_classes'] += len(file_metrics['classes'])
                project_metrics['summary']['total_functions'] += len(file_metrics['functions'])
                project_metrics['summary']['total_imports'] += len(file_metrics['imports'])
                
                total_cc += file_metrics['total_cc']
                
                # Raccoglie CC dei singoli metodi/funzioni
                for cls in file_metrics['classes']:
                    for method in cls['methods']:
                        cc_values.append(method['cc'])
                        
                for func in file_metrics['functions']:
                    cc_values.append(func['cc'])
        
        project_metrics['summary']['total_files'] = len(project_metrics['files'])
        project_metrics['summary']['average_cc'] = total_cc / max(len(cc_values), 1)
        project_metrics['summary']['max_cc'] = max(cc_values) if cc_values else 0
        
        return project_metrics
    
    def calculate_robert_martin_metrics(self, project_metrics: Dict) -> Dict[str, Any]:
        """Calcola metriche di Robert Martin (Ca, Ce, Instability)"""
        print("\n📊 Calcolo metriche Robert Martin...")
        
        # Mappa moduli e dipendenze
        modules = {}
        for file_metrics in project_metrics['files']:
            module_name = Path(file_metrics['file']).stem
            modules[module_name] = {
                'imports': file_metrics['imports'],
                'afferent': 0,  # Ca: incoming dependencies
                'efferent': len(file_metrics['imports'])  # Ce: outgoing dependencies
            }
        
        # Calcola dipendenze afferenti (Ca)
        for module_name, module_data in modules.items():
            for other_module, other_data in modules.items():
                if module_name != other_module:
                    if module_name in other_data['imports']:
                        module_data['afferent'] += 1
        
        # Calcola Instability (I = Ce / (Ca + Ce))
        robert_martin = {}
        for module_name, module_data in modules.items():
            ca = module_data['afferent']
            ce = module_data['efferent']
            instability = ce / (ca + ce) if (ca + ce) > 0 else 0
            
            robert_martin[module_name] = {
                'Ca': ca,
                'Ce': ce,
                'Instability': instability
            }
        
        return robert_martin
    
    def generate_report(self, project_metrics: Dict, robert_martin: Dict) -> str:
        """Genera report dettagliato delle metriche"""
        print("\n📋 Generazione report...")
        
        report = "# 📊 REPORT METRICHE SOFTWARE - ChatBot RAG\n\n"
        
        # Summary generale
        summary = project_metrics['summary']
        report += f"## 🎯 SUMMARY GENERALE\n\n"
        report += f"- **File analizzati:** {summary['total_files']}\n"
        report += f"- **Linee di codice totali:** {summary['total_lines']}\n"
        report += f"- **Classi totali:** {summary['total_classes']}\n"
        report += f"- **Funzioni totali:** {summary['total_functions']}\n"
        report += f"- **Import totali:** {summary['total_imports']}\n"
        report += f"- **CC medio:** {summary['average_cc']:.2f}\n"
        report += f"- **CC massimo:** {summary['max_cc']}\n\n"
        
        # Analisi per file
        report += "## 📁 ANALISI PER FILE\n\n"
        for file_metrics in project_metrics['files']:
            file_name = Path(file_metrics['file']).name
            report += f"### {file_name}\n"
            report += f"- **LOC:** {file_metrics['lines_of_code']}\n"
            report += f"- **Classi:** {len(file_metrics['classes'])}\n"
            report += f"- **Funzioni:** {len(file_metrics['functions'])}\n"
            report += f"- **CC totale:** {file_metrics['total_cc']}\n"
            
            # Dettagli classi
            for cls in file_metrics['classes']:
                report += f"  - **Classe {cls['name']}:** WMC={cls['wmc']}, LCOM={cls['lcom']:.2f}\n"
            
            report += "\n"
        
        # Metriche Robert Martin
        report += "## 🔗 METRICHE ROBERT MARTIN\n\n"
        report += "| Modulo | Ca (Afferent) | Ce (Efferent) | Instability |\n"
        report += "|--------|---------------|---------------|-------------|\n"
        for module, metrics in robert_martin.items():
            report += f"| {module} | {metrics['Ca']} | {metrics['Ce']} | {metrics['Instability']:.3f} |\n"
        
        return report
    
    def create_visualizations(self, project_metrics: Dict, robert_martin: Dict):
        """Crea grafici delle metriche"""
        print("\n📈 Creazione visualizzazioni...")
        
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('📊 Metriche Software - ChatBot RAG', fontsize=16, fontweight='bold')
        
        # 1. Distribuzione Cyclomatic Complexity
        cc_values = []
        for file_metrics in project_metrics['files']:
            for cls in file_metrics['classes']:
                for method in cls['methods']:
                    cc_values.append(method['cc'])
            for func in file_metrics['functions']:
                cc_values.append(func['cc'])
        
        axes[0,0].hist(cc_values, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0,0].set_title('Distribuzione Cyclomatic Complexity')
        axes[0,0].set_xlabel('CC Value')
        axes[0,0].set_ylabel('Frequency')
        
        # 2. Lines of Code per file
        files = [Path(f['file']).name for f in project_metrics['files']]
        loc_values = [f['lines_of_code'] for f in project_metrics['files']]
        
        axes[0,1].bar(range(len(files)), loc_values, color='lightgreen', alpha=0.8)
        axes[0,1].set_title('Lines of Code per File')
        axes[0,1].set_xlabel('Files')
        axes[0,1].set_ylabel('LOC')
        axes[0,1].set_xticks(range(len(files)))
        axes[0,1].set_xticklabels(files, rotation=45, ha='right')
        
        # 3. Robert Martin Instability
        modules = list(robert_martin.keys())
        instability_values = [robert_martin[m]['Instability'] for m in modules]
        
        axes[1,0].bar(modules, instability_values, color='coral', alpha=0.8)
        axes[1,0].set_title('Instability per Modulo (Robert Martin)')
        axes[1,0].set_xlabel('Modules')
        axes[1,0].set_ylabel('Instability (I)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. WMC per classi
        class_names = []
        wmc_values = []
        for file_metrics in project_metrics['files']:
            for cls in file_metrics['classes']:
                class_names.append(cls['name'])
                wmc_values.append(cls['wmc'])
        
        if class_names:
            axes[1,1].bar(class_names, wmc_values, color='gold', alpha=0.8)
            axes[1,1].set_title('WMC (Weighted Methods per Class)')
            axes[1,1].set_xlabel('Classes')
            axes[1,1].set_ylabel('WMC')
            axes[1,1].tick_params(axis='x', rotation=45)
        else:
            axes[1,1].text(0.5, 0.5, 'Nessuna classe trovata', 
                         ha='center', va='center', transform=axes[1,1].transAxes)
            axes[1,1].set_title('WMC - Nessuna classe')
        
        plt.tight_layout()
        plt.savefig('results/software_metrics_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Grafici salvati in: results/software_metrics_analysis.png")
        
        return fig

def main():
    """Esegue analisi completa delle metriche software"""
    print("🚀 ANALISI METRICHE SOFTWARE - CHATBOT RAG")
    print("=" * 60)
    
    # Assicurati che la cartella results esista
    os.makedirs('results', exist_ok=True)
    
    # Inizializza analyzer
    analyzer = CodeMetricsAnalyzer(".")
    
    # Analizza progetto
    project_metrics = analyzer.analyze_project()
    
    # Calcola metriche Robert Martin
    robert_martin = analyzer.calculate_robert_martin_metrics(project_metrics)
    
    # Genera report
    report = analyzer.generate_report(project_metrics, robert_martin)
    
    # Salva report
    with open('results/software_metrics_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Salva dati JSON per ulteriori elaborazioni
    metrics_data = {
        'project_metrics': project_metrics,
        'robert_martin': robert_martin,
        'timestamp': str(pd.Timestamp.now())
    }
    
    with open('results/software_metrics_data.json', 'w', encoding='utf-8') as f:
        json.dump(metrics_data, f, indent=2, ensure_ascii=False)
    
    # Crea visualizzazioni
    analyzer.create_visualizations(project_metrics, robert_martin)
    
    print(f"\n✅ ANALISI COMPLETATA!")
    print(f"📋 Report: results/software_metrics_report.md")
    print(f"📊 Grafici: results/software_metrics_analysis.png")
    print(f"💾 Dati: results/software_metrics_data.json")
    
    # Mostra summary
    summary = project_metrics['summary']
    print(f"\n🎯 HIGHLIGHTS:")
    print(f"   📁 {summary['total_files']} file Python analizzati")
    print(f"   📏 {summary['total_lines']} linee di codice")
    print(f"   🏗️  {summary['total_classes']} classi")
    print(f"   ⚙️  {summary['total_functions']} funzioni")
    print(f"   🔢 CC medio: {summary['average_cc']:.2f}")
    print(f"   ⚠️  CC massimo: {summary['max_cc']}")

if __name__ == "__main__":
    main()
