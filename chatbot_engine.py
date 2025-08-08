from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

load_dotenv()

class ChatbotEngine:
    def __init__(self, vectorstore, top_k=3):
        self.vectorstore = vectorstore
        self.top_k = top_k
        
        # Initialize components
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7  # Make it more conversational
        )
        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": top_k},
            search_type="mmr"  # Use Maximum Marginal Relevance for better diversity
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create prompt template
        self.prompt_template = """
        You are a friendly and helpful AI assistant that answers questions based on the provided document context.
        
        Guidelines:
        - Always be warm, conversational, and helpful in your responses
        - If the user asks about something directly related to the document, use the context to provide detailed answers
        - If the user asks general questions or greetings, respond naturally and offer to help with document-related questions
        - If you cannot find specific information in the context, acknowledge this politely and offer alternative help
        - Use a conversational tone and feel free to ask follow-up questions
        - When referencing the document, be specific about what information you found
        
        Document Context:
        {context}
        
        Previous Conversation:
        {chat_history}
        
        User Question: {question}
        
        Friendly Response:
        """
        
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        # Create conversational chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self.prompt}
        )
    
    def get_response(self, question):
        """Get response from the chatbot"""
        try:
            # Check if it's a greeting or general question
            greeting_words = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you', 'thanks', 'thank you']
            question_lower = question.lower()
            
            # If it's a simple greeting, respond friendly but still use the retrieval system
            if any(greeting in question_lower for greeting in greeting_words) and len(question.split()) <= 3:
                enhanced_question = f"{question} Can you tell me what this document is about?"
                result = self.qa_chain({"question": enhanced_question})
            else:
                result = self.qa_chain({"question": question})
            
            answer = result['answer']
            sources = [doc.page_content for doc in result['source_documents']]
            
            # Post-process the answer to make it more friendly
            if "I don't have enough information" in answer or "cannot find" in answer.lower():
                if any(greeting in question_lower for greeting in greeting_words):
                    answer = f"Hello! 👋 I'm here to help you with questions about your document. {answer} Feel free to ask me anything specific about the content!"
                else:
                    answer = f"I don't have specific information about that in the document I'm working with. However, I can help you with other questions about the content. What else would you like to know?"
            
            return answer, sources
            
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
    
    def get_chat_history(self):
        """Get formatted chat history"""
        history = []
        messages = self.memory.chat_memory.messages
        
        for message in messages:
            role = "Human" if message.type == "human" else "AI"
            history.append(f"{role}: {message.content}")
        
        return history