import faiss
import pickle
import numpy as np
import subprocess
import os
from sentence_transformers import SentenceTransformer

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

FAISS_PATH = os.path.join(PROJECT_ROOT, "faiss_index.bin")
CHUNKS_PATH = os.path.join(PROJECT_ROOT, "chunk_sources.pkl")

# -----------------------------
# Load embedding model
# -----------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# Load FAISS index
# -----------------------------
index = faiss.read_index(FAISS_PATH)

with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

print("🔎 Professional RAG System Ready")
print("--------------------------------")


# -----------------------------
# Search function
# -----------------------------
def search(query, k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"), k
    )

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results


# -----------------------------
# Ask LLM function
# -----------------------------
def ask_llm(prompt):

    process = subprocess.Popen(
        ["ollama", "run", "gemma3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    output, _ = process.communicate(prompt)

    return output