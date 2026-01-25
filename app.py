import os
from fastapi import FastAPI, HTTPException
import chromadb

# -----------------------------
# Mock LLM mode (for CI/testing)
# -----------------------------
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

if not USE_MOCK_LLM:
    import ollama

app = FastAPI()

# -----------------------------
# Vector DB
# -----------------------------
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

# -----------------------------
# Query endpoint
# -----------------------------
@app.post("/query")
def query(q: str):
    try:
        results = collection.query(query_texts=[q], n_results=1)
        context = results["documents"][0][0] if results.get("documents") else ""

        # -----------------------------
        # Mock mode (CI / unit tests)
        # -----------------------------
        if USE_MOCK_LLM:
            return {
                "answer": context or "No relevant context found."
            }

        # -----------------------------
        # Production mode (Ollama)
        # -----------------------------
        response = ollama.generate(
            model="tinyllama",
            prompt=(
                f"Context:\n{context}\n\n"
                f"Question: {q}\n\n"
                f"Answer clearly and concisely:"
            ),
        )

        return {
            "answer": response["response"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
