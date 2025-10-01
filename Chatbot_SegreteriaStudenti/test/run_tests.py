#!/usr/bin/env python3
"""
Test Suite Essenziale - Chatbot Segreteria Studenti
=================================================
Script per eseguire test unitari e prestazionali del chatbot reale
"""

import os
import sys
import json
from datetime import datetime

# Aggiungi path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_essential_test_suite():
    """Esegue la suite essenziale di test"""
    
    print("🧪 SUITE ESSENZIALE - CHATBOT SEGRETERIA STUDENTI")
    print("=" * 60)
    print(f"Avvio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = {
        "suite_start": datetime.now().isoformat(),
        "tests_executed": [],
        "success": True,
        "errors": []
    }
    
    # 1. Test Unitari - Moduli src/
    print("1️⃣ TEST UNITARI - MODULI src/")
    print("-" * 30)
    try:
        from unit.test_components import run_unit_tests
        unit_results = run_unit_tests()
        test_results["tests_executed"].append("unit")
        print("✅ Test unitari completati\n")
    except Exception as e:
        print(f"❌ Errore test unitari: {e}\n")
        test_results["errors"].append(f"Unit tests: {e}")
        test_results["success"] = False
    
    # 2. Test Prestazionali - Chatbot Reale
    print("2️⃣ TEST PRESTAZIONALI - CHATBOT REALE")
    print("-" * 30)
    try:
        from performance.test_performance import run_real_performance_test
        performance_results = run_real_performance_test()
        test_results["tests_executed"].append("performance")
        print("✅ Test prestazionali completati\n")
    except Exception as e:
        print(f"❌ Errore test prestazionali: {e}\n")
        test_results["errors"].append(f"Performance tests: {e}")
        test_results["success"] = False
    
    # Finalizza risultati
    test_results["suite_end"] = datetime.now().isoformat()
    
    # Salva log dell'esecuzione
    log_file = os.path.join(os.path.dirname(__file__), "results", "essential_test_execution.json")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)
    
    # Stampa sommario finale
    print("📋 SOMMARIO ESECUZIONE SUITE")
    print("=" * 60)
    print(f"✅ Test eseguiti: {', '.join(test_results['tests_executed'])}")
    
    if test_results["errors"]:
        print(f"❌ Errori rilevati: {len(test_results['errors'])}")
        for error in test_results["errors"]:
            print(f"   • {error}")
    else:
        print("✅ Nessun errore critico")
    
    print(f"📊 Log esecuzione: {log_file}")
    print(f"📁 Risultati disponibili in: {os.path.join(os.path.dirname(__file__), 'results')}")
    
    if test_results["success"]:
        print("\n🎉 SUITE ESSENZIALE COMPLETATA CON SUCCESSO!")
    else:
        print("\n⚠️ SUITE COMPLETATA CON ALCUNI ERRORI")
    
    return test_results

def run_specific_test(test_type):
    """Esegue un tipo specifico di test"""
    
    if test_type == "unit":
        from unit.test_components import run_unit_tests
        return run_unit_tests()
    elif test_type == "performance":
        from performance.test_performance import run_real_performance_test
        return run_real_performance_test()
    else:
        print(f"❌ Tipo di test non riconosciuto: {test_type}")
        print("   Tipi disponibili: unit, performance")
        return None

def main():
    """Funzione principale con gestione argomenti"""
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type in ["unit", "performance"]:
            print(f"🧪 Esecuzione test specifico: {test_type}")
            result = run_specific_test(test_type)
            
            if result:
                print(f"✅ Test {test_type} completato")
            else:
                print(f"❌ Errore durante test {test_type}")
        
        elif test_type in ["all", "suite", "essential"]:
            run_essential_test_suite()
        
        else:
            print("❌ Argomento non valido")
            print("Uso:")
            print("  python run_tests.py [all|unit|performance]")
            print()
            print("Esempi:")
            print("  python run_tests.py all          # Esegue tutti i test")
            print("  python run_tests.py unit         # Solo test unitari")
            print("  python run_tests.py performance  # Solo test prestazionali reali")
    
    else:
        # Nessun argomento = esegui tutto
        run_essential_test_suite()

if __name__ == "__main__":
    main()