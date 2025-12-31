import os
import sys
from document_processor import DocumentProcessor
from chatbot_engine import ChatbotEngine
from dotenv import load_dotenv

load_dotenv()

def test_chatbot_engine(file_path, question):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"--- Environment Check ---")
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        print("Warning: HUGGINGFACEHUB_API_TOKEN not found in .env file.")
    else:
        print("HUGGINGFACEHUB_API_TOKEN is set.")

    print(f"\n--- 1. Processing Document: {file_path} ---")
    processor = DocumentProcessor()
    vectorstore, doc_info = processor.process_document(file_path)
    print(f"Document processed: {doc_info}")

    print(f"\n--- 2. Initializing Chatbot Engine ---")
    try:
        engine = ChatbotEngine(vectorstore)
        print("Chatbot Engine initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Chatbot Engine: {e}")
        return

    print(f"\n--- 3. Asking Question: '{question}' ---")
    try:
        answer, sources = engine.get_response(question)
        print(f"\nAI Response:\n{answer}")
        print(f"\nSources used: {len(sources)}")
        for i, source in enumerate(sources):
            print(f"Source {i+1} (first 100 chars): {source[:100]}...")
    except Exception as e:
        print(f"\nError getting response: {e}")

if __name__ == "__main__":
    test_file = "CV-Dec.pdf"
    test_question = "What are the key skills mentioned in the document?"
    
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    if len(sys.argv) > 2:
        test_question = sys.argv[2]
        
    test_chatbot_engine(test_file, test_question)
