import os
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Path to docs folder
docs_folder = "___our specified doc foler path should be mentioned here___"

# Load documents
documents = []
doc_names = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(docs_folder, filename), "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(text)
            doc_names.append(filename)

# Chunk documents (simple split by 200 words)
def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks

all_chunks = []
chunk_sources = []

for i, doc in enumerate(documents):
    chunks = chunk_text(doc)
    all_chunks.extend(chunks)
    chunk_sources.extend([doc_names[i]] * len(chunks))

print(f"Total chunks created: {len(all_chunks)}")

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(all_chunks, show_progress_bar=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index and metadata
faiss.write_index(index, "faiss_index.bin")
with open("chunk_sources.pkl", "wb") as f:
    pickle.dump({"chunks": all_chunks, "sources": chunk_sources}, f)

print("FAISS index and chunk metadata saved successfully!")
