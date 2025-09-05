import fitz
import re
import os
from typing import List, Dict, Any

class EnhancedLinkExtractor:
    """
    Estrattore di link migliorato che cattura:
    1. Link standard
    2. Annotazioni con link ipertestuali
    3. URL nel testo
    4. Pattern specifici UniBG
    """
    
    def __init__(self):
        self.url_patterns = [
            r'https?://[^\s\)\],]+',
            r'www\.[^\s\)\],]+',
            r'[a-zA-Z0-9.-]+\.unibg\.it[^\s\)\],]*'
        ]
        
        self.unibg_text_patterns = [
            # Pattern per testi che spesso contengono link
            (r'Help Desk [Ss]tudenti?', r'https://helpdesk.unibg.it/helpdesksegrestud/'),
            (r'[Rr]eperibilità telefonica del Servizio [Ss]tudenti', r'https://www.unibg.it/node/6946'),
            (r'[Pp]renotando un appuntamento', r'https://logistica.unibg.it/PortalePlanning/UNIBG-servizi'),
            (r'SOS Matricole', r'https://www.unibg.it/studiare/ti-aiutiamo/servizio-orientamento/sos-matricole'),
            (r'[Ss]portello internet', r'http://www.unibg.it/node/6977'),
            (r'[Cc]ontribuzione studentesca', r'https://www.unibg.it/studiare/iscriversi/tasse-e-agevolazioni/contribuzione-studentesca'),
        ]
    
    def extract_hyperlink_annotations(self, page):
        """
        Estrae le annotazioni ipertestuali dalla pagina
        """
        hyperlinks = []
        
        # Metodo 1: Link diretti
        links = page.get_links()
        for link in links:
            if 'uri' in link and link['uri']:
                try:
                    rect = link.get('rect', [0,0,0,0])
                    if rect and len(rect) == 4:
                        rect_obj = fitz.Rect(rect)
                        # Ottieni il testo nella zona del link
                        link_text = page.get_textbox(rect_obj).strip()
                        
                        # Se non c'è testo, cerca nelle vicinanze
                        if not link_text:
                            # Espandi leggermente l'area
                            expanded_rect = fitz.Rect(
                                rect[0] - 5, rect[1] - 2, 
                                rect[2] + 5, rect[3] + 2
                            )
                            link_text = page.get_textbox(expanded_rect).strip()
                        
                        if not link_text:
                            link_text = "Link"
                        
                        hyperlinks.append({
                            'method': 'hyperlink_annotation',
                            'text': link_text,
                            'url': link['uri'],
                            'rect': rect
                        })
                except Exception as e:
                    print(f"   ⚠️ Errore estrazione hyperlink: {e}")
        
        # Metodo 2: Annotazioni
        try:
            for annot in page.annots():
                if annot.type[0] == 2:  # Link annotation
                    uri = annot.uri
                    if uri:
                        rect = annot.rect
                        link_text = page.get_textbox(rect).strip()
                        
                        if not link_text:
                            link_text = "Link"
                            
                        hyperlinks.append({
                            'method': 'annotation',
                            'text': link_text,
                            'url': uri,
                            'rect': [rect.x0, rect.y0, rect.x1, rect.y1]
                        })
        except Exception as e:
            print(f"   ⚠️ Errore annotazioni: {e}")
        
        return hyperlinks
    
    def find_text_patterns(self, text, page_num):
        """
        Trova pattern di testo che potrebbero essere link
        """
        found_patterns = []
        
        # Pattern UniBG specifici
        for pattern_text, url in self.unibg_text_patterns:
            matches = re.finditer(pattern_text, text, re.IGNORECASE)
            for match in matches:
                found_patterns.append({
                    'method': 'text_pattern',
                    'text': match.group(),
                    'url': url,
                    'position': match.start()
                })
        
        return found_patterns
    
    def find_url_in_text(self, text, page_num):
        """
        Trova URL espliciti nel testo
        """
        found_urls = []
        
        for pattern in self.url_patterns:
            urls = re.finditer(pattern, text, re.IGNORECASE)
            for match in urls:
                url = match.group()
                # Trova il contesto
                start_pos = max(0, match.start() - 50)
                end_pos = min(len(text), match.end() + 20)
                context = text[start_pos:match.start()].strip()
                
                # Trova le ultime parole significative
                words = context.split()
                if words:
                    link_text = ' '.join(words[-4:])
                else:
                    link_text = "URL"
                
                found_urls.append({
                    'method': 'url_in_text',
                    'text': link_text,
                    'url': url,
                    'position': match.start()
                })
        
        return found_urls
    
    def extract_all_links(self, pdf_path: str):
        """
        Estrae tutti i link usando tutti i metodi
        """
        print(f"\n🔗 ESTRAZIONE LINK POTENZIATA: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        all_links = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            print(f"\n📄 PAGINA {page_num + 1}:")
            
            # 1. Link ipertestuali
            hyperlinks = self.extract_hyperlink_annotations(page)
            for link in hyperlinks:
                link['page'] = page_num + 1
                all_links.append(link)
                print(f"   🔗 Hyperlink: '{link['text']}' → {link['url']}")
            
            # 2. Pattern di testo
            text_patterns = self.find_text_patterns(text, page_num)
            for pattern in text_patterns:
                pattern['page'] = page_num + 1
                all_links.append(pattern)
                print(f"   📝 Pattern: '{pattern['text']}' → {pattern['url']}")
            
            # 3. URL nel testo
            url_matches = self.find_url_in_text(text, page_num)
            for url_match in url_matches:
                url_match['page'] = page_num + 1
                all_links.append(url_match)
                print(f"   🌐 URL: '{url_match['text']}' → {url_match['url']}")
        
        doc.close()
        
        # Rimuovi duplicati mantenendo l'ordine
        unique_links = []
        seen_urls = set()
        
        for link in all_links:
            url_text_combo = f"{link['url']}|{link['text']}"
            if url_text_combo not in seen_urls:
                seen_urls.add(url_text_combo)
                unique_links.append(link)
        
        print(f"\n📊 TOTALE LINK UNICI: {len(unique_links)}")
        return unique_links
    
    def create_enhanced_text(self, pdf_path: str, output_path: str):
        """
        Crea il testo con i link integrati nel contesto corretto
        """
        print(f"\n📝 CREAZIONE TESTO POTENZIATO: {pdf_path}")
        
        # Estrai tutti i link
        all_links = self.extract_all_links(pdf_path)
        
        # Organizza i link per pagina
        links_by_page = {}
        for link in all_links:
            page_num = link['page']
            if page_num not in links_by_page:
                links_by_page[page_num] = []
            links_by_page[page_num].append(link)
        
        # Processa il documento
        doc = fitz.open(pdf_path)
        final_text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            final_text += f"\n\n=== PAGINA {page_num + 1} ===\n\n"
            
            # Se ci sono link per questa pagina, processali
            if (page_num + 1) in links_by_page:
                page_links = links_by_page[page_num + 1]
                
                # Sostituisci il testo con le versioni linkate
                modified_text = text
                
                # Ordina i link per posizione (se disponibile)
                page_links.sort(key=lambda x: x.get('position', 0))
                
                for link in page_links:
                    link_text = link['text']
                    link_url = link['url']
                    
                    # Sostituisci solo se il testo è abbastanza specifico
                    if len(link_text) > 3 and link_text != "Link":
                        # Pattern più preciso per la sostituzione
                        pattern = re.escape(link_text)
                        replacement = f"{link_text} ({link_url})"
                        
                        # Sostituisci solo la prima occorrenza per evitare sostituzioni multiple
                        modified_text = re.sub(pattern, replacement, modified_text, count=1, flags=re.IGNORECASE)
                
                final_text += modified_text
            else:
                final_text += text
        
        doc.close()
        
        # Salva il file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_text)
        
        print(f"✅ File salvato: {output_path}")
        
        return len(all_links)

if __name__ == "__main__":
    extractor = EnhancedLinkExtractor()
    
    # Test con un PDF
    pdf_file = "data/guida_dello_studente/futuri_studenti.pdf"
    if os.path.exists(pdf_file):
        output_file = "extracted_text/futuri_studenti_enhanced.txt"
        link_count = extractor.create_enhanced_text(pdf_file, output_file)
        print(f"🎉 Completato! {link_count} link estratti")
    else:
        print(f"❌ File non trovato: {pdf_file}")
