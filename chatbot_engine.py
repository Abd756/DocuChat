import os
import logging
from typing import List, Tuple
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

class ChatbotEngine:
    def __init__(self, vectorstore, top_k=5):
        self.vectorstore = vectorstore
        self.top_k = top_k
        self.history = [] # Manual conversation history
        
        # Initialize the LLM - Using ChatHuggingFace wrapper for better chat capabilities
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        
        try:
            endpoint_llm = HuggingFaceEndpoint(
                repo_id=repo_id,
                max_new_tokens=1024,
                temperature=0.1,
                huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
                timeout=300
            )
            self.llm = ChatHuggingFace(llm=endpoint_llm)
        except Exception as e:
            logging.error(f"Error initializing ChatHuggingFace: {e}")
            # Fallback to direct endpoint
            self.llm = HuggingFaceEndpoint(
                repo_id=repo_id,
                max_new_tokens=512,
                temperature=0.1,
                huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
            )
        
        # Initialize retriever
        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )
        
        # Define the RAG prompt with history
        self.prompt = ChatPromptTemplate.from_template("""
        You are a helpful and intelligent document assistant. Use the following pieces of context and the conversation history to answer the visitor's question.
        If you don't know the answer or the context doesn't provide enough information, just say that you don't know.
        
        Context:
        {context}
        
        Recent Conversation History:
        {history}
        
        Question: {question}
        
        Answer:""")
        
        # RAG Chain
        self.chain = (
            {
                "context": self.retriever | self._format_docs, 
                "history": lambda x: self._format_history(),
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs):
        """Format retrieved documents as context string"""
        return "\n\n".join(doc.page_content for doc in docs)

    def _format_history(self):
        """Format history list into a string"""
        if not self.history:
            return "No previous interaction."
        # Keep last 5 exchanges to avoid prompt bloat
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.history[-6:]])

    def get_response(self, question: str) -> Tuple[str, List[str]]:
        """
        Process the user query and return (response_text, list_of_source_contents)
        """
        try:
            # 1. Get retrieved docs for source tracking and filter unique ones
            docs = self.retriever.invoke(question)
            
            # Use a seen set to maintain order and uniqueness
            seen = set()
            sources = []
            for doc in docs:
                content = doc.page_content.strip()
                if content and content not in seen:
                    seen.add(content)
                    sources.append(content)
            
            # 2. Generate response including history
            response = self.chain.invoke(question)
            
            # 3. Update history
            self.history.append({"role": "User", "content": question})
            self.history.append({"role": "Assistant", "content": response.strip()})
            
            return response.strip(), sources
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            logging.error(f"Error in ChatbotEngine: {error_msg}")
            if "Authorization" in str(e):
                return "Authentication Error: Please verify your HUGGINGFACEHUB_API_TOKEN.", []
            return f"Thinking error: {error_msg}", []

    def clear_memory(self):
        """Reset conversation history"""
        self.history = []
