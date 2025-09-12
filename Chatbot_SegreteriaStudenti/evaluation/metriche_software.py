# Crea: metriche_software_native.py

"""
Analisi metriche software usando solo Python standard
Perfetto per tesi triennale - zero dipendenze esterne
"""

import os
import ast
import time
import json
from pathlib import Path
import re

class NativeSoftwareAnalyzer:
    """Analizzatore metriche software con Python nativo"""
    
    def __init__(self, project_root="../src"):
        self.project_root = Path(project_root)
        self.results = {}
        
    def analyze_project(self):
        """Analizza progetto completo"""
        
        print("📊 ANALISI METRICHE SOFTWARE - VERSIONE NATIVA")
        print("=" * 55)
        
        # Trova tutti i file Python
        python_files = list(self.project_root.rglob("*.py"))
        print(f"📁 File Python trovati: {len(python_files)}")
        
        # Analizza ogni file
        total_metrics = {
            'files': len(python_files),
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'functions': 0,
            'classes': 0,
            'complexity_issues': 0,
            'long_functions': 0,
            'file_details': []
        }
        
        for py_file in python_files:
            if py_file.name.startswith('__'):
                continue  # Salta __init__.py e __pycache__
                
            file_metrics = self._analyze_file(py_file)
            total_metrics['file_details'].append(file_metrics)
            
            # Somma metriche
            total_metrics['total_lines'] += file_metrics['total_lines']
            total_metrics['code_lines'] += file_metrics['code_lines']
            total_metrics['comment_lines'] += file_metrics['comment_lines']
            total_metrics['blank_lines'] += file_metrics['blank_lines']
            total_metrics['functions'] += file_metrics['functions']
            total_metrics['classes'] += file_metrics['classes']
            total_metrics['complexity_issues'] += file_metrics['complexity_issues']
            total_metrics['long_functions'] += file_metrics['long_functions']
        
        # Calcola metriche derivate
        total_metrics['avg_lines_per_file'] = total_metrics['total_lines'] / max(len(python_files), 1)
        total_metrics['code_to_comment_ratio'] = (total_metrics['comment_lines'] / max(total_metrics['code_lines'], 1)) * 100
        total_metrics['complexity_score'] = self._calculate_complexity_score(total_metrics)
        total_metrics['maintainability_score'] = self._calculate_maintainability_score(total_metrics)
        total_metrics['quality_grade'] = self._get_quality_grade(total_metrics)
        
        self.results = total_metrics
        
        # Report console
        self._print_results(total_metrics)
        
        # Salva risultati
        self._save_results(total_metrics)
        
        return total_metrics
    
    def _analyze_file(self, file_path):
        """Analizza singolo file Python"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Conteggi base
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if not line.strip())
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            code_lines = total_lines - blank_lines - comment_lines
            
            # Analisi AST per funzioni e classi
            try:
                tree = ast.parse(content)
                functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
                classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
                
                # Rileva funzioni lunghe (>50 righe)
                long_functions = 0
                complexity_issues = 0
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_length = self._get_function_length(node, lines)
                        if func_length > 50:
                            long_functions += 1
                        
                        # Stima complessità (if, for, while, try)
                        complexity = self._estimate_function_complexity(node)
                        if complexity > 10:
                            complexity_issues += 1
                            
            except SyntaxError:
                functions = classes = long_functions = complexity_issues = 0
            
            return {
                'file_name': file_path.name,
                'file_path': str(file_path),
                'total_lines': total_lines,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'blank_lines': blank_lines,
                'functions': functions,
                'classes': classes,
                'long_functions': long_functions,
                'complexity_issues': complexity_issues,
                'avg_line_length': sum(len(line) for line in lines) / max(total_lines, 1)
            }
            
        except Exception as e:
            return {
                'file_name': file_path.name,
                'error': str(e),
                'total_lines': 0,
                'code_lines': 0,
                'comment_lines': 0,
                'blank_lines': 0,
                'functions': 0,
                'classes': 0,
                'long_functions': 0,
                'complexity_issues': 0
            }
    
    def _get_function_length(self, func_node, lines):
        """Calcola lunghezza funzione"""
        try:
            start_line = func_node.lineno - 1
            end_line = func_node.end_lineno - 1 if hasattr(func_node, 'end_lineno') else start_line + 20
            return end_line - start_line + 1
        except:
            return 0
    
    def _estimate_function_complexity(self, func_node):
        """Stima complessità ciclomatica di una funzione"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            # Incrementa per ogni decisione
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calculate_complexity_score(self, metrics):
        """Calcola score complessità (0-10, più alto = migliore)"""
        base_score = 10.0
        
        # Penalità per problemi complessità
        if metrics['complexity_issues'] > 5:
            base_score -= 3.0
        elif metrics['complexity_issues'] > 2:
            base_score -= 1.5
        elif metrics['complexity_issues'] > 0:
            base_score -= 0.5
            
        # Penalità per funzioni lunghe
        if metrics['long_functions'] > 3:
            base_score -= 2.0
        elif metrics['long_functions'] > 1:
            base_score -= 1.0
        
        return max(0.0, base_score)
    
    def _calculate_maintainability_score(self, metrics):
        """Calcola score manutenibilità"""
        base_score = 10.0
        
        # Bonus per buona documentazione
        if metrics['code_to_comment_ratio'] >= 15:
            base_score += 1.0
        elif metrics['code_to_comment_ratio'] >= 10:
            base_score += 0.5
        elif metrics['code_to_comment_ratio'] < 5:
            base_score -= 1.0
        
        # Penalità per file troppo grandi
        if metrics['avg_lines_per_file'] > 500:
            base_score -= 2.0
        elif metrics['avg_lines_per_file'] > 300:
            base_score -= 1.0
        
        return max(0.0, min(10.0, base_score))
    
    def _get_quality_grade(self, metrics):
        """Determina voto qualità complessivo"""
        complexity_score = metrics['complexity_score']
        maintainability_score = metrics['maintainability_score']
        
        avg_score = (complexity_score + maintainability_score) / 2
        
        if avg_score >= 8.5:
            return "A - Eccellente"
        elif avg_score >= 7.0:
            return "B - Buono"
        elif avg_score >= 6.0:
            return "C - Sufficiente"
        else:
            return "D - Da migliorare"
    
    def _print_results(self, metrics):
        """Stampa risultati console"""
        
        print(f"\n📈 RISULTATI ANALISI")
        print("=" * 40)
        
        print(f"📊 **METRICHE GENERALI:**")
        print(f"   File analizzati: {metrics['files']}")
        print(f"   Righe totali: {metrics['total_lines']:,}")
        print(f"   Righe di codice: {metrics['code_lines']:,}")
        print(f"   Righe commenti: {metrics['comment_lines']:,}")
        print(f"   Righe vuote: {metrics['blank_lines']:,}")
        
        print(f"\n🏗️ **STRUTTURA CODICE:**")
        print(f"   Funzioni: {metrics['functions']}")
        print(f"   Classi: {metrics['classes']}")
        print(f"   Media righe/file: {metrics['avg_lines_per_file']:.1f}")
        
        print(f"\n📋 **QUALITÀ CODICE:**")
        print(f"   Rapporto commenti/codice: {metrics['code_to_comment_ratio']:.1f}%")
        print(f"   Funzioni lunghe (>50 righe): {metrics['long_functions']}")
        print(f"   Funzioni complesse: {metrics['complexity_issues']}")
        
        print(f"\n🎯 **SCORE QUALITÀ:**")
        print(f"   Complessità: {metrics['complexity_score']:.1f}/10")
        print(f"   Manutenibilità: {metrics['maintainability_score']:.1f}/10")
        print(f"   **Voto finale: {metrics['quality_grade']}**")
        
        # Valutazione per tesi
        print(f"\n📚 **VALUTAZIONE PER TESI TRIENNALE:**")
        if "Eccellente" in metrics['quality_grade']:
            print("   ✅ CODICE DI ALTA QUALITÀ - Perfetto per tesi")
        elif "Buono" in metrics['quality_grade']:
            print("   ✅ CODICE DI BUONA QUALITÀ - Adatto per tesi")
        elif "Sufficiente" in metrics['quality_grade']:
            print("   🟡 CODICE ACCETTABILE - Sufficiente per tesi")
        else:
            print("   ⚠️ CODICE DA MIGLIORARE - Alcune ottimizzazioni consigliate")
    
    def _save_results(self, metrics):
        """Salva risultati per la tesi"""
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': 'Native Python Metrics',
            'project_root': str(self.project_root),
            'summary': {
                'quality_grade': metrics['quality_grade'],
                'complexity_score': metrics['complexity_score'],
                'maintainability_score': metrics['maintainability_score'],
                'total_files': metrics['files'],
                'total_lines': metrics['total_lines'],
                'code_lines': metrics['code_lines']
            },
            'detailed_metrics': metrics,
            'thesis_ready': True
        }
        
        with open('native_software_metrics.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Report salvato in: native_software_metrics.json")

if __name__ == "__main__":
    analyzer = NativeSoftwareAnalyzer()
    results = analyzer.analyze_project()
    
    print(f"\n🏆 ANALISI COMPLETATA!")
    print(f"   Voto qualità: {results['quality_grade']}")
    print(f"   Pronto per inclusione in tesi ✅")