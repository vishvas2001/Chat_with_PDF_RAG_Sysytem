from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# ==========================================
# 1. SETUP MODELS & DATABASE
# ==========================================
llm = ChatOllama(model="mistral")
embeddings = OllamaEmbeddings(model="mistral")
DB_DIR = "./chroma_db"

# ==========================================
# 2. BASIC AI CHAT (No PDF Context)
# ==========================================
def ask_langchain_ai(user_prompt: str) -> str:
    print(f"Asking basic AI: '{user_prompt}'...")
    
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content=user_prompt)
    ]
    response = llm.invoke(messages)
    return response.content

# ==========================================
# 3. RAG PIPELINE (The Modern LCEL Way)
# ==========================================


system_prompt = (
    "You are a helpful assistant. Use the following pieces of retrieved context "
    "to answer the question. If you don't know the answer, just say that you don't know. "
    "\n\nContext: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Helper function to format the retrieved documents into a single string
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def ask_pdf(user_question: str) -> dict:
    print(f"🔎 Searching PDF database for: '{user_question}'...")
    
    vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})
    
    # Step 1: Explicitly retrieve the documents from ChromaDB
    docs = retriever.invoke(user_question)
    
    # Step 2: Format the text and send it to the LLM
    formatted_context = format_docs(docs)
    
    # We create a simple chain: Prompt -> LLM
    simple_chain = prompt | llm
    response = simple_chain.invoke({
        "context": formatted_context, 
        "input": user_question
    })
    
    # Step 3: Build the Citations List
    sources = []
    for doc in docs:
        page_num = doc.metadata.get("page", 0) + 1 
        source_file = doc.metadata.get("source", "Unknown Document")
        
        clean_source = f"{source_file} (Page {page_num})"
        
        if clean_source not in sources:
            sources.append(clean_source)
            
    # Step 4: Return exactly what FastAPI expects
    # Notice we use response.content here!
    return {
        "answer": response.content,
        "sources": sources
    }