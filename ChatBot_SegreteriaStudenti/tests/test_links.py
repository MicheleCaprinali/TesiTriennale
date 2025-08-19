#!/usr/bin/env python3
"""
Test specifico per verificare la gestione dei link nel chatbot
"""

import sys
import os
sys.path.append('src')

from chatbot import setup_chatbot

def test_link_responses():
    """Testa le risposte del chatbot per domande che dovrebbero contenere link"""
    
    print("🧪 TEST GESTIONE LINK - ChatBot RAG")
    print("=" * 50)
    
    chatbot = setup_chatbot()
    if not chatbot:
        print("❌ Setup chatbot fallito!")
        return
    
    # Domande che dovrebbero contenere link specifici
    test_queries = [
        "Come faccio a fare un tirocinio?",
        "Dove trovo informazioni sui tirocini?",
        "Come converto un PDF in PDF/A?",
        "Dove trovo il regolamento tirocini?",
        "Informazioni sui tirocini all'estero"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}/5: {query}")
        print("-" * 40)
        
        result = chatbot.chat(query)
        response = result['response']
        
        print(f"🤖 Risposta: {response}")
        
        # Verifica presenza link
        import re
        links = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', response)
        
        if links:
            print(f"🔗 Link trovati ({len(links)}):")
            for link in links:
                print(f"   • {link}")
        else:
            print("ℹ️  Nessun link nella risposta")
        
        if result['should_redirect']:
            print("🎫 → Suggerisce contatto segreteria")
        
        print()

if __name__ == "__main__":
    test_link_responses()
