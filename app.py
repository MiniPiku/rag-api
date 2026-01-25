from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import ollama
import uuid
import os

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")
ollama_client = ollama.Client(host="http://host.docker.internal:11434")

class TextInput(BaseModel):
    text: str

@app.post("/query")
def query(q: str):
    try:
        results = collection.query(query_texts=[q], n_results=1)
        context = results["documents"][0][0] if results["documents"] else ""

        answer = ollama_client.generate(
            model="tinyllama",
            prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
        )

        return {"answer": answer["response"]}
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process query: {str(e)}",
            "hint": "Make sure Ollama is running and accessible. If running in Docker, check OLLAMA_HOST environment variable."
        }


@app.post("/add")
def add_knowledge(input_data: TextInput):
    """Add new content to the knowledge base dynamically."""
    try:
        # Generate a unique ID for this document
        doc_id = str(uuid.uuid4())
        
        # Add the text to Chroma collection
        collection.add(documents=[input_data.text], ids=[doc_id])
        
        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/health")
def health():
    return {"status": "ok"}