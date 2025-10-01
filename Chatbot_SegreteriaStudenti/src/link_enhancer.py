import re
from typing import Dict, List

class LinkEnhancer:
    """Sistema per migliorare formattazione link e aggiungere contatti istituzionali"""
    
    def __init__(self):
        """Inizializza contatti istituzionali sicuri e pattern di formattazione"""
        # SOLO contatti generici sicuri
        self.safe_contacts = {
            'email_segreteria': 'segreteria.studenti@unibg.it',
            'telefono_generale': '0352052620',
            'sito_base': 'https://helpdesk.unibg.it'
        }
        
        # Pattern per migliorare formattazione (senza link esterni)
        self.formatting_patterns = {
            'email': r'([a-zA-Z0-9._%+-]+@unibg\.it)',
            'telefono': r'(\b0?35\s?205\s?26\d{2}\b)',
            'sito_web': r'(www\.unibg\.it)'
        }
    
    def enhance_response(self, response: str, category: str = None) -> str:
        """Migliora formattazione della risposta senza aggiungere link non verificati"""
        enhanced_response = response
        
        # Migliora formattazione contatti esistenti
        enhanced_response = self._enhance_contact_formatting(enhanced_response)
        
        # Aggiungi sezione contatti solo se mancante
        enhanced_response = self._add_contact_section_if_missing(enhanced_response, category)
        
        return enhanced_response
    
    def _enhance_contact_formatting(self, text: str) -> str:
        """Formatta email, telefoni e siti web esistenti come link cliccabili"""
        # Formatta email come link mailto
        if 'mailto:' not in text:
            text = re.sub(
                self.formatting_patterns['email'], 
                r'[\1](mailto:\1)', 
                text
            )
        
        # Formatta telefoni come link tel
        def replace_phone(match):
            phone_display = match.group(1)
            phone_clean = re.sub(r'\s+', '', phone_display)
            if not phone_clean.startswith('035'):
                phone_clean = '035' + phone_clean.lstrip('0')
            return f'[{phone_display}](tel:+39{phone_clean})'
        
        if 'tel:' not in text:
            text = re.sub(
                self.formatting_patterns['telefono'], 
                replace_phone,
                text
            )
        
        # Formatta sito come link web
        if '[www.unibg.it]' not in text and 'https://www.unibg.it' not in text:
            text = re.sub(
                r'(^|[^\[\(])(www\.unibg\.it)([^\]\)]*)', 
                r'\1[\2](https://\2)', 
                text
            )
        
        return text
    
    def _add_contact_section_if_missing(self, text: str, category: str) -> str:
        """Aggiunge footer con contatti solo se la risposta ne è completamente priva"""
        # Controlla se ci sono già contatti nella risposta
        has_contacts = any([
            'email' in text.lower(),
            'telefono' in text.lower(), 
            'contatt' in text.lower(),
            '@' in text,
            '035' in text,
            'segreteria' in text.lower()
        ])
        
        # Se non ci sono contatti, aggiungi footer minimal
        if not has_contacts and category:
            footer = self._get_minimal_footer(category)
            text += "\n\n" + footer
        
        return text
    
    def _get_minimal_footer(self, category: str) -> str:
        """Genera footer con contatti istituzionali appropriati per la categoria"""
        category_footers = {
            'iscrizioni_esami': """Per supporto iscrizioni:
- Segreteria: https://helpdesk.unibg.it
- Telefono: +390352052620""",
            
            'tasse_pagamenti': """Per informazioni su tasse:
- Segreteria: https://helpdesk.unibg.it
- Telefono: +390352052620""",

            'certificati_documenti': """Per richieste certificati:
- Segreteria: https://helpdesk.unibg.it
- Telefono: +390352052620""",

            'generic': """Per informazioni:
- Segreteria: https://helpdesk.unibg.it
- Telefono: +390352052620
- Sito: www.unibg.it"""
        }
        
        return category_footers.get(category, category_footers['generic'])
    
    def count_links(self, text: str) -> int:
        """Conta il numero totale di link presenti nel testo"""
        markdown_links = len(re.findall(r'\[.*?\]\([^)]+\)', text))
        http_pattern = r'https?://[^\s\)\]]+(?![^\[]*\])'
        http_links = len(re.findall(http_pattern, text))
        return markdown_links + http_links
    
    def get_enhancement_stats(self, original: str, enhanced: str) -> dict:
        """Calcola statistiche sui miglioramenti applicati al testo"""
        return {
            'original_links': self.count_links(original),
            'enhanced_links': self.count_links(enhanced),
            'links_added': self.count_links(enhanced) - self.count_links(original),
            'has_footer_added': len(enhanced) > len(original) + 50,
            'formatting_improved': '[' in enhanced and '[' not in original
        }


if __name__ == "__main__":
    # Test del sistema
    enhancer = LinkEnhancer()
    
    test_cases = [
        "Contatta la segreteria al numero 035 205 2620",
        "Per informazioni scrivi a segreteria.studenti@unibg.it",
        "Visita il sito www.unibg.it per maggiori dettagli",
        "Per iscriverti agli esami segui la procedura online"
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTEST {i}:")
        print(f"ORIGINALE: {test}")
        
        enhanced = enhancer.enhance_response(test, 'iscrizioni_esami')
        print(f"MIGLIORATO: {enhanced}")
        
        stats = enhancer.get_enhancement_stats(test, enhanced)
        print(f"STATS: {stats}")