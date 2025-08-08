import streamlit as st

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'chatbot_engine' not in st.session_state:
        st.session_state.chatbot_engine = None
    
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    
    if 'doc_info' not in st.session_state:
        st.session_state.doc_info = None

def display_chat_history():
    """Display chat messages from history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def format_sources(sources):
    """Format source documents for display"""
    formatted_sources = []
    for i, source in enumerate(sources, 1):
        # Truncate long sources
        truncated = source[:200] + "..." if len(source) > 200 else source
        formatted_sources.append(f"**Source {i}:** {truncated}")
    
    return formatted_sources