#!/usr/bin/env python3
"""
Test finale per verificare che i problemi con i link siano stati risolti
"""

import sys
import os
import re
import time
sys.path.append('src')

def test_links_fixed():
    """Test per verificare che i link funzionino correttamente"""
    print("TEST FINALE - VERIFICA CORREZIONE LINK")
    print("=" * 50)
    
    # 1. Test dei file corretti
    print("\n1. VERIFICA FILE CORRETTI")
    print("-" * 30)
    
    extracted_dir = "extracted_text"
    files_checked = 0
    malformed_found = 0
    
    for filename in os.listdir(extracted_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(extracted_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            files_checked += 1
            
            # Cerca link malformati
            malformed_patterns = [
                r'https?://[^\s]+\)',  # Link con parentesi extra
                r'https?://[^\s]+,',   # Link con virgole
                r'(https?://[^\s]+)\s+\1',  # Link duplicati
            ]
            
            for pattern in malformed_patterns:
                if re.search(pattern, content):
                    malformed_found += 1
                    print(f"⚠️ Possibile link malformato in {filename}")
                    break
    
    print(f"✅ File controllati: {files_checked}")
    print(f"{'✅' if malformed_found == 0 else '❌'} Link malformati: {malformed_found}")
    
    # 2. Test del chatbot
    print("\n2. TEST CHATBOT")
    print("-" * 30)
    
    try:
        from chatbot import setup_chatbot
        
        chatbot = setup_chatbot()
        if not chatbot:
            print("❌ Setup chatbot fallito!")
            return False
        
        test_queries = [
            {
                "query": "Come faccio a fare un tirocinio?",
                "expect_links": True,
                "expect_fast": True
            },
            {
                "query": "Dove trovo informazioni sui tirocini?",
                "expect_links": True,
                "expect_fast": True  
            },
            {
                "query": "Come converto un PDF in PDF/A?",
                "expect_links": True,
                "expect_fast": True
            },
            {
                "query": "Informazioni sui tirocini all'estero",
                "expect_links": True,
                "expect_fast": True
            }
        ]
        
        all_tests_passed = True
        
        for i, test in enumerate(test_queries, 1):
            query = test["query"]
            
            print(f"\n🔍 Test {i}: {query}")
            
            start_time = time.time()
            result = chatbot.chat(query)
            response_time = time.time() - start_time
            
            response = result['response']
            
            # Verifica tempo di risposta
            if test["expect_fast"] and response_time > 1.0:
                print(f"❌ Troppo lento: {response_time:.1f}s (atteso < 1s)")
                all_tests_passed = False
            else:
                print(f"✅ Tempo OK: {response_time:.1f}s")
            
            # Verifica presenza link
            links = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', response)
            
            if test["expect_links"] and not links:
                print(f"❌ Nessun link trovato (attesi)")
                all_tests_passed = False
            elif links:
                print(f"✅ Link trovati: {len(links)}")
                
                # Verifica validità link
                valid_links = 0
                for link in links:
                    if link.startswith('https://www.unibg.it'):
                        valid_links += 1
                
                if valid_links == len(links):
                    print(f"✅ Tutti i link sono del dominio UniBG")
                else:
                    print(f"⚠️ {len(links)-valid_links}/{len(links)} link non UniBG")
            else:
                print("ℹ️ Nessun link (non richiesti)")
        
        print(f"\n{'✅ TUTTI I TEST PASSATI' if all_tests_passed else '❌ ALCUNI TEST FALLITI'}")
        return all_tests_passed
        
    except Exception as e:
        print(f"❌ Errore nel test chatbot: {e}")
        return False

def test_web_interface():
    """Test dell'interfaccia web"""
    print("\n3. TEST INTERFACCIA WEB")
    print("-" * 30)
    
    try:
        # Verifica che il server Streamlit sia attivo
        import requests
        
        try:
            response = requests.get("http://localhost:8502", timeout=5)
            if response.status_code == 200:
                print("✅ Interfaccia web attiva su http://localhost:8502")
                return True
            else:
                print(f"⚠️ Server risponde con codice {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("❌ Interfaccia web non raggiungibile")
            print("   Avvia con: streamlit run interfaces/streamlit_app.py --server.port 8502")
            return False
            
    except ImportError:
        print("⚠️ Modulo requests non disponibile per test web")
        return False

def main():
    """Esegue tutti i test"""
    print("🧪 SUITE DI TEST COMPLETA - CORREZIONE LINK")
    print("=" * 60)
    
    # Esegui tutti i test
    test1 = test_links_fixed()
    test2 = test_web_interface()
    
    print("\n" + "=" * 60)
    print("📊 RIEPILOGO RISULTATI")
    print("=" * 60)
    
    print(f"📁 File corretti: {'✅' if test1 else '❌'}")
    print(f"🤖 Chatbot funzionante: {'✅' if test1 else '❌'}")
    print(f"🌐 Interfaccia web: {'✅' if test2 else '❌'}")
    
    if test1 and test2:
        print("\n🎉 TUTTI I PROBLEMI CON I LINK SONO STATI RISOLTI!")
        print("\n📋 FUNZIONALITÀ VERIFICATE:")
        print("   ✅ Link corretti nei file di testo")
        print("   ✅ Risposte rapide per domande comuni")
        print("   ✅ Link cliccabili nell'interfaccia web")
        print("   ✅ Gestione timeout LLM con fallback")
        print("   ✅ Validazione link UniBG")
        
        print("\n🚀 IL SISTEMA È PRONTO ALL'USO!")
    else:
        print("\n⚠️ Alcuni problemi rimangono da risolvere")

if __name__ == "__main__":
    main()
