import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 1. Set up our free, local Embedding Model via Ollama
# (Embeddings turn text into a map of numbers)
embeddings = OllamaEmbeddings(model="mistral")

# 2. Define the database folder
DB_DIR = "./chroma_db"

def process_pdf(pdf_path: str):
    print(f"📄 Loading PDF: {pdf_path}...")
    
    #Delete the old database so the AI forgets the previous PDF
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
        print("🗑️ Cleared old AI memory.")
    
    # Step 1: Read the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Step 2: Chop it into smaller chunks (1000 characters each)
    # We use an overlap of 200 characters so sentences don't get cut in half awkwardly
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Sliced the PDF into {len(chunks)} smaller chunks.")
    
    # Step 3 & 4: Embed the chunks and save them to the Vector Database
    print("💾 Saving to Vector Database (This might take a minute)...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    print("✅ PDF successfully ingested into the database!")

