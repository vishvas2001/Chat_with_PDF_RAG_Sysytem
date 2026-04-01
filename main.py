import os
import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
from ingest import process_pdf
from llm_service import ask_langchain_ai, ask_pdf

app = FastAPI()

class PromptRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Enter your question here.")
    
@app.post("/ask")
async def ask_ai(data: PromptRequest):
    response = ask_langchain_ai(data.question)
     
    return {
        'result': response
    }

@app.post("/ask-pdf")
async def AskPDF(data: PromptRequest):
    response = ask_pdf(data.question)
    
    return response
    
@app.post("/upload-pdf")
async def upload_document(file: UploadFile = File(...)):
    
    file_path = f'temp_{file.filename}'
    
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        process_pdf(file_path)
        
        os.remove(file_path)
        
        return {'message': f'Successfully ingested {file.filename}'}
    except Exception as e:
        return {'error': str(e)}