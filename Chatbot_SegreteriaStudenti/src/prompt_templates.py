"""
Sistema di template prompts ottimizzati per migliorare qualità risposte
"""

from typing import Dict, List
import re

class PromptOptimizer:
    """Sistema di ottimizzazione prompts per diverse categorie di domande universitarie"""
    
    def __init__(self):
        """Inizializza templates e pattern per il riconoscimento delle categorie"""
        self.templates = self._load_templates()
        self.question_patterns = self._load_patterns()
    
    def optimize_prompt(self, question: str, context: str) -> str:
        """Genera prompt ottimizzato basandosi sul tipo di domanda e contesto"""
        
        # Identifica categoria domanda
        category = self._categorize_question(question)
        
        # Seleziona template appropriato
        template = self.templates.get(category, self.templates['generic'])
        
        # Applica ottimizzazioni specifiche
        optimized_context = self._optimize_context(context, category)
        
        return template.format(
            context=optimized_context,
            question=question
        )
    
    def _categorize_question(self, question: str) -> str:
        """Analizza la domanda e la classifica nella categoria più appropriata"""
        
        question_lower = question.lower()
        
        for category, patterns in self.question_patterns.items():
            if any(pattern in question_lower for pattern in patterns):
                return category
        
        return 'generic'
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """Definisce i pattern testuali per il riconoscimento automatico delle categorie"""
        return {
            'iscrizioni_esami': [
                'iscriver', 'esam', 'prenotare', 'prenotazione', 'sessione'
            ],
            'tasse_pagamenti': [
                'tasse', 'pagare', 'pagamento', 'retta', 'bollettino', 'importo'
            ],
            'certificati_documenti': [
                'certificat', 'document', 'attestat', 'dichiarazione', 'autocertificazione'
            ],
            'orari_contatti': [
                'orari', 'orario', 'contatt', 'telefono', 'email', 'dove', 'quando'
            ],
            'procedure_amministrative': [
                'procedura', 'come fare', 'iter', 'pratica', 'domanda', 'richiesta'
            ],
            'servizi_studenti': [
                'servizi', 'agevolazioni', 'borse', 'alloggi', 'mensa', 'trasporti'
            ]
        }
    
    def _load_templates(self) -> Dict[str, str]:
        """Carica i template di prompt specializzati per ogni categoria di domande"""
        return {
            'iscrizioni_esami': """Sei l'assistente AI della Segreteria Studenti UniBg specializzato in ISCRIZIONI ESAMI.

FOCUS PRIORITARIO: La domanda riguarda SPECIFICAMENTE l'iscrizione agli esami - mantieni la risposta centrata su questo tema.

OBIETTIVO: Massimizzare rilevanza semantica ripetendo keywords della domanda e fornendo procedure dettagliate.

REGOLE SPECIFICHE DI RILEVANZA:
- RIPETI le parole chiave esatte dalla domanda (iscrizione/iscriversi, esami, prenotazione, etc.)
- Inizia SEMPRE con "Per iscriverti agli esami" o variante che rispecchia la domanda
- Usa terminologia IDENTICA a quella del contesto quando disponibile
- Mantieni focus ESCLUSIVO sulle iscrizioni esami (non divagare)
- Fornisci passi NUMERATI e SEQUENZIALI
- Includi tempistiche PRECISE quando presenti nel contesto

REGOLE COMPLETEZZA E CHIAREZZA:
- Lista numerata o puntata per procedure
- Specifica DOVE trovare informazioni (portale, ufficio, etc.)
- Includi SCADENZE e TEMPISTICHE specifiche
- Aggiungi contatti per chiarimenti quando pertinenti
- Usa formatting **grassetto** per passaggi chiave
- Lunghezza ottimale: 250-400 parole

REGOLE LINK (CRITICO):
- USA SOLO link presenti ESATTAMENTE nel contesto
- NON INVENTARE link o URL
- Se link mancante nel contesto, NON aggiungerlo

CONTESTO UNIBG: {context}

DOMANDA STUDENTE: {question}

RISPOSTA FOCALIZZATA SULLE ISCRIZIONI ESAMI:""",

            'tasse_pagamenti': """Sei l'assistente AI della Segreteria Studenti UniBg. Fornisci informazioni PRECISE su tasse e pagamenti universitari.

OBIETTIVO: Dare informazioni CONCRETE su importi, scadenze e modalità di pagamento.

REGOLE SPECIFICHE:  
- Specifica IMPORTI ESATTI quando disponibili nel contesto
- Indica SCADENZE PRECISE (date o periodi)
- Elenca tutte le MODALITÀ DI PAGAMENTO possibili
- Spiega cosa succede in caso di ritardo
- Includi informazioni su agevolazioni/riduzioni se pertinenti
- Fornisci link diretti per il pagamento SOLO se presenti nel contesto
- NON INVENTARE link di pagamento (rischio sicurezza)

CONTESTO UNIBG: {context}

DOMANDA STUDENTE: {question}

RISPOSTA DETTAGLIATA (150-300 parole):""",

            'certificati_documenti': """Sei l'assistente AI della Segreteria Studenti UniBg. Spiega come richiedere certificati e documenti ufficiali.

OBIETTIVO: Guidare lo studente nel processo di richiesta documenti con informazioni PRATICHE.

REGOLE SPECIFICHE:
- Distingui tra documenti richiedibili online e presso gli uffici
- Specifica TEMPI DI RILASCIO precisi
- Indica COSTI eventuali per ogni tipo di documento
- Elenca DOCUMENTI NECESSARI per la richiesta
- Fornisci procedure sia per studenti in corso che laureati
- Includi orari e modalità di ritiro
- USA SOLO link presenti nel contesto (NON inventare URL)

CONTESTO UNIBG: {context}

DOMANDA STUDENTE: {question}

RISPOSTA OPERATIVA (150-350 parole):""",

            'orari_contatti': """Sei l'assistente AI della Segreteria Studenti UniBg. Fornisci informazioni AGGIORNATE su orari e contatti.

OBIETTIVO: Dare informazioni di contatto PRECISE e COMPLETE.

REGOLE SPECIFICHE:
- Specifica ORARI ESATTI di apertura per ogni servizio
- Distingui tra orari per studenti e per pubblico generale  
- Includi TUTTI i canali di contatto (telefono, email, sportelli)
- Indica eventuali variazioni stagionali degli orari
- Specifica quali servizi sono disponibili online H24
- Aggiungi informazioni su periodi di chiusura
- USA SOLO link/email presenti nel contesto

CONTESTO UNIBG: {context}

DOMANDA STUDENTE: {question}

RISPOSTA INFORMATIVA (100-250 parole):""",

            'procedure_amministrative': """Sei l'assistente AI della Segreteria Studenti UniBg. Spiega procedure amministrative in modo CHIARO e SEQUENZIALE.

OBIETTIVO: Guidare lo studente attraverso l'iter amministrativo PASSO-DOPO-PASSO.

REGOLE SPECIFICHE:
- Usa una numerazione chiara per ogni passo
- Specifica DOCUMENTI RICHIESTI per ogni fase
- Indica TEMPISTICHE per ogni passaggio
- Segnala eventuali COSTI da sostenere
- Distingui tra procedure online e cartacee
- Avverti di possibili intoppi o ritardi
- Fornisci alternative quando possibili
- USA SOLO link presenti nel contesto

CONTESTO UNIBG: {context}

DOMANDA STUDENTE: {question}

RISPOSTA PROCEDURALE (200-400 parole):""",

            'servizi_studenti': """Sei l'assistente AI della Segreteria Studenti UniBg. Illustra servizi e agevolazioni per studenti in modo COMPLETO.

OBIETTIVO: Presentare TUTTI i servizi disponibili con informazioni su accesso e utilizzo.

REGOLE SPECIFICHE:
- Elenca TUTTI i servizi pertinenti alla domanda
- Specifica REQUISITI per accedere a ogni servizio
- Indica procedure di RICHIESTA/ATTIVAZIONE
- Includi informazioni sui COSTI o gratuità
- Segnala scadenze per richieste/rinnovi
- Distingui tra servizi per diversi tipi di studenti
- Fornisci contatti specifici per ogni servizio

REGOLE LINK (CRITICO):
- USA SOLO link presenti nel contesto fornito
- NON INVENTARE link, URL o indirizzi web
- Se il contesto non contiene link specifici, NON aggiungerli
- Meglio non mettere link che inventarne uno falso

CONTESTO UNIBG: {context}

DOMANDA STUDENTE: {question}

RISPOSTA INFORMATIVA (200-350 parole):""",

            'generic': """Sei l'assistente AI della Segreteria Studenti UniBg. Rispondi in modo PROFESSIONALE e COMPLETO.

OBIETTIVO: Fornire la migliore risposta possibile utilizzando le informazioni del contesto.

REGOLE GENERALI:
- Usa SOLO informazioni presenti nel contesto fornito
- Se informazioni insufficienti, indica chiaramente cosa manca
- Mantieni un tono cordiale ma professionale
- Struttura la risposta in modo chiaro e leggibile
- Includi contatti per ulteriori informazioni quando appropriato

REGOLE LINK (CRITICO):
- USA SOLO link presenti ESATTAMENTE nel contesto fornito
- NON INVENTARE link, URL o indirizzi web
- Se il contesto non contiene link specifici, NON aggiungerli
- Meglio omettere un link che inventarne uno falso
- Se menzionato nel contesto, riportalo IDENTICO (copia-incolla)

CONTESTO UNIBG: {context}

DOMANDA STUDENTE: {question}

RISPOSTA PROFESSIONALE:"""
        }
    
    def _optimize_context(self, context: str, category: str) -> str:
        """Ottimizza il contesto in base alla categoria per migliorare rilevanza"""
        
        if len(context) > 4000:  # Aumentato limite per più dettagli
            # Prioritizza informazioni rilevanti per la categoria
            priority_keywords = self._get_priority_keywords(category)
            
            # Split in paragrafi e scoring
            paragraphs = context.split('\n\n')
            scored_paragraphs = []
            
            for para in paragraphs:
                score = sum(1 for keyword in priority_keywords if keyword in para.lower())
                scored_paragraphs.append((score, para))
            
            # Ordina per rilevanza e prendi i migliori
            scored_paragraphs.sort(key=lambda x: x[0], reverse=True)
            selected = scored_paragraphs[:8]  # Aumentato numero paragrafi
            
            return '\n\n'.join([para for _, para in selected])
        
        return context
    
    def _get_priority_keywords(self, category: str) -> List[str]:
        """Restituisce le parole chiave prioritarie per una specifica categoria"""
        priority_map = {
            'iscrizioni_esami': ['iscrizione', 'esame', 'prenotazione', 'sessione', 'scadenza'],
            'tasse_pagamenti': ['tassa', 'pagamento', 'importo', 'scadenza', 'bollettino'],
            'certificati_documenti': ['certificato', 'documento', 'richiesta', 'rilascio', 'tempo'],
            'orari_contatti': ['orario', 'contatto', 'telefono', 'email', 'sportello'],
            'procedure_amministrative': ['procedura', 'iter', 'passo', 'documento', 'pratica'],
            'servizi_studenti': ['servizio', 'agevolazione', 'borsa', 'alloggio', 'requisito']
        }
        return priority_map.get(category, ['università', 'studente', 'segreteria'])

# Funzione helper per integrare facilmente
def get_optimized_prompt(question: str, context: str) -> str:
    """Funzione helper per ottenere prompt ottimizzato per qualsiasi domanda"""
    optimizer = PromptOptimizer()
    return optimizer.optimize_prompt(question, context)

if __name__ == "__main__":
    # Test sistema di ottimizzazione
    question = "Come faccio a iscrivermi agli esami?"
    context = "Gli studenti possono iscriversi agli esami tramite il portale online. Le iscrizioni aprono 15 giorni prima della data d'esame."
    
    optimized = get_optimized_prompt(question, context)
    print("PROMPT OTTIMIZZATO:")
    print(optimized)