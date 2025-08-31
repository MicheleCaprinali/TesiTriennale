#!/usr/bin/env python3
"""
Test rapido del chatbot migliorato
"""

import sys
sys.path.append('src')

def test_chatbot():
    from chatbot import setup_chatbot
    
    print("TEST CHATBOT MIGLIORATO")
    print("=" * 40)
    
    chatbot = setup_chatbot()
    if not chatbot:
        print("❌ Setup chatbot fallito!")
        return
    
    # Test queries per i link
    test_queries = [
        "Come faccio a fare un tirocinio?",
        "Dove trovo informazioni sui tirocini?", 
        "Come converto un PDF in PDF/A?",
        "Informazioni sui tirocini all'estero"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}: {query}")
        print("-" * 40)
        
        import time
        start = time.time()
        result = chatbot.chat(query)
        end = time.time()
        
        print(f"⏱️ Tempo: {end-start:.1f}s")
        print(f"📄 Contesto trovato: {result['context_found']}")
        print(f"🔄 Dovrebbe reindirizzare: {result['should_redirect']}")
        
        response = result['response']
        print(f"📝 Risposta ({len(response)} caratteri):")
        
        # Trova link nella risposta
        import re
        links = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', response)
        
        if links:
            print(f"🔗 Link trovati ({len(links)}):")
            for link in links:
                print(f"   • {link}")
        else:
            print("❌ Nessun link nella risposta")
        
        # Mostra anteprima risposta
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"💬 Anteprima: {preview}")
        
        print()

if __name__ == "__main__":
    test_chatbot()
