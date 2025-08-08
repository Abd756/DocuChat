import streamlit as st
import tempfile
import os
from document_processor import DocumentProcessor
from chatbot_engine import ChatbotEngine
from utils import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="CYour Document Chat AI",
    page_icon="💬",
    layout="centered"
)

# Simple CSS like ChatGPT
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Clean main container */
    .main {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
        background: #ffffff;
    }
    
    /* Modern header - 80vw width only */
    .header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        color: white;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        width: 80vw !important;
        margin-left: auto !important;
        margin-right: auto !important;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Document status with better styling */
    .doc-status {
        background: linear-gradient(135deg, #10a37f 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(16, 163, 127, 0.3);
    }
    
    /* Simple upload area - clean and short */
    .upload-section {
        background: #313160 ;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .upload-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .upload-description {
        color: #e2e8f0;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        min-height: 400px;
    }
    
    /* Source styling */
    .source-item {
        background: #f8fafc;
        border-left: 4px solid #10a37f;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: #10a37f !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(16, 163, 127, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: #059669 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(16, 163, 127, 0.4) !important;
    }
    
    /* Example buttons */
    .example-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* File uploader improvements */
    .stFileUploader {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Processing section */
    .processing {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        border: 1px solid #e5e7eb;
        margin: 2rem 0;
    }
    
    .processing-icon {
        font-size: 2.5rem;
        color: #10a37f;
        margin-bottom: 1rem;
        animation: spin 2s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main { padding: 0.5rem; }
        .title { font-size: 2rem; }
        .example-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Modern header
st.markdown("""
<div class="header">
    <h1 class="title">💬 Document Chat AI</h1>
    <p class="subtitle">Upload any document and have intelligent conversations with it</p>
</div>
""", unsafe_allow_html=True)

# Document status (if loaded)
if st.session_state.chatbot_engine and st.session_state.doc_info:
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
        <div class="doc-status">
            <div>
                📄 <strong>{st.session_state.current_file}</strong> 
                • {st.session_state.doc_info['pages']} pages • {st.session_state.doc_info['chunks']} chunks
            </div>
            <div style="color: white; font-weight: 500;">Ready</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🔄 New"):
            for key in ['chatbot_engine', 'current_file', 'doc_info', 'messages', 'processing_file']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Clean and simple upload section
if not st.session_state.chatbot_engine and not st.session_state.get('processing_file', False):
    st.markdown("""
    <div class="upload-section">
        <h2 class="upload-title">📄 Ready to chat with your documents?</h2>
        <p class="upload-description">Upload a PDF, TXT, or DOCX file to start an intelligent conversation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple file uploader
    st.markdown("### 📎 Choose Your Document")
    uploaded_file = st.file_uploader(
        "Drag and drop or click to browse",
        type=['pdf', 'txt', 'docx'],
        help="Supported formats: PDF, TXT, DOCX (up to 200MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Show file info
        file_size = len(uploaded_file.getvalue()) / (1024*1024)  # MB
        st.success(f"✅ **{uploaded_file.name}** loaded ({file_size:.1f} MB)")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process & Chat", type="primary", use_container_width=True):
                st.session_state.uploaded_file_data = uploaded_file.getvalue()
                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.processing_file = True
                st.rerun()

# Processing section
if st.session_state.get('processing_file', False):
    st.markdown("""
    <div class="processing">
        <div class="processing-icon">⚙️</div>
        <h2 style="color: #374151; margin-bottom: 0.5rem;">Processing Your Document</h2>
        <p style="color: #6b7280; margin-bottom: 1.5rem;">Analyzing content and creating intelligent embeddings...</p>
    </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        file_data = st.session_state.uploaded_file_data
        file_name = st.session_state.uploaded_file_name
        file_extension = file_name.split('.')[-1]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
            tmp_file.write(file_data)
            tmp_file_path = tmp_file.name
        
        status_text.text("Loading document...")
        progress_bar.progress(25)
        
        processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
        
        status_text.text("Creating chunks...")
        progress_bar.progress(50)
        
        vectorstore, doc_info = processor.process_document(tmp_file_path)
        
        status_text.text("Building embeddings...")
        progress_bar.progress(75)
        
        st.session_state.chatbot_engine = ChatbotEngine(vectorstore=vectorstore, top_k=10)
        st.session_state.current_file = file_name
        st.session_state.doc_info = doc_info
        
        progress_bar.progress(100)
        status_text.text("Ready!")
        
        welcome_msg = f"""🎉 **{file_name}** is ready for conversation!

📋 **Document Stats:**
- 📄 **{doc_info['pages']} pages** processed
- 🧩 **{doc_info['chunks']} sections** created  
- 🧠 **AI embeddings** generated

💬 **What would you like to know?** Just ask me anything about your document!"""
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg,
            "sources": []
        })
        
        st.session_state.processing_file = False
        del st.session_state.uploaded_file_data
        del st.session_state.uploaded_file_name
        
        st.success("Document processed successfully!")
        
        import time
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.processing_file = False
    
    finally:
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            with st.expander(f"📚 **View Sources** ({len(message['sources'])} references)", expanded=False):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"""
                    <div class="source-item">
                        <div style="font-weight: 600; color: #10a37f; margin-bottom: 0.5rem;">
                            📖 Source {i}
                        </div>
                        <div style="font-size: 0.9rem; line-height: 1.6;">
                            {source[:350]}{'...' if len(source) > 350 else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# # Example questions
# if st.session_state.chatbot_engine and len(st.session_state.messages) <= 1:
#     st.markdown("### 💡 **Try these questions:**")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         if st.button("📋 **Summarize**", key="sum", use_container_width=True):
#             prompt = "Please provide a comprehensive summary of this document"
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             st.rerun()
    
#     with col2:
#         if st.button("🔍 **Key Points**", key="key", use_container_width=True):
#             prompt = "What are the most important key points and main ideas in this document?"
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             st.rerun()
    
#     with col3:
#         if st.button("🎯 **Main Topics**", key="topics", use_container_width=True):
#             prompt = "What are the main topics and themes covered in this document?"
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             st.rerun()

# Chat input
if st.session_state.chatbot_engine:
    if prompt := st.chat_input("💬 Ask me anything about your document..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analyzing document and generating response..."):
                try:
                    response, sources = st.session_state.chatbot_engine.get_response(prompt)
                    st.markdown(response)
                    
                    if sources:
                        with st.expander(f"📚 **View Sources** ({len(sources)} references)", expanded=False):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"""
                                <div class="source-item">
                                    <div style="font-weight: 600; color: #10a37f; margin-bottom: 0.5rem;">
                                        📖 Source {i}
                                    </div>
                                    <div style="font-size: 0.9rem; line-height: 1.6;">
                                        {source[:350]}{'...' if len(source) > 350 else ''}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                
                except Exception as e:
                    response = f"⚠️ Sorry, I encountered an error: {str(e)}"
                    sources = []
                    st.error(response)
        
        # Add to history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "sources": sources if 'sources' in locals() else []
        })

# elif not st.session_state.get('processing_file', False):
#     st.markdown("""
#     <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 12px; border: 1px solid #e5e7eb; margin: 2rem 0;">
#         <div style="font-size: 1.2rem; color: #10a37f; margin-bottom: 0.5rem;">🎯 Ready to Start?</div>
#         <div style="color: #6b7280;">Upload a document above to begin your intelligent conversation</div>
#     </div>
#     """, unsafe_allow_html=True)
