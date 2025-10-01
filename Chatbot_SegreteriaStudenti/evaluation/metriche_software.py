"""
Analisi metriche software per tesi triennale
Focus su complessità ciclomatica e qualità del codice
"""

import ast
import time
import json
from pathlib import Path

class NativeSoftwareAnalyzer:
    """Analizzatore metriche software con Python nativo"""
    
    def __init__(self, project_root=".."):
        self.project_root = Path(project_root)
        self.results = {}
        
    def analyze_project(self):
        """Analizza progetto completo con focus su complessità ciclomatica"""
        
        print("ANALISI METRICHE SOFTWARE")
        print("=" * 30)
        
        # Analizza file specifici del chatbot
        python_files = self._get_chatbot_files()
        print(f"File Python analizzati: {len(python_files)}")
        for f in python_files:
            print(f"  - {f.relative_to(self.project_root)}")
        
        # Analizza metriche di base per ogni file
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
                continue  # Salta file system Python
                
            file_metrics = self._analyze_file(py_file)
            total_metrics['file_details'].append(file_metrics)
            
            # Accumula statistiche totali
            total_metrics['total_lines'] += file_metrics['total_lines']
            total_metrics['code_lines'] += file_metrics['code_lines']
            total_metrics['comment_lines'] += file_metrics['comment_lines']
            total_metrics['blank_lines'] += file_metrics['blank_lines']
            total_metrics['functions'] += file_metrics['functions']
            total_metrics['classes'] += file_metrics['classes']
            total_metrics['complexity_issues'] += file_metrics['complexity_issues']
            total_metrics['long_functions'] += file_metrics['long_functions']
        
        # Calcola statistiche derivate per analisi qualitativa
        total_metrics['avg_lines_per_file'] = total_metrics['total_lines'] / max(len(python_files), 1)
        total_metrics['code_to_comment_ratio'] = (total_metrics['comment_lines'] / max(total_metrics['code_lines'], 1)) * 100
        
        # Analisi complessità ciclomatica dettagliata
        total_metrics['complexity_analysis'] = self._analyze_complexity_distribution(total_metrics)
        total_metrics['complexity_stats'] = self._calculate_complexity_stats(total_metrics)
        
        self.results = total_metrics
        
        self._print_results(total_metrics)
        self._save_results(total_metrics)
        
        return total_metrics
    
    def _get_chatbot_files(self):
        """Ottiene lista file Python del chatbot da analizzare"""
        files_to_analyze = []
        
        # 1. File principale
        main_file = self.project_root / "main.py"
        if main_file.exists():
            files_to_analyze.append(main_file)
        
        # 2. Tutti i file src/
        src_dir = self.project_root / "src"
        if src_dir.exists():
            for py_file in src_dir.glob("*.py"):
                if not py_file.name.startswith('__'):
                    files_to_analyze.append(py_file)
        
        # 3. Interfaccia Streamlit
        streamlit_file = self.project_root / "interfaccia" / "streamlit.py"
        if streamlit_file.exists():
            files_to_analyze.append(streamlit_file)
        
        return files_to_analyze
    
    def _analyze_file(self, file_path):
        """Analizza singolo file Python per metriche di base"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Conteggi linee base
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if not line.strip())
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            code_lines = total_lines - blank_lines - comment_lines
            
            # Analisi AST per strutture
            try:
                tree = ast.parse(content)
                functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
                classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
                
                # Conta funzioni problematiche
                long_functions = 0
                complexity_issues = 0
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_length = self._get_function_length(node, lines)
                        if func_length > 50:
                            long_functions += 1
                        
                        # Calcola complessità ciclomatica
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
                'avg_line_length': sum(len(line) for line in lines) / max(total_lines, 1),
                'complexity_details': self._get_file_complexity_details(tree) if 'tree' in locals() else []
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
        """Calcola complessità ciclomatica di una funzione"""
        complexity = 1  # Base
        
        for node in ast.walk(func_node):
            # Conta decisioni e costrutti di controllo
            if isinstance(node, ast.If):
                complexity += 1
            elif isinstance(node, ast.While):
                complexity += 1
            elif isinstance(node, ast.For):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                # Operatori booleani (and, or)
                complexity += len(node.values) - 1
            elif isinstance(node, ast.Compare) and len(node.ops) > 1:
                # Confronti multipli (a < b < c)
                complexity += len(node.ops) - 1
        
        return complexity
    
    def _get_file_complexity_details(self, tree):
        """Estrae dettagli complessità per ogni funzione"""
        complexity_details = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._estimate_function_complexity(node)
                complexity_details.append({
                    'function_name': node.name,
                    'complexity': complexity,
                    'line_start': node.lineno,
                    'level': self._classify_complexity_level(complexity)
                })
        
        return complexity_details
    
    def _classify_complexity_level(self, complexity):
        """Classifica livello di complessità"""
        if complexity <= 5:
            return "Bassa"
        elif complexity <= 10:
            return "Media"
        elif complexity <= 15:
            return "Alta"
        else:
            return "Molto Alta"
    
    def _analyze_complexity_distribution(self, metrics):
        """Analizza distribuzione della complessità nel progetto"""
        all_complexities = []
        
        for file_detail in metrics['file_details']:
            if 'complexity_details' in file_detail:
                for func_detail in file_detail['complexity_details']:
                    all_complexities.append(func_detail['complexity'])
        
        if not all_complexities:
            return {
                'total_functions': 0,
                'avg_complexity': 0,
                'max_complexity': 0,
                'min_complexity': 0,
                'distribution': {}
            }
        
        return {
            'total_functions': len(all_complexities),
            'avg_complexity': sum(all_complexities) / len(all_complexities),
            'max_complexity': max(all_complexities),
            'min_complexity': min(all_complexities),
            'distribution': self._calculate_complexity_distribution(all_complexities)
        }
    
    def _calculate_complexity_distribution(self, complexities):
        """Calcola distribuzione percentuale complessità"""
        if not complexities:
            return {}
            
        total = len(complexities)
        
        low = sum(1 for c in complexities if c <= 5)
        medium = sum(1 for c in complexities if 6 <= c <= 10)
        high = sum(1 for c in complexities if 11 <= c <= 15)
        very_high = sum(1 for c in complexities if c > 15)
        
        return {
            'bassa_1_5': round((low / total) * 100, 1),
            'media_6_10': round((medium / total) * 100, 1),
            'alta_11_15': round((high / total) * 100, 1),
            'molto_alta_16+': round((very_high / total) * 100, 1)
        }
    
    def _calculate_complexity_stats(self, metrics):
        """Calcola statistiche qualitative complessità"""
        complexity_analysis = metrics['complexity_analysis']
        
        if complexity_analysis['total_functions'] == 0:
            return {
                'qualita_complessita': 'N/A',
                'funzioni_problematiche': 0,
                'percentuale_buona_qualita': 0
            }
        
        total_functions = complexity_analysis['total_functions']
        good_quality_functions = sum(1 for file_detail in metrics['file_details'] 
                                   if 'complexity_details' in file_detail
                                   for func_detail in file_detail['complexity_details']
                                   if func_detail['complexity'] <= 10)
        
        percentage_good = (good_quality_functions / total_functions) * 100
        problematic_functions = total_functions - good_quality_functions
        
        # Classifica qualità complessiva
        if percentage_good >= 90:
            quality_level = "Eccellente"
        elif percentage_good >= 80:
            quality_level = "Buona"
        elif percentage_good >= 70:
            quality_level = "Sufficiente"
        else:
            quality_level = "Da migliorare"
        
        return {
            'qualita_complessita': quality_level,
            'funzioni_problematiche': problematic_functions,
            'percentuale_buona_qualita': round(percentage_good, 1)
        }
    
    def _print_results(self, metrics):
        """Stampa risultati analisi"""
        
        print(f"\nRISULTATI ANALISI METRICHE SOFTWARE")
        print("=" * 40)
        
        print(f"METRICHE GENERALI:")
        print(f"   File analizzati: {metrics['files']}")
        print(f"   Righe totali: {metrics['total_lines']:,}")
        print(f"   Righe di codice: {metrics['code_lines']:,}")
        print(f"   Righe commenti: {metrics['comment_lines']:,}")
        print(f"   Righe vuote: {metrics['blank_lines']:,}")
        
        print(f"\nSTRUTTURA CODICE:")
        print(f"   Funzioni totali: {metrics['functions']}")
        print(f"   Classi: {metrics['classes']}")
        print(f"   Media righe/file: {metrics['avg_lines_per_file']:.1f}")
        print(f"   Rapporto commenti/codice: {metrics['code_to_comment_ratio']:.1f}%")
        
        # Analisi complessità
        complexity_analysis = metrics['complexity_analysis']
        complexity_stats = metrics['complexity_stats']
        
        print(f"\nANALISI COMPLESSITÀ CICLOMATICA:")
        print(f"   Funzioni analizzate: {complexity_analysis['total_functions']}")
        print(f"   Complessità media: {complexity_analysis['avg_complexity']:.2f}")
        print(f"   Complessità massima: {complexity_analysis['max_complexity']}")
        print(f"   Complessità minima: {complexity_analysis['min_complexity']}")
        
        print(f"\nDISTRIBUZIONE COMPLESSITÀ:")
        distribution = complexity_analysis['distribution']
        print(f"   Bassa (1-5): {distribution.get('bassa_1_5', 0)}%")
        print(f"   Media (6-10): {distribution.get('media_6_10', 0)}%")
        print(f"   Alta (11-15): {distribution.get('alta_11_15', 0)}%")
        print(f"   Molto Alta (16+): {distribution.get('molto_alta_16+', 0)}%")
        
        print(f"\nVALUTAZIONE QUALITÀ:")
        print(f"   Qualità complessiva: {complexity_stats['qualita_complessita']}")
        print(f"   Funzioni di buona qualità: {complexity_stats['percentuale_buona_qualita']}%")
        print(f"   Funzioni problematiche (>10): {complexity_stats['funzioni_problematiche']}")
        
        print(f"\nALTRE METRICHE:")
        print(f"   Funzioni lunghe (>50 righe): {metrics['long_functions']}")
        print(f"   Funzioni molto complesse (>10): {metrics['complexity_issues']}")
        
        # Top 5 funzioni più complesse
        print(f"\nFUNZIONI PIÙ COMPLESSE:")
        all_functions = []
        for file_detail in metrics['file_details']:
            if 'complexity_details' in file_detail:
                for func_detail in file_detail['complexity_details']:
                    all_functions.append({
                        'file': file_detail['file_name'],
                        'function': func_detail['function_name'],
                        'complexity': func_detail['complexity'],
                        'level': func_detail['level']
                    })
        
        all_functions.sort(key=lambda x: x['complexity'], reverse=True)
        for i, func in enumerate(all_functions[:5]):
            print(f"   {i+1}. {func['function']} ({func['file']}): {func['complexity']} - {func['level']}")
        
        print(f"\nAnalisi completata - Dati pronti per tesi")
    
    def _save_results(self, metrics):
        """Salva risultati JSON per tesi"""
        
        results_dir = Path("../results")
        results_dir.mkdir(exist_ok=True)
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': 'Metriche Software - Complessità Ciclomatica',
            'project_root': str(self.project_root),
            'analyzed_files': [str(f.relative_to(self.project_root)) for f in self._get_chatbot_files()],
            'summary': {
                'total_files': metrics['files'],
                'total_lines': metrics['total_lines'],
                'code_lines': metrics['code_lines'],
                'total_functions': metrics['functions'],
                'total_classes': metrics['classes']
            },
            'complexity_analysis': metrics['complexity_analysis'],
            'complexity_stats': metrics['complexity_stats'],
            'detailed_metrics': metrics,
            'thesis_ready': True
        }
        
        output_file = results_dir / 'metriche_software_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Report salvato in: {output_file}")

if __name__ == "__main__":
    analyzer = NativeSoftwareAnalyzer()
    results = analyzer.analyze_project()
    
    print(f"\nANALISI COMPLETATA!")
    complexity_stats = results['complexity_stats']
    print(f"Qualità complessità: {complexity_stats['qualita_complessita']}")
    print(f"Funzioni di buona qualità: {complexity_stats['percentuale_buona_qualita']}%")
    print(f"Dati pronti per tesi")