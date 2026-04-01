import streamlit as st
import requests

# Set page config for a wider, cleaner look
st.set_page_config(page_title="Private Document AI", page_icon="📄", layout="wide")

# ==========================================
# SIDEBAR: File Upload & Instructions
# ==========================================
with st.sidebar:
    st.header("Document Management")
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Ingest PDF", use_container_width=True):
            with st.spinner("Processing into Vector DB..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post("http://127.0.0.1:8000/upload-pdf", files=files)
                
                if response.status_code == 200:
                    st.success(f"✅ Ready! The AI has memorized {uploaded_file.name}")
                else:
                    st.error("Upload failed. Check backend.")
                    
    st.markdown("---")
    st.markdown("**How to use:**\n1. Upload your PDF.\n2. Click Ingest.\n3. Ask questions in the main chat area.")

# ==========================================
# MAIN AREA: Chat Interface
# ==========================================
st.title("📄 Private Document AI")
st.caption("A completely local, privacy-first RAG system powered by Mistral.")

# Modern Chat Input Box at the bottom of the screen
user_question = st.chat_input("Ask a question about your document...")

if user_question:
    # 1. Display the user's message in a chat bubble
    with st.chat_message("user"):
        st.write(user_question)
        
    # 2. Display the AI's response in a chat bubble
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                payload = {"question": user_question}
                response = requests.post("http://127.0.0.1:8000/ask-pdf", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_answer = data.get("answer", "Error: No answer found.")
                    sources = data.get("sources", [])
                    
                    # Print the main answer
                    st.write(ai_answer)
                    
                    # Print the citations neatly at the bottom of the bubble
                    if sources:
                        st.divider()
                        st.write("**Sources:**")
                        for source in sources:
                            st.caption(f"- {source}")
                else:
                    st.error(f"Backend Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Is FastAPI running?")