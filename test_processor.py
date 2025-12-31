import os
import sys
from document_processor import DocumentProcessor

def test_document_processor(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"--- Processing Document: {file_path} ---")
    
    # Initialize processor
    processor = DocumentProcessor()
    
    try:
        # Load the document
        print("Loading document...")
        documents = processor.load_document(file_path)
        print(f"Loaded {len(documents)} document pages/parts.")
        
        # Split into chunks
        print("Splitting into chunks...")
        chunks = processor.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks.")
        
        # Show chunk statistics
        stats = processor.get_document_stats(documents, chunks)
        print("\n--- Document Statistics ---")
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
        # Display first 2 chunks as preview
        print("\n--- Chunks Preview (First 2) ---")
        for i, chunk in enumerate(chunks[:2]):
            print(f"\nChunk {i+1}:")
            print("-" * 20)
            # Truncate content for display
            content = chunk.page_content[:200] + "..." if len(chunk.page_content) > 200 else chunk.page_content
            print(content)
            print("-" * 20)
            
            # Show embedding for this chunk
            print(f"Generating embedding for Chunk {i+1}...")
            embedding = processor.embeddings.embed_query(chunk.page_content)
            print(f"Embedding dimensions: {len(embedding)}")
            print(f"Embedding preview (first 5 values): {embedding[:5]}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default to README.md if it exists as a fallback
        file_path = "README.md"
        print(f"No file path provided. Using {file_path} as default.")
        
    test_document_processor(file_path)
