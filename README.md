# Private Document AI (Local RAG System)
A privacy-focused, 100% local Retrieval-Augmented Generation (RAG) system. This application allows users to upload PDF documents and query them instantly using a local LLM, complete with page-level source citations to prevent hallucinations.

Created by Vishvas Parmar.

## Features
* **Zero Cloud Costs:** Uses local inference and local embeddings.
* **Privacy First:** Data never leaves the local machine.
* **Dynamic Document Ingestion:** Upload any PDF through the UI to instantly vectorize it.
* **Verifiable Citations:** The AI returns exact source files and page numbers for every answer.
* **Modern Chat UI:** Built with Streamlit's native chat elements.

## Technical Architecture
1. **Frontend:** Streamlit handles the chat interface and file uploads.
2. **API Layer:** FastAPI manages asynchronous routes and data validation via Pydantic.
3. **Orchestration:** LangChain Expression Language (LCEL) chains handle retrieval and prompt injection.
4. **Vector Store:** ChromaDB stores and retrieves document embeddings.
5. **LLM Engine:** Ollama serves the Mistral model for both embeddings and text generation.

## Technology Stack
* Python 3.12
* FastAPI
* LangChain
* ChromaDB
* Ollama (Mistral)
* Streamlit

## How to Run Locally

1. **Install Ollama** and download the Mistral model:
   ```bash
   ollama run mistral
   ```
2. **Install Python Dependancies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Start the FastAPI Backend:**
   ```bash
   uvicorn main:app --reload
   ```
4. **Start the Streamlit Frontend:**
   ```bash
   streamlit run app.py
   ```

---

**If like the idea, leave a star⭐.**