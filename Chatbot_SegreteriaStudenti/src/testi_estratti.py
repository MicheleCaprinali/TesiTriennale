import fitz  # PyMuPDF
import os

def pdf_to_txt_with_inline_links(pdf_path, txt_path):
    """Estrae testo da PDF preservando i link come annotazioni inline"""
    doc = fitz.open(pdf_path)
    output_lines = []

    for page_num, page in enumerate(doc, start=1):
        words = page.get_text("words")
        words.sort(key=lambda w: (round(w[1], 1), w[0]))  # ordina: y (approssimato), poi x

        links = page.get_links()
        link_map = []
        for l in links:
            if "uri" in l:
                rect = fitz.Rect(l["from"])
                link_map.append((rect, l["uri"]))

        line_text = []
        buffer_word = []
        buffer_link = None
        current_y = None

        def flush_buffer(force_newline=False):
            """Svuota il buffer delle parole accumulando testo e link"""
            nonlocal buffer_word, buffer_link, line_text, output_lines
            if buffer_word:
                phrase = " ".join(buffer_word)
                if buffer_link:
                    line_text.append(f"{phrase} ({buffer_link})")
                else:
                    line_text.append(phrase)
            buffer_word = []
            buffer_link = None
            if force_newline and line_text:
                output_lines.append(" ".join(line_text))
                line_text = []

        for w in words:
            x0, y0, x1, y1, word, *_ = w

            link_found = None
            for rect, uri in link_map:
                if rect.intersects(fitz.Rect(x0, y0, x1, y1)):
                    link_found = uri
                    break

            if current_y is None:
                current_y = y0
            elif abs(y0 - current_y) > 5:  # cambio riga
                if buffer_link and buffer_link == link_found:
                    current_y = y0
                else:
                    flush_buffer(force_newline=True)
                    current_y = y0

            if buffer_link == link_found:
                buffer_word.append(word)
            else:
                flush_buffer()
                buffer_word = [word]
                buffer_link = link_found

        flush_buffer()
        if line_text:
            output_lines.append(" ".join(line_text))

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"Conversione completata: {txt_path}")


if __name__ == "__main__":
    """Script principale per processare tutti i PDF nella cartella guida_dello_studente"""
    # ✅ FIX: Usa percorsi assoluti basati sulla posizione dello script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(BASE_DIR, "../data/guida_dello_studente")
    output_folder = os.path.join(BASE_DIR, "../data/testi_estratti")

    os.makedirs(output_folder, exist_ok=True)
    
    print(f"ESTRAZIONE TESTI DA PDF")
    print("=" * 50)
    print(f"Input: {os.path.abspath(input_folder)}")
    print(f"Output: {os.path.abspath(output_folder)}")
    print()

    if not os.path.exists(input_folder):
        print(f"[ERRORE] Cartella {input_folder} non trovata!")
        exit(1)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print(f"[WARN] Nessun file PDF trovato in {input_folder}")
        exit(0)
    
    print(f"Trovati {len(pdf_files)} file PDF da processare\n")

    for filename in pdf_files:
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_extracted.txt"
        output_path = os.path.join(output_folder, output_filename)

        print(f"Processando: {filename}...")
        try:
            pdf_to_txt_with_inline_links(input_path, output_path)
            print(f"  ✓ Completato: {output_filename}\n")
        except Exception as e:
            print(f"  ✗ Errore: {e}\n")
    
    print("=" * 50)
    print(f"ESTRAZIONE COMPLETATA")
    print(f"File processati: {len(pdf_files)}")
