"""
Sistema Link Enhancement SICURO - Solo formattazione e contatti generici
VERSIONE CORRETTA - Fix problemi link malformati
"""

import re
from typing import Dict, List

class LinkEnhancer:
    """Sistema sicuro per migliorare formattazione e aggiungere contatti"""
    
    def __init__(self):
        # SOLO contatti generici sicuri
        self.safe_contacts = {
            'email_segreteria': 'segreteria.studenti@unibg.it',
            'telefono_generale': '0352052620',
            'sito_base': 'https://helpdesk.unibg.it'
        }
        
        # Pattern per migliorare formattazione (senza link esterni)
        self.formatting_patterns = {
            'email': r'([a-zA-Z0-9._%+-]+@unibg\.it)',
            'telefono': r'(\b0?35\s?205\s?26\d{2}\b)',  # Pattern più specifico per UniBg
            'sito_web': r'(www\.unibg\.it)'
        }
    
    def enhance_response(self, response: str, category: str = None) -> str:
        """Migliora formattazione senza aggiungere link esterni non verificati"""
        
        enhanced_response = response
        
        # FASE 0: Pulizia preventiva link malformati
        enhanced_response = self._clean_malformed_links(enhanced_response)
        
        # FASE 1: Migliora formattazione contatti esistenti
        enhanced_response = self._enhance_contact_formatting(enhanced_response)
        
        # FASE 2: Aggiungi sezione contatti solo se mancante
        enhanced_response = self._add_contact_section_if_missing(enhanced_response, category)
        
        return enhanced_response
    
    def _clean_malformed_links(self, text: str) -> str:
        """Pulisce link già malformati prima di processare"""
        
        # Fix pattern comuni di link corrotti
        # Rimuovi parentesi e punti extra dai link
        text = re.sub(r'(https?://[^\s\)]+)\)([^\s]*)-\.', r'\1\2', text)  # parentesi + punto extra
        text = re.sub(r'(https?://[^\s]+)-\.$', r'\1', text)  # punto extra finale
        text = re.sub(r'(https?://[^\s]+)\)-', r'\1', text)  # parentesi + dash
        text = re.sub(r'(https?://[^\s]+)>\.$', r'\1', text)  # > + punto finale
        
        # Fix URL con caratteri extra
        text = re.sub(r'(https?://[a-zA-Z0-9\./\-]+)[\)\.\-]+$', r'\1', text, flags=re.MULTILINE)
        
        return text
    
    def _enhance_contact_formatting(self, text: str) -> str:
        """Migliora formattazione di email, telefoni e siti esistenti"""
        
        # Formatta email come link mailto (EVITA doppia formattazione)
        if 'mailto:' not in text:
            text = re.sub(
                self.formatting_patterns['email'], 
                r'[\1](mailto:\1)', 
                text
            )
        
        # Formatta telefoni come link tel (MANTIENI spazi nel testo visibile)
        def replace_phone(match):
            phone_display = match.group(1)  # Numero con spazi per visualizzazione
            phone_clean = re.sub(r'\s+', '', phone_display)  # Numero pulito per tel:
            # Assicurati che inizi con 0352052
            if not phone_clean.startswith('035'):
                phone_clean = '035' + phone_clean.lstrip('0')
            return f'[{phone_display}](tel:+39{phone_clean})'
        
        # Solo se non ci sono già link tel:
        if 'tel:' not in text:
            text = re.sub(
                self.formatting_patterns['telefono'], 
                replace_phone,
                text
            )
        
        # Formatta sito come link web (EVITA doppia formattazione)
        if '[www.unibg.it]' not in text and 'https://www.unibg.it' not in text:
            text = re.sub(
                r'(^|[^\[\(])(www\.unibg\.it)([^\]\)]*)', 
                r'\1[\2](https://\2)', 
                text
            )
        
        return text
    
    def _add_contact_section_if_missing(self, text: str, category: str) -> str:
        """Aggiunge sezione contatti SOLO se mancante completamente"""
        
        # Controlla se ci sono già contatti nella risposta
        has_contacts = any([
            'email' in text.lower(),
            'telefono' in text.lower(), 
            'contatt' in text.lower(),
            '@' in text,
            '035' in text,
            'segreteria' in text.lower(),
            'dipartimento' in text.lower()
        ])
        
        # Se non ci sono contatti, aggiungi footer minimal
        if not has_contacts and category:
            footer = self._get_minimal_footer(category)
            text += "\n\n" + footer
        
        return text
    
    def _get_minimal_footer(self, category: str) -> str:
        """Footer minimale con SOLO contatti verificati"""
        
        # Footer specifico per categoria
        category_footers = {
            'iscrizioni_esami': """📞 **Per supporto iscrizioni:**
- **Email**: [segreteria.studenti@unibg.it](mailto:segreteria.studenti@unibg.it)
- **Telefono**: [035 205 2620](tel:+390352052620)""",
            
            'tasse_pagamenti': """💰 **Per informazioni su tasse:**
- **Email**: [segreteria.studenti@unibg.it](mailto:segreteria.studenti@unibg.it)  
- **Telefono**: [035 205 2620](tel:+390352052620)""",
            
            'certificati_documenti': """📄 **Per richieste certificati:**
- **Email**: [segreteria.studenti@unibg.it](mailto:segreteria.studenti@unibg.it)
- **Telefono**: [035 205 2620](tel:+390352052620)""",
            
            'orari_contatti': """🕒 **Contatti segreteria:**
- **Email**: [segreteria.studenti@unibg.it](mailto:segreteria.studenti@unibg.it)
- **Telefono**: [035 205 2620](tel:+390352052620)""",
            
            'servizi_studenti': """🎓 **Per servizi studenti:**
- **Email**: [segreteria.studenti@unibg.it](mailto:segreteria.studenti@unibg.it)
- **Telefono**: [035 205 2620](tel:+390352052620)""",
            
            'generic': """📞 **Per informazioni:**
- **Email**: [segreteria.studenti@unibg.it](mailto:segreteria.studenti@unibg.it)
- **Telefono**: [035 205 2620](tel:+390352052620)
- **Sito**: [www.unibg.it](https://www.unibg.it)"""
        }
        
        return category_footers.get(category, category_footers['generic'])
    
    def count_links(self, text: str) -> int:
        """Conta tutti i tipi di link nel testo"""
        
        # Link markdown [testo](url)
        markdown_links = len(re.findall(r'\[.*?\]\([^)]+\)', text))
        
        # Link diretti http/https (non già in markdown)
        http_pattern = r'https?://[^\s\)\]]+(?![^\[]*\])'
        http_links = len(re.findall(http_pattern, text))
        
        # Link email mailto: (già contati nei markdown)
        # Link telefono tel: (già contati nei markdown)
        
        # Evita doppio conteggio
        total = markdown_links + http_links
        
        return total
    
    def get_enhancement_stats(self, original: str, enhanced: str) -> dict:
        """Statistiche del miglioramento"""
        
        return {
            'original_links': self.count_links(original),
            'enhanced_links': self.count_links(enhanced),
            'links_added': self.count_links(enhanced) - self.count_links(original),
            'has_footer_added': len(enhanced) > len(original) + 50,
            'formatting_improved': '[' in enhanced and '[' not in original,
            'emails_formatted': enhanced.count('mailto:') - original.count('mailto:'),
            'phones_formatted': enhanced.count('tel:') - original.count('tel:'),
            'malformed_links_fixed': self._count_malformed_patterns(original) - self._count_malformed_patterns(enhanced)
        }
    
    def _count_malformed_patterns(self, text: str) -> int:
        """Conta pattern di link malformati"""
        
        patterns = [
            r'https?://[^\s]+\)-\.',  # link con parentesi + punto
            r'https?://[^\s]+>\.$',   # link con > + punto
            r'https?://[^\s]+\)$',    # link con parentesi finale sospetta
        ]
        
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, text))
        
        return count
    
    def validate_links(self, text: str) -> dict:
        """Valida la qualità dei link nel testo"""
        
        # Trova tutti i link
        all_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
        
        validation_results = {
            'total_links': len(all_links),
            'valid_links': 0,
            'email_links': 0,
            'phone_links': 0,
            'web_links': 0,
            'malformed_links': 0
        }
        
        for link_text, link_url in all_links:
            if link_url.startswith('mailto:'):
                validation_results['email_links'] += 1
                validation_results['valid_links'] += 1
            elif link_url.startswith('tel:'):
                validation_results['phone_links'] += 1
                validation_results['valid_links'] += 1
            elif link_url.startswith('http'):
                validation_results['web_links'] += 1
                validation_results['valid_links'] += 1
            else:
                validation_results['malformed_links'] += 1
        
        return validation_results

if __name__ == "__main__":
    # Test sistema corretto
    enhancer = LinkEnhancer()
    
    test_cases = [
        "Contatta la segreteria al numero 035 205 2620",
        "Per informazioni scrivi a segreteria.studenti@unibg.it",
        "Visita il sito www.unibg.it per maggiori dettagli", 
        "Link malformato: https://www.unibg.it)-.",  # Test correzione
        "Per iscriverti agli esami segui la procedura online"  # Senza contatti
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}:")
        print(f"ORIGINALE: {test}")
        
        enhanced = enhancer.enhance_response(test, 'iscrizioni_esami')
        print(f"MIGLIORATO: {enhanced}")
        
        stats = enhancer.get_enhancement_stats(test, enhanced)
        print(f"STATS: {stats}")
        
        # Test validazione link
        validation = enhancer.validate_links(enhanced)
        print(f"VALIDAZIONE: {validation}")