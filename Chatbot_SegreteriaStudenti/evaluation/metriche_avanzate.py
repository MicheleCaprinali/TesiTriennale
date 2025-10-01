"""
Metriche software avanzate WMC e LCOM per tesi triennale
Analisi qualità architettura object-oriented
"""

import ast
import json
import time
from pathlib import Path
from collections import defaultdict

class AdvancedMetricsAnalyzer:
    """Analizzatore WMC e LCOM per valutazione architettura OOP"""
    
    def __init__(self, project_root=".."):
        self.project_root = Path(project_root)
        self.results = {}
        
    def analyze_wmc_lcom_metrics(self):
        """Analisi WMC (Weighted Methods per Class) e LCOM (Lack of Cohesion)"""
        
        print("ANALISI METRICHE AVANZATE - WMC e LCOM")
        print("=" * 40)
        
        print("\nAnalisi WMC e LCOM in corso...")
        metrics = self._analyze_classes_metrics()
        
        # Prepara risultati per salvataggio
        self.results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': 'WMC e LCOM Analysis',
            'analyzed_files': [str(f.relative_to(self.project_root)) for f in self._get_chatbot_files()],
            'metrics': metrics
        }
        
        self._print_results()
        self._save_results()
        
        return self.results
    
    def _analyze_classes_metrics(self):
        """Analizza WMC e LCOM per tutte le classi del chatbot"""
        
        python_files = self._get_chatbot_files()
        print(f"File analizzati: {len(python_files)}")
        for f in python_files:
            print(f"  - {f.relative_to(self.project_root)}")
        
        metrics = {
            'file_analizzati': len(python_files),
            'classi_analizzate': 0,
            'wmc_scores': [],
            'lcom_scores': [],
            'dettagli_classi': []
        }
        
        for py_file in python_files:
            if py_file.name.startswith('__'):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Analizza ogni classe
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_metrics = self._analyze_single_class(node, py_file, content)
                        metrics['dettagli_classi'].append(class_metrics)
                        metrics['classi_analizzate'] += 1
                        
                        # Accumula scores per statistiche
                        metrics['wmc_scores'].append(class_metrics['wmc'])
                        metrics['lcom_scores'].append(class_metrics['lcom'])
                        
            except Exception as e:
                print(f"   Errore analisi {py_file.name}: {e}")
                continue
        
        # Calcola statistiche WMC e LCOM
        if metrics['wmc_scores']:
            metrics['wmc_medio'] = sum(metrics['wmc_scores']) / len(metrics['wmc_scores'])
            metrics['wmc_massimo'] = max(metrics['wmc_scores'])
            metrics['wmc_minimo'] = min(metrics['wmc_scores'])
        else:
            metrics['wmc_medio'] = metrics['wmc_massimo'] = metrics['wmc_minimo'] = 0
            
        if metrics['lcom_scores']:
            metrics['lcom_medio'] = sum(metrics['lcom_scores']) / len(metrics['lcom_scores'])
            metrics['lcom_massimo'] = max(metrics['lcom_scores'])
            metrics['lcom_minimo'] = min(metrics['lcom_scores'])
        else:
            metrics['lcom_medio'] = metrics['lcom_massimo'] = metrics['lcom_minimo'] = 0
        
        # Valutazioni qualitative complessive
        metrics['valutazione_wmc'] = self._valuta_wmc(metrics['wmc_medio'])
        metrics['valutazione_lcom'] = self._valuta_lcom(metrics['lcom_medio'])
        
        print(f"Analizzate {metrics['classi_analizzate']} classi in {len(python_files)} file")
        
        return metrics
    
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
    
    def _analyze_single_class(self, class_node, file_path, content):
        """Analizza singola classe per WMC e LCOM"""
        
        class_name = class_node.name
        
        # WMC - Somma complessità di tutti i metodi
        wmc = self._calculate_wmc(class_node)
        
        # LCOM - Mancanza di coesione tra metodi  
        lcom = self._calculate_lcom(class_node, content)
        
        return {
            'nome_classe': class_name,
            'file': file_path.name,
            'wmc': wmc,
            'lcom': lcom,
            'numero_metodi': len([n for n in class_node.body if isinstance(n, ast.FunctionDef)]),
            'valutazione_wmc': self._classifica_wmc(wmc),
            'valutazione_lcom': self._classifica_lcom(lcom)
        }
    
    def _calculate_wmc(self, class_node):
        """Calcola WMC - Somma complessità ciclomatica tutti i metodi"""
        
        total_complexity = 0
        methods = [n for n in class_node.body if isinstance(n, ast.FunctionDef)]
        
        for method in methods:
            complexity = self._calcola_complessita_metodo(method)
            total_complexity += complexity
            
        return total_complexity
    
    def _calcola_complessita_metodo(self, method_node):
        """Calcola complessità ciclomatica singolo metodo"""
        complexity = 1  # Base
        
        for node in ast.walk(method_node):
            # Conta decisioni e loop
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
                
        return complexity
    
    def _calculate_lcom(self, class_node, content):
        """Calcola LCOM - Percentuale metodi senza attributi condivisi"""
        
        methods = [n for n in class_node.body if isinstance(n, ast.FunctionDef)]
        if len(methods) <= 1:
            return 0  # Non applicabile per 0-1 metodi
            
        # Trova attributi usati da ogni metodo
        method_attributes = {}
        class_attributes = self._trova_attributi_classe(class_node)
        
        for method in methods:
            used_attrs = set()
            for node in ast.walk(method):
                if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'self':
                    if node.attr in class_attributes:
                        used_attrs.add(node.attr)
            method_attributes[method.name] = used_attrs
        
        # Conta coppie di metodi senza attributi condivisi
        pairs_without_shared_attrs = 0
        total_pairs = 0
        
        method_names = list(method_attributes.keys())
        for i in range(len(method_names)):
            for j in range(i + 1, len(method_names)):
                total_pairs += 1
                attrs1 = method_attributes[method_names[i]]
                attrs2 = method_attributes[method_names[j]]
                
                if not attrs1.intersection(attrs2):  # Nessun attributo comune
                    pairs_without_shared_attrs += 1
        
        if total_pairs == 0:
            return 0
            
        return round((pairs_without_shared_attrs / total_pairs) * 100, 1)
    
    def _trova_attributi_classe(self, class_node):
        """Trova tutti gli attributi della classe (principalmente in __init__)"""
        attributes = set()
        
        for node in ast.walk(class_node):
            # Attributi definiti con self.attributo
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                        attributes.add(target.attr)
        
        return attributes
    
    def _classifica_wmc(self, wmc):
        """Classifica livello WMC"""
        if wmc <= 20:
            return "Basso"
        elif wmc <= 50:
            return "Medio"
        elif wmc <= 100:
            return "Alto"
        else:
            return "Molto Alto"
    
    def _classifica_lcom(self, lcom):
        """Classifica livello LCOM"""
        if lcom <= 20:
            return "Buona Coesione"
        elif lcom <= 50:
            return "Coesione Media"
        elif lcom <= 80:
            return "Coesione Bassa"
        else:
            return "Coesione Molto Bassa"
    
    def _valuta_wmc(self, wmc_medio):
        """Valuta WMC medio del progetto"""
        if wmc_medio <= 25:
            return "Eccellente"
        elif wmc_medio <= 40:
            return "Buono"
        elif wmc_medio <= 60:
            return "Sufficiente"
        else:
            return "Da migliorare"
    
    def _valuta_lcom(self, lcom_medio):
        """Valuta LCOM medio del progetto"""
        if lcom_medio <= 30:
            return "Eccellente"
        elif lcom_medio <= 50:
            return "Buono"
        elif lcom_medio <= 70:
            return "Sufficiente"
        else:
            return "Da migliorare"
    
    def _print_results(self):
        """Stampa risultati analisi WMC e LCOM"""
        
        metrics = self.results['metrics']
        
        print(f"\nRISULTATI ANALISI WMC e LCOM")
        print("=" * 35)
        
        print(f"STATISTICHE GENERALI:")
        print(f"   File analizzati: {metrics['file_analizzati']}")
        print(f"   Classi analizzate: {metrics['classi_analizzate']}")
        
        if metrics['classi_analizzate'] > 0:
            print(f"\nMETRICHE WMC (Weighted Methods per Class):")
            print(f"   WMC medio: {metrics['wmc_medio']:.1f}")
            print(f"   WMC massimo: {metrics['wmc_massimo']}")
            print(f"   WMC minimo: {metrics['wmc_minimo']}")
            print(f"   Valutazione WMC: {metrics['valutazione_wmc']}")
            
            print(f"\nMETRICHE LCOM (Lack of Cohesion of Methods):")
            print(f"   LCOM medio: {metrics['lcom_medio']:.1f}%")
            print(f"   LCOM massimo: {metrics['lcom_massimo']:.1f}%")
            print(f"   LCOM minimo: {metrics['lcom_minimo']:.1f}%")
            print(f"   Valutazione LCOM: {metrics['valutazione_lcom']}")
            
            print(f"\nDETTAGLI PER CLASSE:")
            for classe in metrics['dettagli_classi']:
                print(f"   • {classe['nome_classe']} ({classe['file']}):")
                print(f"     - WMC: {classe['wmc']} ({classe['valutazione_wmc']})")
                print(f"     - LCOM: {classe['lcom']}% ({classe['valutazione_lcom']})")
                print(f"     - Metodi: {classe['numero_metodi']}")
                
            print(f"\nINTERPRETAZIONE:")
            print(f"   WMC: Complessità media per classe - {metrics['valutazione_wmc']}")
            print(f"   LCOM: Coesione metodi nelle classi - {metrics['valutazione_lcom']}")
            
        else:
            print("   Nessuna classe trovata da analizzare")
        
        print(f"\nAnalisi WMC e LCOM completata")
    
    def _save_results(self):
        """Salva risultati JSON per tesi"""
        
        results_dir = Path("../results")
        results_dir.mkdir(exist_ok=True)
        
        output_file = results_dir / 'metriche_avanzate_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"Report salvato in: {output_file}")

if __name__ == "__main__":
    analyzer = AdvancedMetricsAnalyzer()
    results = analyzer.analyze_wmc_lcom_metrics()
    
    print(f"\nANALISI WMC e LCOM COMPLETATA!")
    metrics = results['metrics']
    if metrics['classi_analizzate'] > 0:
        print(f"WMC medio: {metrics['wmc_medio']:.1f} ({metrics['valutazione_wmc']})")
        print(f"LCOM medio: {metrics['lcom_medio']:.1f}% ({metrics['valutazione_lcom']})")
    print(f"Dati pronti per tesi")