import os
import faiss
import pickle
import numpy as np
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

documents_folder = os.path.join(PROJECT_ROOT, "documents")
faiss_path = os.path.join(PROJECT_ROOT, "faiss_index.bin")
chunks_path = os.path.join(PROJECT_ROOT, "chunk_sources.pkl")

# -----------------------------
# Load embedding model
# -----------------------------
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# PDF Reader
# -----------------------------
def read_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    return text

# -----------------------------
# Load documents
# -----------------------------
print("Loading documents...")

documents = []

for filename in os.listdir(documents_folder):

    file_path = os.path.join(documents_folder, filename)

    if filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    elif filename.endswith(".pdf"):
        text = read_pdf(file_path)

    else:
        continue

    documents.append({
        "text": text,
        "source": filename
    })

print(f"Loaded {len(documents)} documents")

# -----------------------------
# Chunk documents
# -----------------------------
print("Chunking documents...")

chunks = []

for doc in documents:

    sentences = doc["text"].split(".")

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 20:
            chunks.append({
                "text": sentence,
                "source": doc["source"]
            })

print(f"Created {len(chunks)} chunks")

# -----------------------------
# Create embeddings
# -----------------------------
print("Creating embeddings...")

chunk_texts = [c["text"] for c in chunks]

embeddings = model.encode(chunk_texts)

embeddings = np.array(embeddings).astype("float32")

# -----------------------------
# Create FAISS index
# -----------------------------
print("Building FAISS index...")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# -----------------------------
# Save index
# -----------------------------
faiss.write_index(index, faiss_path)

with open(chunks_path, "wb") as f:
    pickle.dump(chunks, f)

print("✅ Vector database created successfully!")
print(f"Chunks: {len(chunks)}")
print(f"FAISS saved at: {faiss_path}")
print(f"Chunk metadata saved at: {chunks_path}")