#!/usr/bin/env python3
"""
Script per generare dataset di test completo per la tesi
"""

import json
import random
import time
from datetime import datetime, timedelta

# Dataset di domande realistiche per studenti UniBG
REALISTIC_QUERIES = [
    # Iscrizioni ed esami
    "Come faccio a iscrivermi agli esami di gennaio?",
    "Quando apre la sessione di esami straordinaria?", 
    "Posso iscrivermi a un esame se ho ancora un debito?",
    "Come cambio data di un esame già prenotato?",
    
    # Tasse e pagamenti
    "Quando devo pagare la seconda rata delle tasse?",
    "Come richiedo l'esonero per reddito delle tasse universitarie?",
    "Cosa succede se pago le tasse in ritardo?",
    "Come ottengo la ricevuta di pagamento delle tasse?",
    
    # Lauree e certificati
    "Quando posso prenotarmi per la sessione di laurea?",
    "Che documenti servono per iscriversi alla laurea?",
    "Come richiedo un certificato di laurea con voti?",
    "Quanto tempo ci vuole per avere la pergamena?",
    
    # Servizi studenti
    "Come funziona il servizio di orientamento?",
    "Dove trovo informazioni sui tirocini curricolari?",
    "Come richiedo supporto per studenti con DSA?",
    "Quali agevolazioni ci sono per studenti fuori sede?",
    
    # Contatti e orari
    "Quali sono gli orari della segreteria studenti?",
    "Come posso contattare la segreteria via email?",
    "Dove si trova l'ufficio tasse e contributi?",
    "Posso prenotare un appuntamento con la segreteria?",
    
    # Domande specifiche/personali (dovrebbero fare redirect)
    "Perché non riesco ad accedere al mio sportello studenti?",
    "Il mio piano di studi è stato approvato?",
    "Quando riceverò l'esito della mia domanda di borsa di studio?",
    "Posso vedere il mio libretto universitario aggiornato?",
    
    # Domande generiche
    "Come funziona l'università?",
    "Che corsi ci sono a ingegneria?",
    "Dove parcheggio in università?",
    "C'è una mensa universitaria?"
]

def generate_test_dataset(num_queries=50):
    """Genera dataset di test per evaluation"""
    dataset = []
    
    for i in range(num_queries):
        query = random.choice(REALISTIC_QUERIES)
        
        # Simula timestamp random negli ultimi 30 giorni
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago)
        
        # Categorizza la query
        category = categorize_query(query)
        
        # Determina se dovrebbe fare redirect
        should_redirect = is_personal_query(query)
        
        dataset.append({
            'id': i + 1,
            'timestamp': timestamp.isoformat(),
            'query': query,
            'category': category,
            'expected_redirect': should_redirect,
            'priority': 'high' if should_redirect else 'normal'
        })
    
    return dataset

def categorize_query(query):
    """Categorizza una query"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['esami', 'iscriv', 'prenotare', 'sessione']):
        return 'esami'
    elif any(word in query_lower for word in ['tasse', 'pagament', 'contribut', 'rata']):
        return 'tasse'
    elif any(word in query_lower for word in ['laurea', 'certificat', 'pergamen', 'diploma']):
        return 'lauree'
    elif any(word in query_lower for word in ['segreteria', 'contatt', 'orari', 'ufficio']):
        return 'contatti'
    elif any(word in query_lower for word in ['tirocini', 'orientamento', 'dsa', 'disabilit']):
        return 'servizi'
    else:
        return 'generale'

def is_personal_query(query):
    """Determina se una query richiede dati personali"""
    personal_indicators = [
        'mio', 'mia', 'miei', 'mie', 'non riesco', 'perché non',
        'quando riceverò', 'il mio', 'la mia', 'posso vedere'
    ]
    
    query_lower = query.lower()
    return any(indicator in query_lower for indicator in personal_indicators)

def save_dataset(dataset, filename="test_dataset.json"):
    """Salva il dataset in JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_queries': len(dataset),
                'categories': list(set(item['category'] for item in dataset)),
                'description': 'Dataset di test per ChatBot RAG UniBG'
            },
            'queries': dataset
        }, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Dataset salvato in: {filename}")
    print(f"📊 {len(dataset)} query generate")
    
    # Statistiche
    categories = {}
    redirect_count = 0
    
    for item in dataset:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1
        if item['expected_redirect']:
            redirect_count += 1
    
    print(f"📈 Statistiche:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}")
    print(f"🎫 Query che dovrebbero fare redirect: {redirect_count}")

if __name__ == "__main__":
    print("🧪 Generazione Dataset di Test per Tesi")
    print("=" * 50)
    
    # Genera dataset
    dataset = generate_test_dataset(100)
    save_dataset(dataset)
    
    print("\n💡 Usa questo dataset per:")
    print("  1. Testing automatico del chatbot")
    print("  2. Metriche per la tesi")
    print("  3. Evaluation della performance")
    print("  4. Analisi del comportamento utente")
