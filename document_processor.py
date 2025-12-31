from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Use HuggingFace embeddings instead of Google to avoid async issues
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def load_document(self, file_path):
        """Load document based on file extension"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension == '.txt':
            loader = TextLoader(file_path)
        elif file_extension in ['.docx', '.doc']:
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        return loader.load()
    
    def process_document(self, file_path):
        """Process document and create vector store"""
        try:
            # Load document
            documents = self.load_document(file_path)
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Use a persistent directory for the embeddings
            persist_dir = "chroma_db"
            
            # Clear previous vector store to avoid duplicates/mixing documents
            import shutil
            if os.path.exists(persist_dir):
                shutil.rmtree(persist_dir)
            
            # Create vector store
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=persist_dir
            )
            
            # Document information
            doc_info = {
                'pages': len(documents),
                'chunks': len(chunks),
                'file_path': file_path,
                'storage': persist_dir
            }
            
            return vectorstore, doc_info
            
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
    
    def get_document_stats(self, documents, chunks):
        """Get document statistics"""
        total_chars = sum(len(doc.page_content) for doc in documents)
        avg_chunk_size = sum(len(chunk.page_content) for chunk in chunks) / len(chunks)
        
        return {
            'total_pages': len(documents),
            'total_chunks': len(chunks),
            'total_characters': total_chars,
            'avg_chunk_size': int(avg_chunk_size)
        }