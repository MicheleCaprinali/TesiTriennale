import streamlit as st
import sys
import os
import re
import time

# Setup path - Corretto per la nuova struttura
current_dir = os.path.dirname(__file__)
src_path = os.path.join(current_dir, '..', 'src')
sys.path.append(src_path)

# Import corretti
try:
    from local_embeddings import LocalEmbeddings
    from creazione_vectorstore import search_vectorstore
    from ollama_llm import OllamaLLM
except ImportError as e:
    st.error(f"Errore import moduli: {e}")
    st.stop()

# Configurazione pagina
st.set_page_config(
    page_title="ChatBot UniBg - Segreteria Studenti",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato - Tema scuro professionale
st.markdown("""
<style>
/* Theme scuro professionale */
.stApp {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #ffffff;
}

/* Header principale */
.unibg-header {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
    color: white;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
    text-align: center;
}

.unibg-header h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.unibg-header p {
    margin: 10px 0 0 0;
    opacity: 0.95;
    font-size: 1.1rem;
    font-weight: 400;
}

/* Container chat */
.chat-container {
    background-color: #2a2a2a;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid #404040;
}

/* Messaggi chat */
.chat-message {
    padding: 15px 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    display: flex;
    align-items: flex-start;
    max-width: 85%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chat-message.user {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 5px;
}

.chat-message.bot {
    background: linear-gradient(135deg, #404040 0%, #505050 100%);
    color: #ffffff;
    margin-right: auto;
    border: 1px solid #606060;
    border-bottom-left-radius: 5px;
}

.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    font-weight: 600;
    flex-shrink: 0;
}

.chat-message.user .avatar {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    margin-right: 0;
    margin-left: 15px;
    order: 2;
}

.chat-message.bot .avatar {
    background: #3b82f6;
    color: white;
}

.chat-message .content {
    flex: 1;
    line-height: 1.6;
    font-size: 1rem;
}

.chat-message.user .content {
    text-align: right;
}

/* Link styling */
.chat-message .content a {
    color: #60a5fa !important;
    text-decoration: none !important;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 6px;
    background-color: rgba(96, 165, 250, 0.2);
    transition: all 0.3s ease;
    border-bottom: 2px solid transparent;
}

.chat-message .content a:hover {
    background-color: rgba(96, 165, 250, 0.3);
    border-bottom-color: #60a5fa;
    transform: translateY(-1px);
}

.chat-message.user .content a {
    color: #bfdbfe !important;
    background-color: rgba(255, 255, 255, 0.2);
}

.chat-message.user .content a:hover {
    background-color: rgba(255, 255, 255, 0.3);
    border-bottom-color: white;
}

/* Sidebar styling */
.css-1d391kg {
    background-color: #1a1a1a !important;
}

.sidebar-section {
    background-color: #2a2a2a;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    border: 1px solid #404040;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #2a2a2a 0%, #404040 100%);
    color: #ffffff;
    border: 1px solid #606060;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
    transition: all 0.3s ease;
    width: 100%;
    text-align: left;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Input styling */
.stChatInput > div > div > input {
    background-color: #2a2a2a !important;
    border: 2px solid #404040 !important;
    border-radius: 25px;
    padding: 12px 20px;
    font-size: 1rem;
    color: #ffffff !important;
    transition: border-color 0.3s ease;
}

.stChatInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.stChatInput > div > div > input::placeholder {
    color: #9ca3af !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 15px;
    color: #9ca3af;
    margin-top: 30px;
    border: 1px solid #404040;
}

/* Loading indicator */
.stSpinner > div {
    color: #3b82f6 !important;
}

/* Sidebar text color fix */
.css-1d391kg .stMarkdown {
    color: #ffffff;
}

.css-1d391kg h3 {
    color: #ffffff !important;
}

/* Sidebar divider */
.css-1d391kg hr {
    border-color: #404040;
}
</style>
""", unsafe_allow_html=True)

class ChatbotRAG:
    """Classe ChatbotRAG integrata per Streamlit"""
    
    def __init__(self):
        self.embedder = LocalEmbeddings()
        self.llm = OllamaLLM()
        
    def retrieve_documents(self, query, k=5):
        try:
            results = search_vectorstore(query, k=k, embedder=self.embedder)
            if not results["documents"] or not results["documents"][0]:
                return []
            
            docs = []
            for doc, distance in zip(results["documents"][0], results["distances"][0]):
                docs.append({
                    "content": doc,
                    "score": distance
                })
            return docs
        except Exception:
            return []
    
    def generate_response(self, query, context_docs):
        if context_docs:
            context = "\n\n".join([doc["content"] for doc in context_docs[:3]])
        else:
            context = "Informazioni non trovate nei documenti disponibili."
        
        try:
            response = self.llm.generate(query, context)
            return {
                "response": response,
                "context_used": len(context_docs),
                "should_redirect": len(context_docs) == 0 or "REDIRECT_TO_HUMAN" in response
            }
        except Exception as e:
            return {
                "response": "Servizio temporaneamente non disponibile. Contattare la segreteria studenti.",
                "context_used": 0,
                "should_redirect": True
            }
    
    def chat(self, query):
        docs = self.retrieve_documents(query)
        result = self.generate_response(query, docs)
        return result

@st.cache_resource
def initialize_chatbot():
    """Inizializza il chatbot con cache per performance"""
    try:
        return ChatbotRAG()
    except Exception as e:
        st.error(f"❌ Errore inizializzazione: {e}")
        return None

def create_clickable_links(text):
    """Converte URLs in link cliccabili HTML"""
    url_pattern = r'(https?://[^\s<>"{}|\\^`\[\]]+)'
    
    def replace_url(match):
        url = match.group(1).rstrip('.,!?;)')
        return f'<a href="{url}" target="_blank">{url}</a>'
    
    return re.sub(url_pattern, replace_url, text)

def display_message(message, is_user=True):
    """Visualizza messaggi con styling ottimizzato"""
    message_class = "user" if is_user else "bot"
    avatar = "👤" if is_user else "🤖"
    
    if not is_user:
        message = create_clickable_links(message)
    else:
        import html
        message = html.escape(message)
    
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
        <h1>🎓 ChatBot Segreteria Studenti</h1>
        <p>Università degli Studi di Bergamo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 💡 Esempi di Domande")
        
        examples = [
            "Come iscriversi agli esami?",
            "Quando pagare le tasse universitarie?",
            "Orari della segreteria studenti?", 
            "Servizi per studenti con disabilità?",
            "Come richiedere certificati?",
            "Procedure per la laurea?",
            "Contatti segreteria"
        ]
        
        for example in examples:
            if st.button(f"▶️ {example}", key=example):
                st.session_state.user_input = example
        
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-section">
            <h4 style="color: #3b82f6; text-align: center; margin-bottom: 10px;">📖 Progetto Tesi</h4>
            <p style="text-align: center; font-size: 0.9rem; margin: 0; color: #9ca3af;">
                <strong>RAG ChatBot</strong><br>
                Tesi Triennale<br>
                Ingegneria Informatica<br>
                UniBg 2024-2025
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Inizializza chatbot
    chatbot = initialize_chatbot()
    if not chatbot:
        st.error("❌ Impossibile inizializzare il chatbot. Verifica che Ollama sia in esecuzione.")
        return
    
    # Inizializza chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        welcome_msg = """Ciao! 👋 Sono il ChatBot della Segreteria Studenti UniBg.

Posso aiutarti con informazioni su:
• 📚 Iscrizioni e gestione esami
• 💰 Tasse universitarie e pagamenti
• 📄 Certificati e documenti ufficiali
• 📞 Contatti e orari degli uffici
• ♿ Servizi per studenti con disabilità
• 🎓 Procedure di laurea

Scrivi la tua domanda qui sotto! 🚀"""
        st.session_state.messages.append({"role": "bot", "content": welcome_msg})
    
    # Container chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        is_user = message["role"] == "user"
        display_message(message["content"], is_user)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input
    user_input = st.chat_input("💬 Scrivi la tua domanda...")
    
    # Gestisci input da sidebar
    if 'user_input' in st.session_state:
        user_input = st.session_state.user_input
        del st.session_state.user_input
    
    if user_input:
        # Aggiungi messaggio utente
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Genera risposta
        with st.spinner('🔄 Sto elaborando la risposta...'):
            try:
                result = chatbot.chat(user_input)
                response = result['response']
                
                # Gestisci redirect
                if result.get('should_redirect', False) and "REDIRECT_TO_HUMAN" in response:
                    response = response.replace("REDIRECT_TO_HUMAN - ", "")
                    response += "\n\n💡 **Per assistenza personalizzata:**\n🔗 https://helpdesk.unibg.it/"
                
                st.session_state.messages.append({"role": "bot", "content": response})
                
            except Exception as e:
                error_msg = f"❌ Si è verificato un errore: {str(e)}\n\n💡 **Contatta la Segreteria:**\n🔗 https://helpdesk.unibg.it/"
                st.session_state.messages.append({"role": "bot", "content": error_msg})
        
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        🎓 <strong>RAG ChatBot</strong> per Segreteria Studenti UniBg<br>
        <small>Tesi Triennale Ingegneria Informatica • A.A. 2024-2025</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()