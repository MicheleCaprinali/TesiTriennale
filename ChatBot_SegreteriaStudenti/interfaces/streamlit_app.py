import streamlit as st
import sys
import os
import re

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import setup_chatbot

# Configurazione pagina
st.set_page_config(
    page_title="ChatBot UniBg - Segreteria Studenti",
    page_icon="🎓",
    layout="wide"
)

# CSS personalizzato con palette nero e azzurro
st.markdown("""
<style>
/* Theme scuro con palette nero e azzurro */
.stApp {
    background-color: #1a1a1a;
    color: #ffffff;
}

/* Header principale */
.unibg-header {
    background: linear-gradient(135deg, #1a1a1a 0%, #1976d2 100%);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3);
    border: 1px solid #4fc3f7;
}

/* Stili per i messaggi chat */
.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    display: flex;
    border: 1px solid #333;
    background-color: #2d2d2d;
}

.chat-message.user {
    background-color: #1e3a5f;
    border-left: 4px solid #4fc3f7;
}

.chat-message.bot {
    background-color: #2d2d2d;
    border-left: 4px solid #1976d2;
}

.chat-message .avatar {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    margin-right: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    background-color: #1976d2;
    color: white;
    border: 2px solid #4fc3f7;
}

.chat-message.user .avatar {
    background-color: #4fc3f7;
    border-color: #1976d2;
}

.chat-message .content {
    flex: 1;
    line-height: 1.6;
    font-size: 1rem;
    color: #ffffff;
}

/* Stili per i link */
.chat-message .content a {
    color: #4fc3f7 !important;
    text-decoration: underline !important;
    font-weight: 600;
    padding: 2px 4px;
    border-radius: 4px;
    background-color: rgba(79, 195, 247, 0.1);
    transition: all 0.3s ease;
}

.chat-message .content a:hover {
    color: #81d4fa !important;
    background-color: rgba(79, 195, 247, 0.2);
    text-decoration: none !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 15px;
    background-color: #2d2d2d;
    border-radius: 8px;
    border: 1px solid #333;
    color: #4fc3f7;
    margin-top: 20px;
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
    """Converte URLs in link cliccabili HTML standard"""
    # Pattern migliorato per trovare URLs
    url_pattern = r'(https?://[^\s<>"{}|\\^`\[\]]+)'
    
    def replace_url(match):
        url = match.group(1)
        # Rimuovi punteggiatura finale
        url = re.sub(r'[,.!?;)]+$', '', url)
        return f'<a href="{url}" target="_blank">{url}</a>'
    
    # Sostituisci URLs con link HTML semplici
    text_with_links = re.sub(url_pattern, replace_url, text)
    
    return text_with_links

def display_message_improved(message, is_user=True):
    """Visualizza messaggi con link cliccabili"""
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
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="avatar">{avatar}</div>
        <div class="content">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="unibg-header">
        <h1 style="margin: 0; text-align: center;">🎓 ChatBot Segreteria Studenti</h1>
        <p style="margin: 10px 0 0 0; text-align: center; opacity: 0.9;">Università degli Studi di Bergamo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con esempi di domande
    with st.sidebar:
        st.markdown("### 💡 Esempi di domande")
        
        examples = [
            "Come iscriversi agli esami?",
            "Quando pagare le tasse universitarie?",
            "Orari della segreteria studenti?", 
            "Servizi per studenti con disabilità?",
            "Come richiedere certificati?",
            "Informazioni su alloggi universitari?",
            "Procedure per la laurea?",
            "Contatti segreteria"
        ]
        
        for example in examples:
            if st.button(f"▶️ {example}", key=example, use_container_width=True):
                st.session_state.user_input = example
        
        st.markdown("---")
        
        # Informazioni progetto
        st.markdown("""
        <div style="background-color: #2d2d2d; padding: 15px; border-radius: 8px; border: 1px solid #4fc3f7;">
            <h4 style="color: #4fc3f7; text-align: center; margin-bottom: 10px;">📖 Progetto Tesi</h4>
            <p style="text-align: center; color: #ffffff; font-size: 0.9rem; margin: 0;">
                <strong>RAG ChatBot</strong><br>
                Tesi Triennale<br>
                Ingegneria Informatica<br>
                UniBg 2024-2025
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Inizializza chatbot
    if not initialize_chatbot():
        return
    
    # Inizializza cronologia chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        welcome_msg = """Ciao! 👋 Sono il ChatBot della Segreteria Studenti UniBg.

Posso aiutarti con informazioni su:
• 📚 Iscrizioni e gestione esami
• 💰 Tasse universitarie e pagamenti
• 📄 Certificati e documenti ufficiali
• 📞 Contatti e orari degli uffici
• ♿ Servizi per studenti con disabilità
• 🏠 Alloggi e servizi universitari
• 🎓 Procedure di laurea

Scrivi la tua domanda qui sotto! 🚀"""
        st.session_state.messages.append({"role": "bot", "content": welcome_msg})
    
    # Visualizza cronologia chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            is_user = message["role"] == "user"
            display_message_improved(message["content"], is_user)
    
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
    st.markdown("""
    <div class="footer">
        🎓 RAG ChatBot per Segreteria Studenti UniBg<br>
        <small>Tesi Triennale Ingegneria Informatica • A.A. 2024-2025</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
