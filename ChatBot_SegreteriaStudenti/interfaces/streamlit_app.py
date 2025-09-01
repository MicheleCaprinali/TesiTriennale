import streamlit as st
import sys
import os
import re

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import setup_chatbot
import time

# Configurazione pagina
st.set_page_config(
    page_title="ChatBot UniBg",
    page_icon="🎓",
    layout="wide"
)

# CSS personalizzato con stili migliorati per i link
st.markdown("""
<style>
/* Theme scuro generale */
.stApp {
    background-color: #1a1a1a;
}
.main-header {
    text-align: center;
    color: #4fc3f7;
    border-bottom: 2px solid #1f4e79;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.8rem;
    margin-bottom: 1rem;
    display: flex;
    border: 1px solid #444;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.chat-message.user {
    background-color: #1e3a5f;
    color: #ffffff;
    border-left: 4px solid #4fc3f7;
}
.chat-message.bot {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border-left: 4px solid #4caf50;
}
.chat-message .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background-color: #333333;
    border: 2px solid #555;
}
.chat-message .content {
    flex: 1;
    line-height: 1.6;
    font-size: 1rem;
}
/* Stili migliorati per i link cliccabili */
.chat-message .content a {
    color: #4fc3f7 !important;
    text-decoration: underline !important;
    transition: all 0.3s ease;
    font-weight: 600;
    border-radius: 3px;
    padding: 2px 4px;
    background-color: rgba(79, 195, 247, 0.1);
}
.chat-message .content a:hover {
    color: #ffffff !important;
    background-color: rgba(79, 195, 247, 0.3);
    text-decoration: none !important;
}
.chat-message .content a:visited {
    color: #4fc3f7 !important;
}
/* Stili per link buttons */
.link-button {
    display: inline-block;
    background-color: #4fc3f7;
    color: white !important;
    padding: 8px 16px;
    border-radius: 6px;
    text-decoration: none !important;
    font-weight: bold;
    margin: 5px 5px 5px 0;
    transition: all 0.3s ease;
    border: 2px solid #4fc3f7;
}
.link-button:hover {
    background-color: #81d4fa;
    border-color: #81d4fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(79, 195, 247, 0.3);
}
/* Personalizzazioni UniBg */
.unibg-colors {
    background: linear-gradient(135deg, #1f4e79 0%, #4fc3f7 100%);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Inizializza il chatbot se non è già stato fatto"""
    if 'chatbot' not in st.session_state:
        with st.spinner('Inizializzazione chatbot...'):
            st.session_state.chatbot = setup_chatbot()
            if st.session_state.chatbot:
                pass
            else:
                st.error('❌ Errore inizializzazione chatbot')
                return False
    return True

def create_clickable_links(text):
    """Converte URLs in link cliccabili e formatta il testo"""
    
    # Pattern per trovare URLs
    url_pattern = r'(https?://[^\s<>"{}|\\^`\[\]]+)'
    
    def replace_with_link(match):
        url = match.group(1)
        # Pulisci caratteri finali problematici
        url = re.sub(r'[,.)]+$', '', url)
        
        # Estrai nome dominio per display più carino
        domain_match = re.search(r'//([^/]+)', url)
        if domain_match:
            domain = domain_match.group(1)
            if 'unibg.it' in domain:
                display_text = f"🎓 {domain}"
            elif 'helpdesk' in domain:
                display_text = f"🆘 {domain}"
            elif 'logistica' in domain:
                display_text = f"📅 {domain}"
            else:
                display_text = domain
        else:
            display_text = url
        
        return f'<a href="{url}" target="_blank" class="link-button">{display_text}</a>'
    
    # Sostituisci URLs con link button
    text_with_links = re.sub(url_pattern, replace_with_link, text)
    
    # Gestisci markdown links [text](url) se presenti
    markdown_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    text_with_links = re.sub(markdown_pattern, r'<a href="\2" target="_blank" class="link-button">\1</a>', text_with_links)
    
    return text_with_links

def display_message_improved(message, is_user=True):
    """Versione migliorata per visualizzare messaggi con link cliccabili"""
    message_class = "user" if is_user else "bot"
    avatar = "👤" if is_user else "🤖"
    
    # Per messaggi bot, rendi i link cliccabili
    if not is_user:
        message = create_clickable_links(message)
    else:
        # Escape HTML per sicurezza nei messaggi utente
        import html
        message = html.escape(message)
    
    # Converti line breaks
    message = message.replace('\n', '<br>')
    
    # Migliora formattazione con emoji
    message = re.sub(r'•\s*', '• ', message)  # Normalizza bullet points
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="avatar">{avatar}</div>
        <div class="content">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def display_message_with_components(message, is_user=True):
    """Alternativa usando componenti nativi Streamlit"""
    
    if is_user:
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            # Dividi il messaggio in parti testo e link
            parts = re.split(r'(https?://[^\s<>"{}|\\^`\[\]]+)', message)
            
            for part in parts:
                if part.startswith('http'):
                    # È un link
                    url = re.sub(r'[,.)]+$', '', part)
                    st.markdown(f"🔗 [{url}]({url})")
                else:
                    # È testo normale
                    if part.strip():
                        st.write(part)

def main():
    # Header
    st.markdown("""
    <div class="unibg-colors">
        <h1 style="margin: 0; text-align: center;">ChatBot Segreteria Studenti</h1>
        <p style="margin: 5px 0 0 0; text-align: center; opacity: 0.9;">Università degli Studi di Bergamo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con informazioni
    with st.sidebar:
        st.write("**💡 Esempi di domande:**")
        examples = [
            "Come iscriversi agli esami?",
            "Quando pagare le tasse?",
            "Orari della segreteria?",
            "Servizi per disabili?",
            "Come richiedere certificati?"
        ]
        
        for example in examples:
            if st.button(f"▶️ {example}", key=example, use_container_width=True):
                st.session_state.user_input = example
        
        st.markdown("---")
        
        # Opzioni visualizzazione
        st.write("**⚙️ Modalità visualizzazione:**")
        display_mode = st.radio(
            "Scegli modalità:",
            ["🎨 Avanzata (HTML)", "🔗 Nativa (Streamlit)"],
            key="display_mode"
        )
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p><strong>Tesi Triennale</strong><br>
            Ingegneria Informatica</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Inizializza chatbot
    if not initialize_chatbot():
        return
    
    # Inizializza cronologia chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        welcome_msg = """Ciao! Sono il ChatBot della Segreteria Studenti UniBg.

Posso aiutarti con:
• Iscrizioni e esami
• Tasse universitarie  
• Certificati e documenti
• Contatti e orari
• Servizi per studenti con disabilità

Fai pure la tua domanda!"""
        st.session_state.messages.append({"role": "bot", "content": welcome_msg})
    
    # Scegli funzione di display
    if st.session_state.get("display_mode", "🎨 Avanzata (HTML)") == "🎨 Avanzata (HTML)":
        display_func = display_message_improved
    else:
        display_func = display_message_with_components
    
    # Visualizza cronologia chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            is_user = message["role"] == "user"
            display_func(message["content"], is_user)
    
    # Input utente
    user_input = st.chat_input("Scrivi la tua domanda...")
    
    # Gestione input da sidebar
    if 'user_input' in st.session_state:
        user_input = st.session_state.user_input
        del st.session_state.user_input
    
    if user_input:
        # Aggiungi messaggio utente
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Genera risposta
        with st.spinner('Sto cercando la risposta...'):
            try:
                result = st.session_state.chatbot.chat(user_input)
                response = result['response']
                
                # Aggiungi info sul redirect se necessario
                if result.get('should_redirect', False):
                    response += "\n\nPer assistenza personalizzata, apri un ticket alla Segreteria:\nhttps://helpdesk.unibg.it/"
                
                # Aggiungi risposta bot
                st.session_state.messages.append({"role": "bot", "content": response})
                
            except Exception as e:
                error_msg = f"❌ Errore: {str(e)}\n\nTi consiglio di contattare direttamente la Segreteria.\nhttps://helpdesk.unibg.it/"
                st.session_state.messages.append({"role": "bot", "content": error_msg})
        
        # Refresh per mostrare i nuovi messaggi
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;"> Tesi Triennale Ingegneria Informatica - UniBg 2024-2025</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
