import streamlit as st
import sys
import os

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import setup_chatbot
import time

# Configurazione pagina
st.set_page_config(
    page_title="ChatBot UniBG",
    page_icon="🎓",
    layout="wide"
)

# CSS personalizzato
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1f4e79;
    border-bottom: 2px solid #1f4e79;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #e3f2fd;
}
.chat-message.bot {
    background-color: #f5f5f5;
}
.chat-message .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 1rem;
}
.sidebar-content {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Inizializza il chatbot"""
    if 'chatbot' not in st.session_state:
        with st.spinner('🔄 Inizializzazione chatbot...'):
            st.session_state.chatbot = setup_chatbot()
            if st.session_state.chatbot:
                st.success('✅ Chatbot pronto!')
            else:
                st.error('❌ Errore inizializzazione chatbot')
                return False
    return True

def display_message(message, is_user=True):
    """Visualizza un messaggio nella chat"""
    message_class = "user" if is_user else "bot"
    avatar = "👤" if is_user else "🤖"
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="avatar">{avatar}</div>
        <div>{message}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 ChatBot Segreteria Studenti UniBG</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar con informazioni
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("ℹ️ Informazioni")
        st.write("**Tecnologie utilizzate:**")
        st.write("• 🧠 Mistral 7B (LLM locale)")
        st.write("• 🔍 Sentence Transformers")
        st.write("• 💾 ChromaDB")
        st.write("• 🔗 RAG Architecture")
        
        st.write("**Documenti indicizzati:**")
        if os.path.exists("vectordb"):
            import chromadb
            try:
                client = chromadb.PersistentClient(path="vectordb")
                collection = client.get_collection("unibg_docs")
                doc_count = collection.count()
                st.write(f"📄 {doc_count} documenti")
            except:
                st.write("📄 Database presente")
        
        st.write("**Esempi di domande:**")
        examples = [
            "Come iscriversi agli esami?",
            "Quando pagare le tasse?",
            "Orari della segreteria?",
            "Servizi per disabili?",
            "Come richiedere certificati?"
        ]
        
        for example in examples:
            if st.button(f"💡 {example}", key=example):
                st.session_state.user_input = example
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Inizializza chatbot
    if not initialize_chatbot():
        return
    
    # Inizializza cronologia chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Messaggio di benvenuto
        welcome_msg = """👋 Ciao! Sono il ChatBot della Segreteria Studenti UniBG.

Posso aiutarti con:
• 📚 Iscrizioni e esami
• 💰 Tasse universitarie  
• 📄 Certificati e documenti
• 🏢 Contatti e orari
• ♿ Servizi per studenti con disabilità

Fai pure la tua domanda! 😊"""
        st.session_state.messages.append({"role": "bot", "content": welcome_msg})
    
    # Visualizza cronologia chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            is_user = message["role"] == "user"
            display_message(message["content"], is_user)
    
    # Input utente
    user_input = st.chat_input("Scrivi la tua domanda...")
    
    # Gestione input da sidebar
    if 'user_input' in st.session_state:
        user_input = st.session_state.user_input
        del st.session_state.user_input
    
    if user_input:
        # Aggiungi messaggio utente
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Mostra messaggio utente
        display_message(user_input, True)
        
        # Genera risposta
        with st.spinner('🔍 Sto cercando la risposta...'):
            try:
                result = st.session_state.chatbot.chat(user_input)
                response = result['response']
                
                # Aggiungi info sul redirect se necessario
                if result.get('should_redirect', False):
                    response += "\n\n🎫 **Per assistenza personalizzata, apri un ticket alla Segreteria:**\n🌐 https://www.unibg.it/servizi-studenti/contatti"
                
                # Aggiungi risposta bot
                st.session_state.messages.append({"role": "bot", "content": response})
                
                # Mostra risposta bot
                display_message(response, False)
                
            except Exception as e:
                error_msg = f"❌ Errore: {str(e)}\n\nTi consiglio di contattare direttamente la Segreteria."
                st.session_state.messages.append({"role": "bot", "content": error_msg})
                display_message(error_msg, False)
        
        # Refresh per mostrare i nuovi messaggi
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">🎓 Tesi Triennale Ingegneria Informatica - UniBG 2025</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
