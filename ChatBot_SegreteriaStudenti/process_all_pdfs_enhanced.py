#!/usr/bin/env python3
"""
Script per processare tutti i PDF con l'estrattore potenziato
"""
import os
import sys
from pathlib import Path

# Aggiungi src al path
sys.path.append(str(Path(__file__).parent / 'src'))

from enhanced_link_extractor import EnhancedLinkExtractor

def main():
    """
    Processa tutti i PDF con link potenziati
    """
    extractor = EnhancedLinkExtractor()
    
    # Directory dei PDF
    pdf_dir = "data/guida_dello_studente"
    output_dir = "extracted_text"
    
    # Crea directory di output se non exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista dei PDF da processare
    pdf_files = [
        "futuri_studenti.pdf",
        "guide_2025-2026.pdf", 
        "laureati.pdf",
        "studenti.pdf"
    ]
    
    print("🚀 PROCESSAMENTO PDF CON LINK POTENZIATI")
    print("=" * 60)
    
    total_links = 0
    processed_files = []
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        
        if not os.path.exists(pdf_path):
            print(f"❌ File non trovato: {pdf_path}")
            continue
        
        # Nome file di output
        base_name = pdf_file.replace('.pdf', '')
        output_path = os.path.join(output_dir, f"{base_name}_enhanced.txt")
        
        print(f"\n📖 ELABORAZIONE: {pdf_file}")
        print("-" * 40)
        
        try:
            link_count = extractor.create_enhanced_text(pdf_path, output_path)
            total_links += link_count
            processed_files.append({
                'file': pdf_file,
                'output': f"{base_name}_enhanced.txt",
                'links': link_count
            })
            
            print(f"✅ Completato: {link_count} link estratti")
            
        except Exception as e:
            print(f"❌ Errore durante l'elaborazione di {pdf_file}: {e}")
    
    # Riepilogo finale
    print("\n" + "=" * 60)
    print("📊 RIEPILOGO FINALE:")
    print(f"   PDF processati: {len(processed_files)}/{len(pdf_files)}")
    print(f"   Link totali estratti: {total_links}")
    print(f"   File potenziati creati: {len(processed_files)}")
    
    print(f"\n📁 FILE ESTRATTI POTENZIATI:")
    for file_info in processed_files:
        print(f"   ✅ {file_info['output']} ({file_info['links']} link)")
    
    return processed_files

if __name__ == "__main__":
    main()
