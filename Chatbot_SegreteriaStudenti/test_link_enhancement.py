# Crea: test_link_enhancement.py

"""
Test rapido per verificare il sistema link automatico
"""

import sys
sys.path.append('src')
sys.path.append('evaluation')

from ollama_llm import OllamaLLM
from link_enhancer import LinkEnhancer

def test_link_system():
    """Test del sistema link enhancement"""
    
    print("🧪 TEST SISTEMA LINK AUTOMATICO")
    print("=" * 50)
    
    # Test 1: LinkEnhancer standalone
    print("\n🔧 TEST 1: LinkEnhancer standalone")
    enhancer = LinkEnhancer()
    
    test_text = "Per informazioni contatta la segreteria studenti."
    enhanced = enhancer.enhance_response(test_text, 'generic')
    
    print(f"ORIGINALE: {test_text}")
    print(f"ENHANCED:  {enhanced}")
    print(f"Link count: {enhancer.count_links(enhanced)}")
    
    # Test 2: Integrazione con OllamaLLM  
    print("\n🔧 TEST 2: Integrazione OllamaLLM")
    try:
        llm = OllamaLLM()
        
        # Test domanda semplice per velocità
        test_question = "Qual è l'orario della segreteria?"
        test_context = "La segreteria è aperta dal lunedì al venerdì. Per informazioni contattare la segreteria studenti."
        
        print(f"📝 Domanda: {test_question}")
        print("🔄 Generando risposta con link enhancement...")
        
        response = llm.generate(test_question, test_context)
        
        # Conta link nella risposta
        link_count = enhancer.count_links(response)
        
        print(f"\n✅ RISPOSTA GENERATA ({len(response)} caratteri):")
        print("-" * 30)
        print(response[:400] + "..." if len(response) > 400 else response)
        print("-" * 30)
        print(f"🔗 Link totali nella risposta: {link_count}")
        
        # Verifica link specifici
        has_mailto = 'mailto:' in response
        has_tel = 'tel:' in response  
        has_web = 'https://' in response
        
        print(f"\n📊 ANALISI LINK:")
        print(f"   📧 Email link: {'✅' if has_mailto else '❌'}")
        print(f"   📞 Tel link: {'✅' if has_tel else '❌'}")
        print(f"   🌐 Web link: {'✅' if has_web else '❌'}")
        print(f"   📊 Totale link: {link_count}")
        
        # Valutazione successo
        success = link_count >= 2  # Almeno 2 link (email + tel minimo)
        print(f"\n🎯 RISULTATO: {'✅ SUCCESSO' if success else '⚠️ DA MIGLIORARE'}")
        
        if success:
            print("   Il sistema link funziona correttamente!")
            print(f"   Metrica has_links stimata: ~0.90+ (era 0.60)")
        else:
            print("   Controllare integrazione in ollama_llm.py")
        
        return success, link_count
        
    except Exception as e:
        print(f"❌ ERRORE: {e}")
        print("Verifica integrazione in ollama_llm.py")
        return False, 0

def test_categories():
    """Test link per diverse categorie"""
    
    print("\n🎯 TEST 3: Link per categorie")
    
    enhancer = LinkEnhancer()
    test_cases = [
        ("Come iscriversi agli esami?", "iscrizioni_esami"),
        ("Quanto costano le tasse?", "tasse_pagamenti"),
        ("Come richiedere un certificato?", "certificati_documenti"),
        ("Quali sono gli orari?", "orari_contatti")
    ]
    
    for question, category in test_cases:
        response_base = f"Risposta per: {question}"
        enhanced = enhancer.enhance_response(response_base, category)
        link_count = enhancer.count_links(enhanced)
        
        print(f"   {category}: {link_count} link")

if __name__ == "__main__":
    success, links = test_link_system()
    test_categories()
    
    print(f"\n🏆 RIASSUNTO:")
    print(f"   Sistema integrato: {'✅' if success else '❌'}")
    print(f"   Link generati: {links}")
    print(f"   Pronto per Step 4: {'✅' if success else '❌'}")