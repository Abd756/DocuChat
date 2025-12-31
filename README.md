# 💬 DocuChat AI

DocuChat AI is a modern, intelligent document conversation platform. Upload your PDFs, text files, or Word documents and have context-aware conversations with them using state-of-the-art open-source LLMs.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

## 🚀 Features

- **Multi-format Support**: Upload PDF, TXT, or DOCX files.
- **Smart Embeddings**: Uses `all-MiniLM-L6-v2` for efficient local vector search via ChromaDB.
- **Conversational Memory**: The AI remembers previous exchanges within a session for natural follow-up questions.
- **Open Source LLMs**: Integrated with Hugging Face Inference API (Mistral-7B, Zephyr, etc.).
- **Modern UI**: A premium, responsive interface inspired by ChatGPT/Claude.
- **Automatic Cleanup**: Ensures clean processing by refreshing the vector store for each new document.

## 🛠️ Local Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd DocuChat
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate # On Mac/Linux
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   Create a `.env` file in the root directory:
   ```env
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
   ```
   *Note: Ensure your Hugging Face token has "Inference Provider" permissions enabled.*

5. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment on Streamlit Cloud

1. Push your code to a GitHub repository.
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/).
3. Create a new app and point it to `app.py`.
4. **Important**: Add your `HUGGINGFACEHUB_API_TOKEN` to the Streamlit **Secrets** manager:
   ```toml
   HUGGINGFACEHUB_API_TOKEN = "your_token_here"
   ```

## 📁 Project Structure

- `app.py`: Main Streamlit application and UI logic.
- `document_processor.py`: Handles file loading, splitting, and vector indexing.
- `chatbot_engine.py`: Manages the LLM chain, memory, and retrieval.
- `requirements.txt`: List of required Python packages.
- `chroma_db/`: Local directory for persistent vector storage.

## 📝 License

This project is open-source and available under the MIT License.
